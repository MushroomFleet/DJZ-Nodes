import torch
import torch.nn.functional as F
from typing import Tuple, List, Optional
import numpy as np
from comfy import model_management
import comfy.utils

class VideoInterlaceGANV3:
    """
    ComfyUI custom node for GAN-enhanced video frame upscaling.
    Combines interlaced processing with external upscaling models.
    """
    
    def __init__(self):
        self.device = model_management.get_torch_device()
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "upscale_model": ("UPSCALE_MODEL",),  # Add support for external models
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
                "temporal_radius": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 3,
                    "step": 1,
                    "display": "number"
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
                "enhance_edges": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.1,
                }),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "process_video"
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

    def apply_temporal_compensation(self,
                                  frames: torch.Tensor,
                                  blend_factor: float,
                                  temporal_radius: int) -> torch.Tensor:
        """
        Apply temporal compensation across input frames before upscaling.
        This ensures consistent dimensions throughout the process.
        """
        # Ensure frames are on correct device
        frames = frames.to(self.device)
        batch_size = frames.shape[0]
        compensated = frames.clone()
        
        # Calculate temporal weights (ensure on correct device)
        radius_size = 2 * temporal_radius + 1
        weights = torch.softmax(
            torch.tensor([1.0] * radius_size, device=self.device),
            dim=0
        )
        
        # Process center frames
        for i in range(temporal_radius, batch_size - temporal_radius):
            # Get temporal window of original-sized frames
            window = frames[i-temporal_radius:i+temporal_radius+1].to(self.device)
            # Apply weighted average
            compensated[i] = torch.sum(
                window * weights.view(-1, 1, 1, 1).to(self.device),
                dim=0
            )
            
        # Handle edge cases
        for i in range(temporal_radius):
            # Start of sequence
            available_frames = frames[0:2*temporal_radius+1].to(self.device)
            edge_weights = torch.softmax(
                torch.tensor([1.0] * len(available_frames), device=self.device),
                dim=0
            )
            compensated[i] = torch.sum(
                available_frames * edge_weights.view(-1, 1, 1, 1),
                dim=0
            )
            
            # End of sequence
            end_idx = batch_size - i - 1
            available_frames = frames[batch_size-2*temporal_radius-1:batch_size].to(self.device)
            compensated[end_idx] = torch.sum(
                available_frames * edge_weights.view(-1, 1, 1, 1),
                dim=0
            )
            
        return compensated.to(self.device)

    def process_frame_with_model(self,
                               frame: torch.Tensor,
                               upscale_model,
                               tile_size: int,
                               tile_overlap: int) -> torch.Tensor:
        """Process a single frame using the upscale model with tiling"""
        device = self.device
        
        # Calculate memory requirements
        memory_required = model_management.module_size(upscale_model.model)
        memory_required += (tile_size * tile_size * 3) * frame.element_size() * max(upscale_model.scale, 1.0) * 384.0
        memory_required += frame.nelement() * frame.element_size()
        model_management.free_memory(memory_required, device)
        
        # Ensure frame has correct shape and type
        if len(frame.shape) == 3:  # HWC
            frame = frame.unsqueeze(0)  # Add batch dimension
        frame = frame.movedim(-1, -3)  # HWC to CHW
        frame = frame.float().to(device)
            
        # Process with tiling
        try:
            steps = frame.shape[0] * comfy.utils.get_tiled_scale_steps(
                frame.shape[3], frame.shape[2],
                tile_x=tile_size, tile_y=tile_size,
                overlap=tile_overlap
            )
            pbar = comfy.utils.ProgressBar(steps)
            
            upscaled = comfy.utils.tiled_scale(
                frame,
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
            return self.process_frame_with_model(
                frame, upscale_model,
                tile_size // 2,
                tile_overlap
            )
            
        # Convert back to HWC format
        upscaled = upscaled.movedim(-3, -1)  # CHW to HWC
        if upscaled.shape[0] == 1:  # Remove batch dimension if present
            upscaled = upscaled.squeeze(0)
            
        return upscaled

    def create_interlaced_frame(self,
                              frame: torch.Tensor,
                              upscale_model,
                              field_order: str,
                              blend_factor: float,
                              tile_size: int,
                              tile_overlap: int) -> torch.Tensor:
        """Create an interlaced frame using the upscale model"""
        # Ensure frame is on the correct device
        frame = frame.to(self.device)
        
        # First do the full frame upscale
        upscaled = self.process_frame_with_model(
            frame, upscale_model,
            tile_size, tile_overlap
        ).to(self.device)
        
        # Now apply interlacing to the upscaled frame
        height = upscaled.shape[0]
        even_mask = torch.zeros((height, 1, 1), device=self.device)
        odd_mask = torch.zeros((height, 1, 1), device=self.device)
        
        if field_order == "top_first":
            even_mask[::2] = 1.0
            odd_mask[1::2] = 1.0
        else:
            even_mask[1::2] = 1.0
            odd_mask[::2] = 1.0
            
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

    def process_video(self,
                     images: torch.Tensor,
                     upscale_model,
                     field_order: str,
                     blend_factor: float,
                     temporal_radius: int,
                     tile_size: int = 512,
                     tile_overlap: int = 32,
                     enhance_edges: float = 0.0) -> Tuple[torch.Tensor]:
        """
        Main processing function for video frames.
        Applies temporal compensation on input frames before upscaling.
        """
        try:
            # Move model to appropriate device
            upscale_model.to(self.device)
            
            # Process batch
            batch_size = images.shape[0]
            output_frames = []
            
            # Process each frame
            for i in range(batch_size):
                # Create interlaced frame
                processed = self.create_interlaced_frame(
                    images[i],
                    upscale_model,
                    field_order,
                    blend_factor,
                    tile_size,
                    tile_overlap
                )
                output_frames.append(processed)
                
            # Combine frames
            output = torch.stack(output_frames)
            
            # Apply temporal compensation to input frames before processing
            if temporal_radius > 0:
                images = self.apply_temporal_compensation(
                    images,
                    blend_factor,
                    temporal_radius
                )
                
            # Apply edge enhancement if requested
            if enhance_edges > 0:
                for i in range(len(output)):
                    output[i] = self.apply_edge_enhancement(
                        output[i],
                        enhance_edges
                    )
            
            # Cleanup
            upscale_model.to("cpu")
            torch.cuda.empty_cache()
            
            return (torch.clamp(output, 0, 1),)
            
        except Exception as e:
            # Ensure model is moved back to CPU on error
            upscale_model.to("cpu")
            torch.cuda.empty_cache()
            raise e

NODE_CLASS_MAPPINGS = {
    "VideoInterlaceGANV3": VideoInterlaceGANV3
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VideoInterlaceGANV3": "Video Interlace GAN V3"
}