import torch
import torch.nn.functional as F
from typing import Tuple, List
import numpy as np
import colorsys

class ThreeToneStyler:
    """
    ComfyUI custom node for creating 3-tone stylized images with color relationship controls.
    Allows for creative color grading based on color theory relationships and luminance mapping.
    """
    
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "base_color": ("STRING", {
                    "default": "#0000FF",
                    "multiline": False
                }),
                "color_relationship": (["Primaries", "Secondaries", "Complementary", "Split Complementary", "Triadic", "Analogous"], {
                    "default": "Complementary"
                }),
                "tone_mapping": (["Highlights", "Midtones", "Shadows"], {
                    "default": "Midtones"
                }),
                "contrast": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 2.0,
                    "step": 0.1,
                    "display": "slider"
                }),
                "threshold_low": ("FLOAT", {
                    "default": 0.3,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.05,
                    "display": "slider"
                }),
                "threshold_high": ("FLOAT", {
                    "default": 0.7,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.05,
                    "display": "slider"
                }),
            },
            "optional": {
                "smoothing": ("FLOAT", {
                    "default": 0.1,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.05,
                    "display": "slider"
                }),
                "saturation": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.1,
                    "display": "slider"
                }),
                "preserve_luminance": ("BOOLEAN", {
                    "default": True
                })
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_three_tone"
    CATEGORY = "image/color"

    def hex_to_rgb(self, hex_color: str) -> Tuple[float, float, float]:
        """Convert hex color to RGB values (0-1 range)."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))

    def get_color_relationship(self, base_color: Tuple[float, float, float], 
                             relationship: str) -> Tuple[Tuple[float, float, float], 
                                                       Tuple[float, float, float]]:
        """Generate two additional colors based on the relationship to base color."""
        # Convert RGB to HSV for easier color relationship calculations
        h, s, v = colorsys.rgb_to_hsv(*base_color)
        
        if relationship == "Primaries":
            h1 = (h + 1/3) % 1
            h2 = (h + 2/3) % 1
        elif relationship == "Secondaries":
            h1 = (h + 0.5) % 1
            h2 = (h + 0.25) % 1
        elif relationship == "Complementary":
            h1 = (h + 0.5) % 1
            h2 = h  # Use base color twice
        elif relationship == "Split Complementary":
            h1 = (h + 0.5 - 0.15) % 1
            h2 = (h + 0.5 + 0.15) % 1
        elif relationship == "Triadic":
            h1 = (h + 1/3) % 1
            h2 = (h + 2/3) % 1
        else:  # Analogous
            h1 = (h + 0.083) % 1  # 30 degrees
            h2 = (h - 0.083) % 1  # -30 degrees
            
        color1 = colorsys.hsv_to_rgb(h1, s, v)
        color2 = colorsys.hsv_to_rgb(h2, s, v)
        return color1, color2

    def apply_tone_mapping(self, luminance: torch.Tensor, 
                          thresholds: Tuple[float, float]) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """Create masks for three-tone separation based on luminance values."""
        low, high = thresholds
        
        # Create smooth transitions between zones
        shadows = torch.sigmoid(-(luminance - low) / 0.1)
        highlights = torch.sigmoid((luminance - high) / 0.1)
        midtones = 1 - shadows - highlights
        
        return shadows, midtones, highlights

    def apply_three_tone(self,
                        images: torch.Tensor,
                        base_color: str,
                        color_relationship: str,
                        tone_mapping: str,
                        contrast: float,
                        threshold_low: float,
                        threshold_high: float,
                        smoothing: float = 0.1,
                        saturation: float = 1.0,
                        preserve_luminance: bool = True) -> Tuple[torch.Tensor]:
        """
        Apply three-tone styling to a batch of images.
        """
        # Convert input to device
        if not isinstance(images, torch.Tensor):
            images = torch.tensor(images, device=self.device)
        else:
            images = images.to(self.device)
        
        # Get the three colors based on relationship
        base_rgb = self.hex_to_rgb(base_color)
        color1_rgb, color2_rgb = self.get_color_relationship(base_rgb, color_relationship)
        
        # Convert colors to tensors
        colors = {
            "base": torch.tensor(base_rgb, device=self.device),
            "color1": torch.tensor(color1_rgb, device=self.device),
            "color2": torch.tensor(color2_rgb, device=self.device)
        }
        
        # Process batch
        batch_size = images.shape[0]
        output = torch.zeros_like(images)
        
        for i in range(batch_size):
            # Calculate luminance
            luminance = 0.299 * images[i, :, :, 0] + 0.587 * images[i, :, :, 1] + 0.114 * images[i, :, :, 2]
            
            # Apply contrast
            luminance = torch.clamp((luminance - 0.5) * contrast + 0.5, 0, 1)
            
            # Get tone masks
            shadows, midtones, highlights = self.apply_tone_mapping(
                luminance, (threshold_low, threshold_high)
            )
            
            # Assign colors based on tone_mapping preference
            color_masks = {
                "Highlights": {"highlights": colors["base"], "midtones": colors["color1"], "shadows": colors["color2"]},
                "Midtones": {"highlights": colors["color1"], "midtones": colors["base"], "shadows": colors["color2"]},
                "Shadows": {"highlights": colors["color1"], "midtones": colors["color2"], "shadows": colors["base"]}
            }[tone_mapping]
            
            # Combine colors with masks
            result = (highlights.unsqueeze(-1) * color_masks["highlights"] +
                     midtones.unsqueeze(-1) * color_masks["midtones"] +
                     shadows.unsqueeze(-1) * color_masks["shadows"])
            
            if preserve_luminance:
                # Preserve original luminance
                result_luminance = 0.299 * result[:, :, 0] + 0.587 * result[:, :, 1] + 0.114 * result[:, :, 2]
                luminance_ratio = luminance / (result_luminance + 1e-6)
                result *= luminance_ratio.unsqueeze(-1)
            
            # Apply saturation
            if saturation != 1.0:
                result_hsv = torch.zeros_like(result)
                result_luminance = 0.299 * result[:, :, 0] + 0.587 * result[:, :, 1] + 0.114 * result[:, :, 2]
                result = torch.lerp(result_luminance.unsqueeze(-1).expand_as(result), result, saturation)
            
            output[i] = result
        
        return (torch.clamp(output, 0, 1),)

NODE_CLASS_MAPPINGS = {
    "ThreeToneStyler": ThreeToneStyler
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ThreeToneStyler": "Three Tone Style Effect"
}