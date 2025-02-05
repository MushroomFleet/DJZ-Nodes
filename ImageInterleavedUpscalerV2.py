import torch
import torch.nn.functional as F
from typing import Tuple
from comfy import model_management
import comfy.utils

class ImageInterleavedUpscalerV2:
    """
    ComfyUI custom node for GAN-enhanced image upscaling with interlacing.
    Combines interlaced processing with external upscaling models.
    """
    
    def __init__(self):
        self.device = model_management.get_torch_device()
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "upscale_model": ("UPSCALE_MODEL",),
                "field_order": (["top_first", "bottom_first"], {
                    "default": "top_first"
                }),
                "blend_factor": ("FLOAT", {
                    "default": 0.25,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.05,
                    "display": "slider"
                }),
                "field_strength": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.1,
                    "display": "slider"
                }),
            },
            "optional": {
                "tile_size": ("INT", {
                    "default": 512,
                    "min": 128,
                    "max": 1024,
                    "step": 64,
                }),
                "tile_overlap": ("INT", {
                    "default": 32,
                    "min": 16,
                    "max": 256,
                    "step": 16,
                }),
                "edge_enhancement": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.1,
                }),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "upscale_interleaved"
    CATEGORY = "image/upscaling"

    def apply_edge_enhancement(self, frame: torch.Tensor, strength: float) -> torch.Tensor:
        """Apply edge enhancement using Sobel operator"""
        if strength == 0:
            return frame
            
        sobel_x = torch.tensor([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], device=self.device).float()
        sobel_y = torch.tensor([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], device=self.device).float()
        
        frame_gray = frame.mean(dim=-1, keepdim=True)
        frame_gray = frame_gray.permute(2, 0, 1).unsqueeze(0)
        
        edges_x = F.conv2d(frame_gray, sobel_x.view(1, 1, 3, 3), padding=1)
        edges_y = F.conv2d(frame_gray, sobel_y.view(1, 1, 3, 3), padding=1)
        edges = torch.sqrt(edges_x.pow(2) + edges_y.pow(2))
        
        edges = edges / edges.max() * strength
        enhanced = frame + edges.squeeze(0).permute(1, 2, 0).repeat(1, 1, frame.shape[-1])
        return torch.clamp(enhanced, 0, 1)

    def process_image_with_model(self,
                               image: torch.Tensor,
                               upscale_model,
                               tile_size: int,
                               tile_overlap: int) -> torch.Tensor:
        """Process a single image using the upscale model with tiling"""
        device = self.device
        
        # Calculate memory requirements
        memory_required = model_management.module_size(upscale_model.model)
        memory_required += (tile_size * tile_size * 3) * image.element_size() * max(upscale_model.scale, 1.0) * 384.0
        memory_required += image.nelement() * image.element_size()
        model_management.free_memory(memory_required, device)
        
        # Ensure image has correct shape and type
        if len(image.shape) == 2:  # HW
            # Add channel dimension for grayscale
            image = image.unsqueeze(-1).repeat(1, 1, 3)
        elif len(image.shape) == 3 and image.shape[-1] == 1:  # HW1
            # Expand single channel to RGB
            image = image.repeat(1, 1, 3)
        
        # Add batch dimension if needed
        if len(image.shape) == 3:  # HWC
            image = image.unsqueeze(0)  # Add batch dimension
            
        # Move channels to proper position for processing
        image = image.movedim(-1, -3)  # HWC to CHW
        image = image.float().to(device)
            
        # Process with tiling
        try:
            steps = image.shape[0] * comfy.utils.get_tiled_scale_steps(
                image.shape[3], image.shape[2],
                tile_x=tile_size, tile_y=tile_size,
                overlap=tile_overlap
            )
            pbar = comfy.utils.ProgressBar(steps)
            
            upscaled = comfy.utils.tiled_scale(
                image,
                lambda a: upscale_model(a),
                tile_x=tile_size,
                tile_y=tile_size,
                overlap=tile_overlap,
                upscale_amount=upscale_model.scale,
                pbar=pbar
            )
        except model_management.OOM_EXCEPTION as e:
            if tile_size < 128:
                raise e
            return self.process_image_with_model(
                image, upscale_model,
                tile_size // 2,
                tile_overlap
            )
            
        # Convert back to HWC format
        upscaled = upscaled.movedim(-3, -1)  # CHW to HWC
        if upscaled.shape[0] == 1:  # Remove batch dimension if present
            upscaled = upscaled.squeeze(0)
            
        return upscaled

    def create_interlaced_image(self,
                              image: torch.Tensor,
                              upscale_model,
                              field_order: str,
                              blend_factor: float,
                              field_strength: float,
                              tile_size: int,
                              tile_overlap: int) -> torch.Tensor:
        """Create an interlaced image using the upscale model"""
        # Ensure image is on the correct device
        image = image.to(self.device)
        
        # First do the full image upscale
        upscaled = self.process_image_with_model(
            image, upscale_model,
            tile_size, tile_overlap
        ).to(self.device)
        
        # Now apply interlacing to the upscaled image
        height = upscaled.shape[0]
        even_mask = torch.zeros((height, 1, 1), device=self.device)
        odd_mask = torch.zeros((height, 1, 1), device=self.device)
        
        if field_order == "top_first":
            even_mask[::2] = field_strength
            odd_mask[1::2] = field_strength
        else:
            even_mask[1::2] = field_strength
            odd_mask[::2] = field_strength
            
        # Create shifted versions for field blending
        shifted_up = torch.roll(upscaled, shifts=-1, dims=0)
        shifted_down = torch.roll(upscaled, shifts=1, dims=0)
        
        # Apply field masks and blend
        even_field = upscaled * even_mask
        odd_field = upscaled * odd_mask
        
        # Blend with shifted fields for smoother transitions
        even_field = even_field * (1 - blend_factor) + shifted_down * even_mask * blend_factor
        odd_field = odd_field * (1 - blend_factor) + shifted_up * odd_mask * blend_factor
        
        # Combine fields
        interlaced = even_field + odd_field
        
        return interlaced

    def upscale_interleaved(self,
                           image: torch.Tensor,
                           upscale_model,
                           field_order: str,
                           blend_factor: float,
                           field_strength: float,
                           tile_size: int = 512,
                           tile_overlap: int = 32,
                           edge_enhancement: float = 0.0) -> Tuple[torch.Tensor]:
        """
        Main processing function that combines upscaling with interlacing.
        Ensures output is in BHWC format for compatibility with video pipeline.
        """
        try:
            # Move model to appropriate device
            upscale_model.to(self.device)
            
            # Ensure input is at least 3D (HWC)
            if len(image.shape) == 2:  # HW
                image = image.unsqueeze(-1).repeat(1, 1, 3)
            elif len(image.shape) == 3 and image.shape[-1] == 1:  # HW1
                image = image.repeat(1, 1, 3)
            
            # Add batch dimension if needed
            if len(image.shape) == 3:  # HWC
                image = image.unsqueeze(0)  # BHWC
            
            # Process image
            processed = self.create_interlaced_image(
                image,
                upscale_model,
                field_order,
                blend_factor,
                field_strength,
                tile_size,
                tile_overlap
            )
            
            # Apply edge enhancement if requested
            if edge_enhancement > 0:
                processed = self.apply_edge_enhancement(processed, edge_enhancement)
            
            # Ensure output has batch dimension (BHWC)
            if len(processed.shape) == 3:  # HWC
                processed = processed.unsqueeze(0)
            
            # Cleanup
            upscale_model.to("cpu")
            torch.cuda.empty_cache()
            
            result = torch.clamp(processed, 0, 1)
            
            # Double-check dimensions
            if len(result.shape) != 4:
                raise ValueError(f"Expected 4D tensor output (BHWC), got shape {result.shape}")
            
            return (result,)
            
        except Exception as e:
            # Ensure model is moved back to CPU on error
            upscale_model.to("cpu")
            torch.cuda.empty_cache()
            raise e

NODE_CLASS_MAPPINGS = {
    "ImageInterleavedUpscalerV2": ImageInterleavedUpscalerV2
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageInterleavedUpscalerV2": "Image Interleaved Upscaler V2"
}