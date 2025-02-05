import torch
import torch.nn.functional as F
from typing import Tuple
import math

class BlackBarsV2:
    """
    ComfyUI custom node that applies industry-standard letterboxing/pillarboxing
    with aspect ratio detection and center crop options.
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
                "mode": (["letterbox", "pillarbox", "center_crop"],),
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

    def calculate_bars(self, input_res: Tuple[int, int], 
                      target_ratio: str) -> Tuple[int, int, int, int]:
        """
        Calculates the required bar sizes for the given input resolution and target ratio.
        Returns (top, bottom, left, right) bar sizes.
        """
        width, height = input_res
        input_ratio = width / height
        
        if target_ratio == "auto":
            target_ratio = self.detect_aspect_ratio(width, height)
        
        # Strip suffix from target ratio if present
        target_ratio = target_ratio.split(" ")[0]
        target_ratio_float = self.ASPECT_RATIOS[target_ratio]
        
        if abs(input_ratio - target_ratio_float) < 0.01:
            return (0, 0, 0, 0)  # No bars needed
            
        if input_ratio > target_ratio_float:
            # Need pillarboxing
            new_width = int(height * target_ratio_float)
            bar_size = (width - new_width) // 2
            return (0, 0, bar_size, bar_size)
        else:
            # Need letterboxing
            new_height = int(width / target_ratio_float)
            bar_size = (height - new_height) // 2
            return (bar_size, bar_size, 0, 0)

    def apply_center_crop(self, images: torch.Tensor, 
                         target_ratio: str) -> torch.Tensor:
        """
        Applies center crop to achieve target ratio without black bars
        """
        B, H, W, C = images.shape
        
        if target_ratio == "auto":
            return images
            
        target_ratio = target_ratio.split(" ")[0]
        target_ratio_float = self.ASPECT_RATIOS[target_ratio]
        current_ratio = W / H
        
        if current_ratio > target_ratio_float:
            # Crop width
            new_width = int(H * target_ratio_float)
            start = (W - new_width) // 2
            images = images[:, :, start:start + new_width, :]
        else:
            # Crop height
            new_height = int(W / target_ratio_float)
            start = (H - new_height) // 2
            images = images[:, start:start + new_height, :, :]
            
        return images

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
                        mode: str,
                        target_ratio: str,
                        safe_area: bool,
                        show_guides: bool) -> Tuple[torch.Tensor]:
        """
        Apply letterboxing/pillarboxing or center crop with optional guides.
        
        Args:
            images: Input tensor of shape (B, H, W, C)
            mode: "letterbox", "pillarbox", or "center_crop"
            target_ratio: Target aspect ratio (or "auto")
            safe_area: Whether to apply safe area guides
            show_guides: Whether to show crop/bar guides
        
        Returns:
            Tuple containing the processed images tensor
        """
        
        # Ensure input is torch tensor on the correct device
        if not isinstance(images, torch.Tensor):
            images = torch.tensor(images, device=self.device)
        else:
            images = images.to(self.device)
        
        B, H, W, C = images.shape
        
        # Handle center crop mode
        if mode == "center_crop":
            result = self.apply_center_crop(images, target_ratio)
        else:
            # Calculate required bar sizes
            top, bottom, left, right = self.calculate_bars((W, H), target_ratio)
            
            # Create base mask
            mask = torch.ones((B, H, W, C), device=self.device)
            
            # Apply bars through mask
            if top > 0:
                mask[:, :top, :, :] = 0
                mask[:, -bottom:, :, :] = 0
            if left > 0:
                mask[:, :, :left, :] = 0
                mask[:, :, -right:, :] = 0
            
            result = images * mask
        
        # Apply safe area guides if requested
        if safe_area or show_guides:
            result = self.apply_safe_area_guides(result)
        
        return (result,)

NODE_CLASS_MAPPINGS = {
    "BlackBarsV2": BlackBarsV2
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BlackBarsV2": "Black Bars V2"
}