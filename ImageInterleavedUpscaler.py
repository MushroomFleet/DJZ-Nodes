import torch
import torch.nn.functional as F
from typing import Tuple

class ImageInterleavedUpscaler:
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "upscale_interleaved"
    CATEGORY = "image/upscaling"

    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "input_width": ("INT", {
                    "default": 1280,
                    "min": 640,
                    "max": 7680,
                    "step": 1,
                    "display": "number"
                }),
                "input_height": ("INT", {
                    "default": 720,
                    "min": 480,
                    "max": 4320,
                    "step": 1,
                    "display": "number"
                }),
                "scale_factor": ("FLOAT", {
                    "default": 1.5,
                    "min": 1.0,
                    "max": 4.0,
                    "step": 0.1,
                    "display": "slider"
                }),
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
                "interpolation_mode": (["bilinear", "bicubic", "nearest"], {
                    "default": "bilinear"
                }),
                "field_strength": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.1,
                    "display": "slider"
                }),
                "edge_enhancement": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.1,
                    "display": "slider"
                })
            }
        }

    def apply_edge_enhancement(self, frame: torch.Tensor, strength: float) -> torch.Tensor:
        """
        Applies edge enhancement to the frame using a Sobel operator.
        """
        if strength == 0:
            return frame
            
        # Sobel operators
        sobel_x = torch.tensor([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], device=self.device).float()
        sobel_y = torch.tensor([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], device=self.device).float()
        
        # Expand dimensions for conv2d
        frame_gray = frame.mean(dim=-1, keepdim=True)
        frame_gray = frame_gray.permute(0, 3, 1, 2)
        
        # Apply Sobel operators
        edges_x = F.conv2d(frame_gray, sobel_x.view(1, 1, 3, 3), padding=1)
        edges_y = F.conv2d(frame_gray, sobel_y.view(1, 1, 3, 3), padding=1)
        edges = torch.sqrt(edges_x.pow(2) + edges_y.pow(2))
        
        # Normalize and apply strength
        edges = edges / edges.max() * strength
        
        # Add enhanced edges to original frame
        enhanced = frame + edges.permute(0, 2, 3, 1).repeat(1, 1, 1, frame.shape[-1])
        return torch.clamp(enhanced, 0, 1)

    def create_interleaved_image(self,
                               image: torch.Tensor,
                               input_width: int,
                               input_height: int,
                               scale_factor: float,
                               field_order: str = "top_first",
                               blend_factor: float = 0.25,
                               interpolation_mode: str = "bilinear",
                               field_strength: float = 1.0,
                               edge_enhancement: float = 0.0) -> torch.Tensor:
        """
        Creates an interleaved image with proper aspect ratio maintenance.
        """
        # Calculate target dimensions maintaining aspect ratio
        target_height = int(input_height * scale_factor)
        target_width = int(input_width * scale_factor)
        
        # Input is in format (B,H,W,C), needs to be (B,C,H,W) for interpolation
        if len(image.shape) != 4:
            raise ValueError(f"Expected 4D input tensor (B,H,W,C), got shape {image.shape}")
            
        # Convert from (B,H,W,C) to (B,C,H,W)
        image_reshaped = image.permute(0, 3, 1, 2)
        
        # Upscale the input image
        upscaled = F.interpolate(
            image_reshaped,
            size=(target_height, target_width),
            mode=interpolation_mode,
            align_corners=False if interpolation_mode != 'nearest' else None
        )
        
        # Convert back to (B,H,W,C)
        upscaled = upscaled.permute(0, 2, 3, 1)
        
        # Create field masks
        even_mask = torch.zeros((target_height, 1, 1), device=self.device)
        odd_mask = torch.zeros((target_height, 1, 1), device=self.device)
        
        if field_order == "top_first":
            even_mask[::2] = 1.0
            odd_mask[1::2] = 1.0
        else:
            even_mask[1::2] = 1.0
            odd_mask[::2] = 1.0
        
        # Apply field strength
        even_mask *= field_strength
        odd_mask *= field_strength
        
        # Apply masks to all images in batch
        even_field = upscaled * even_mask.unsqueeze(0)
        odd_field = upscaled * odd_mask.unsqueeze(0)
        
        # Blend fields
        if blend_factor > 0:
            shifted_even = torch.roll(even_field, shifts=1, dims=1)
            shifted_odd = torch.roll(odd_field, shifts=-1, dims=1)
            
            blended = (
                (even_field + odd_field) * (1 - blend_factor) +
                (shifted_even + shifted_odd) * blend_factor
            )
        else:
            blended = even_field + odd_field
        
        # Apply edge enhancement if enabled
        if edge_enhancement > 0:
            blended = self.apply_edge_enhancement(blended, edge_enhancement)
        
        return blended

    def upscale_interleaved(self,
                           image: torch.Tensor,
                           input_width: int,
                           input_height: int,
                           scale_factor: float,
                           field_order: str,
                           blend_factor: float,
                           interpolation_mode: str,
                           field_strength: float = 1.0,
                           edge_enhancement: float = 0.0) -> Tuple[torch.Tensor]:
        """
        Upscale an image using interleaving while maintaining aspect ratio.
        """
        # Ensure input is on correct device and has correct dimensions
        if not isinstance(image, torch.Tensor):
            image = torch.tensor(image, device=self.device)
        else:
            image = image.to(self.device)
            
        # Ensure we have a 4D tensor
        if len(image.shape) == 3:
            image = image.unsqueeze(0)
        
        # Process image
        output = self.create_interleaved_image(
            image,
            input_width,
            input_height,
            scale_factor,
            field_order,
            blend_factor,
            interpolation_mode,
            field_strength,
            edge_enhancement
        )
        
        return (torch.clamp(output, 0, 1),)

NODE_CLASS_MAPPINGS = {
    "ImageInterleavedUpscaler": ImageInterleavedUpscaler
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageInterleavedUpscaler": "Image Interleaved Upscaler"
}