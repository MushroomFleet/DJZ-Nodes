import torch
import torch.nn.functional as F
from typing import Tuple

class VideoInterlaced:
    """
    ComfyUI custom node that performs interlaced upscaling of video frames,
    similar to the technique used to convert 720p to 1080i.
    """
    
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "input_height": ("INT", {
                    "default": 720,
                    "min": 480,
                    "max": 4320,
                    "step": 1,
                    "display": "number"
                }),
                "input_width": ("INT", {
                    "default": 1280,
                    "min": 640,
                    "max": 7680,
                    "step": 1,
                    "display": "number"
                }),
                "field_order": (["top_first", "bottom_first"], {"default": "top_first"}),
                "blend_factor": ("FLOAT", {
                    "default": 0.25,
                    "min": 0.0,
                    "max": 0.5,
                    "step": 0.05,
                    "display": "slider"
                })
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_interlacing"
    CATEGORY = "image/upscaling"

    def create_interlaced_frame(self, 
                              frame: torch.Tensor,
                              target_height: int,
                              target_width: int,
                              field_order: str,
                              blend_factor: float) -> torch.Tensor:
        """
        Creates an interlaced frame by alternating lines and applying motion compensation.
        
        Args:
            frame: Input tensor of shape (H, W, C)
            target_height: Desired output height
            target_width: Desired output width
            field_order: Whether top or bottom field comes first
            blend_factor: Amount of blending between fields
            
        Returns:
            Interlaced frame tensor of shape (target_height, target_width, C)
        """
        # Initial bilinear upscale
        upscaled = F.interpolate(
            frame.unsqueeze(0).permute(0, 3, 1, 2),
            size=(target_height, target_width),
            mode='bilinear',
            align_corners=False
        ).permute(0, 2, 3, 1).squeeze(0)
        
        # Create masks for even and odd lines
        even_mask = torch.zeros((target_height, 1, 1), device=self.device)
        odd_mask = torch.zeros((target_height, 1, 1), device=self.device)
        
        if field_order == "top_first":
            even_mask[::2] = 1.0
            odd_mask[1::2] = 1.0
        else:
            even_mask[1::2] = 1.0
            odd_mask[::2] = 1.0
            
        # Apply field separation
        even_field = upscaled * even_mask
        odd_field = upscaled * odd_mask
        
        # Apply motion compensation blend
        if blend_factor > 0:
            # Shift fields for motion compensation
            shifted_even = torch.roll(even_field, shifts=1, dims=0)
            shifted_odd = torch.roll(odd_field, shifts=-1, dims=0)
            
            # Blend with shifted fields
            even_field = (1 - blend_factor) * even_field + blend_factor * shifted_odd
            odd_field = (1 - blend_factor) * odd_field + blend_factor * shifted_even
            
        # Combine fields
        interlaced = even_field + odd_field
        
        return interlaced

    def apply_interlacing(self,
                         images: torch.Tensor,
                         input_height: int,
                         input_width: int,
                         field_order: str,
                         blend_factor: float) -> Tuple[torch.Tensor]:
        """
        Apply interlaced upscaling to a batch of images.
        
        Args:
            images: Input tensor of shape (B, H, W, C)
            input_height: Original frame height
            input_width: Original frame width
            field_order: Field ordering ("top_first" or "bottom_first")
            blend_factor: Amount of blending between fields
            
        Returns:
            Tuple containing the processed images tensor
        """
        # Ensure input is torch tensor on correct device
        if not isinstance(images, torch.Tensor):
            images = torch.tensor(images, device=self.device)
        else:
            images = images.to(self.device)
            
        # Calculate target dimensions (typically 1.5x for 720p to 1080i)
        target_height = int(input_height * 1.5)  # e.g., 720 -> 1080
        target_width = int(input_width * 1.5)    # e.g., 1280 -> 1920
        
        # Process each image in batch
        batch_size = images.shape[0]
        output = torch.zeros((batch_size, target_height, target_width, images.shape[3]), 
                           device=self.device)
        
        for i in range(batch_size):
            output[i] = self.create_interlaced_frame(
                images[i],
                target_height,
                target_width,
                field_order,
                blend_factor
            )
            
        return (torch.clamp(output, 0, 1),)

NODE_CLASS_MAPPINGS = {
    "VideoInterlaced": VideoInterlaced
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VideoInterlaced": "Video Interlaced Upscaler"
}