import torch
import torch.nn.functional as F
from typing import Tuple
import math

class BlackBarsV3:
    """
    ComfyUI custom node that applies industry-standard letterboxing/pillarboxing
    with aspect ratio detection and padding options. Unlike V2, this version
    always preserves the full image by padding instead of cropping.
    """
    
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.ASPECT_RATIOS = {
            "2.39:1": 2.39,
            "2.35:1": 2.35,
            "1.85:1": 1.85,
            "16:9": 1.77777778,
            "3:2": 1.5,
            "4:3": 1.33333333,
            "1:1": 1.0,
            "9:16": 0.5625
        }
        
        self.COMMON_RESOLUTIONS = {
            (1920, 1080): "16:9",
            (3840, 2160): "16:9",
            (1280, 720): "16:9",
            (720, 480): "4:3",
            (720, 576): "4:3",
            (1080, 1920): "9:16",
            (1080, 1080): "1:1"
        }
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "target_ratio": ([
                    "auto",
                    "2.39:1 (Anamorphic)",
                    "2.35:1 (CinemaScope)",
                    "1.85:1 (Theatrical)",
                    "16:9 (HD)",
                    "4:3 (Classic)",
                    "1:1 (Square)",
                    "9:16 (Vertical)"
                ],),
                "safe_area": ("BOOLEAN", {"default": False}),
                "show_guides": ("BOOLEAN", {"default": False})
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_black_bars"
    CATEGORY = "image/format"

    def detect_aspect_ratio(self, width: int, height: int) -> str:
        """
        Detects the aspect ratio of the input image and returns the closest standard ratio.
        """
        # First check if it's a common resolution
        if (width, height) in self.COMMON_RESOLUTIONS:
            return self.COMMON_RESOLUTIONS[(width, height)]
        
        # Calculate actual ratio
        actual_ratio = width / height
        
        # Find closest standard ratio
        closest_ratio = min(self.ASPECT_RATIOS.items(), 
                          key=lambda x: abs(x[1] - actual_ratio))
        
        return closest_ratio[0]

    def calculate_padding(self, input_res: Tuple[int, int], 
                        target_ratio: str) -> Tuple[int, int, int, int, int, int]:
        """
        Calculates the required padding and new dimensions to achieve target ratio.
        Returns (new_width, new_height, top, bottom, left, right) padding sizes.
        """
        width, height = input_res
        input_ratio = width / height
        
        if target_ratio == "auto":
            target_ratio = self.detect_aspect_ratio(width, height)
        
        # Strip suffix from target ratio if present
        target_ratio = target_ratio.split(" ")[0]
        target_ratio_float = self.ASPECT_RATIOS[target_ratio]
        
        if abs(input_ratio - target_ratio_float) < 0.01:
            return width, height, 0, 0, 0, 0  # No padding needed
            
        if input_ratio > target_ratio_float:
            # Need to increase height
            new_height = int(width / target_ratio_float)
            pad_height = new_height - height
            top_pad = pad_height // 2
            bottom_pad = pad_height - top_pad
            return width, new_height, top_pad, bottom_pad, 0, 0
        else:
            # Need to increase width
            new_width = int(height * target_ratio_float)
            pad_width = new_width - width
            left_pad = pad_width // 2
            right_pad = pad_width - left_pad
            return new_width, height, 0, 0, left_pad, right_pad

    def apply_safe_area_guides(self, images: torch.Tensor) -> torch.Tensor:
        """
        Adds safe area guides overlay (90% and 80% markers)
        """
        B, H, W, C = images.shape
        guide_image = images.clone()
        
        # Calculate safe area boundaries
        action_safe = {
            'top': int(H * 0.1),
            'bottom': int(H * 0.9),
            'left': int(W * 0.1),
            'right': int(W * 0.9)
        }
        
        title_safe = {
            'top': int(H * 0.2),
            'bottom': int(H * 0.8),
            'left': int(W * 0.2),
            'right': int(W * 0.8)
        }
        
        # Draw guide lines
        line_color = torch.tensor([0.8, 0.8, 0.8], device=self.device)
        line_thickness = 2
        
        # Action safe area (90%)
        guide_image[:, action_safe['top']:action_safe['top'] + line_thickness, :, :] = line_color
        guide_image[:, action_safe['bottom']-line_thickness:action_safe['bottom'], :, :] = line_color
        guide_image[:, :, action_safe['left']:action_safe['left'] + line_thickness, :] = line_color
        guide_image[:, :, action_safe['right']-line_thickness:action_safe['right'], :] = line_color
        
        # Title safe area (80%)
        guide_image[:, title_safe['top']:title_safe['top'] + line_thickness, :, :] = line_color
        guide_image[:, title_safe['bottom']-line_thickness:title_safe['bottom'], :, :] = line_color
        guide_image[:, :, title_safe['left']:title_safe['left'] + line_thickness, :] = line_color
        guide_image[:, :, title_safe['right']-line_thickness:title_safe['right'], :] = line_color
        
        return guide_image

    def apply_black_bars(self, images: torch.Tensor,
                        target_ratio: str,
                        safe_area: bool,
                        show_guides: bool) -> Tuple[torch.Tensor]:
        """
        Apply padding to achieve target aspect ratio while preserving the entire image.
        
        Args:
            images: Input tensor of shape (B, H, W, C)
            target_ratio: Target aspect ratio (or "auto")
            safe_area: Whether to apply safe area guides
            show_guides: Whether to show padding guides
        
        Returns:
            Tuple containing the processed images tensor with padding
        """
        
        # Ensure input is torch tensor on the correct device
        if not isinstance(images, torch.Tensor):
            images = torch.tensor(images, device=self.device)
        else:
            images = images.to(self.device)
        
        B, H, W, C = images.shape
        
        # Calculate required padding and new dimensions
        new_width, new_height, top, bottom, left, right = self.calculate_padding((W, H), target_ratio)
        
        # Create new tensor with black padding
        result = torch.zeros((B, new_height, new_width, C), device=self.device)
        
        # Place original image in center
        result[:, top:top+H, left:left+W, :] = images
        
        # Apply safe area guides if requested
        if safe_area or show_guides:
            result = self.apply_safe_area_guides(result)
        
        return (result,)

NODE_CLASS_MAPPINGS = {
    "BlackBarsV3": BlackBarsV3
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BlackBarsV3": "Black Bars V3"
}