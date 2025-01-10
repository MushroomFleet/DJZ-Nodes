import torch
import torch.nn.functional as F
import numpy as np
from typing import Tuple

class PanavisionLensV2:
    """
    Enhanced ComfyUI custom node that simulates sophisticated Panavision lens characteristics
    including advanced bokeh modeling, multi-layer flares, chromatic effects, and film-like
    color science.
    """
    
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                # Lens Format
                "aspect_ratio": ("FLOAT", {
                    "default": 2.39,
                    "min": 1.85,
                    "max": 2.76,
                    "step": 0.01,
                    "display": "slider"
                }),
                "anamorphic_squeeze": ("FLOAT", {
                    "default": 2.0,
                    "min": 1.0,
                    "max": 2.4,
                    "step": 0.1,
                    "display": "slider"
                }),
                # Bokeh Characteristics
                "bokeh_intensity": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.05,
                    "display": "slider"
                }),
                "bokeh_threshold": ("FLOAT", {
                    "default": 0.8,
                    "min": 0.5,
                    "max": 1.0,
                    "step": 0.05,
                    "display": "slider"
                }),
                "bokeh_elongation": ("FLOAT", {
                    "default": 2.0,
                    "min": 1.0,
                    "max": 3.0,
                    "step": 0.1,
                    "display": "slider"
                }),
                "bokeh_rotation": ("FLOAT", {
                    "default": 0.0,
                    "min": -45.0,
                    "max": 45.0,
                    "step": 1.0,
                    "display": "slider"
                }),
                # Lens Flare System
                "primary_flare_intensity": ("FLOAT", {
                    "default": 0.4,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.05,
                    "display": "slider"
                }),
                "secondary_flare_intensity": ("FLOAT", {
                    "default": 0.2,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.05,
                    "display": "slider"
                }),
                "flare_position_y": ("FLOAT", {
                    "default": 0.0,
                    "min": -1.0,
                    "max": 1.0,
                    "step": 0.1,
                    "display": "slider"
                }),
                "flare_stretch": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.5,
                    "max": 2.0,
                    "step": 0.1,
                    "display": "slider"
                }),
                # Color Science
                "highlight_retention": ("FLOAT", {
                    "default": 0.8,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.05,
                    "display": "slider"
                }),
                "shadow_rolloff": ("FLOAT", {
                    "default": 0.3,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.05,
                    "display": "slider"
                }),
                "blacks_crush": ("FLOAT", {
                    "default": 0.1,
                    "min": 0.0,
                    "max": 0.5,
                    "step": 0.05,
                    "display": "slider"
                }),
                # Color Temperature
                "highlight_warmth": ("FLOAT", {
                    "default": 0.2,
                    "min": -0.5,
                    "max": 0.5,
                    "step": 0.05,
                    "display": "slider"
                }),
                "midtone_warmth": ("FLOAT", {
                    "default": 0.1,
                    "min": -0.5,
                    "max": 0.5,
                    "step": 0.05,
                    "display": "slider"
                }),
                "shadow_coolness": ("FLOAT", {
                    "default": 0.15,
                    "min": -0.5,
                    "max": 0.5,
                    "step": 0.05,
                    "display": "slider"
                }),
                # Aberration and Distortion
                "chromatic_aberration": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.05,
                    "display": "slider"
                }),
                "barrel_distortion": ("FLOAT", {
                    "default": 0.0,
                    "min": -0.5,
                    "max": 0.5,
                    "step": 0.05,
                    "display": "slider"
                })
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_panavision_effect"
    CATEGORY = "image/effects"

    def create_complex_flare_system(self, image: torch.Tensor, 
                                  primary_intensity: float,
                                  secondary_intensity: float,
                                  position_y: float,
                                  stretch: float) -> torch.Tensor:
        """Creates a sophisticated multi-layer lens flare system"""
        B, H, W, C = image.shape
        
        # Create base coordinate system
        x = torch.linspace(-1, 1, W, device=self.device)
        y = torch.linspace(-1, 1, H, device=self.device)
        xx, yy = torch.meshgrid(x, y, indexing='xy')
        
        # Adjust vertical position
        yy = yy - position_y
        
        # Primary flare (warm, centered)
        primary_mask = torch.exp(-torch.abs(yy) / (0.1 * stretch)) * \
                      torch.exp(-torch.abs(xx) / (0.3 * stretch))
        
        # Secondary flares (cooler, offset)
        flare_positions = torch.tensor([-0.4, 0.4], device=self.device)
        secondary_mask = torch.zeros((H, W), device=self.device)
        
        for pos in flare_positions:
            streak = torch.exp(-torch.abs(yy - pos*stretch) / 0.05) * \
                    torch.exp(-torch.abs(xx) / (0.2 * stretch))
            secondary_mask = secondary_mask + streak
        
        # Create color variations
        primary_flare = torch.stack([
            primary_mask,
            primary_mask * 0.7,
            primary_mask * 0.3
        ], dim=-1) * primary_intensity
        
        secondary_flare = torch.stack([
            secondary_mask * 0.3,
            secondary_mask * 0.6,
            secondary_mask
        ], dim=-1) * secondary_intensity
        
        # Add subtle color noise for organic feel
        noise = torch.randn((H, W, C), device=self.device) * 0.02
        combined_flare = primary_flare + secondary_flare + noise
        
        # Repeat for batch size
        combined_flare = combined_flare.unsqueeze(0).repeat(B, 1, 1, 1)
        
        return torch.clamp(image + combined_flare, 0, 1)

    def apply_advanced_bokeh(self, image: torch.Tensor,
                           intensity: float,
                           threshold: float,
                           elongation: float,
                           rotation: float) -> torch.Tensor:
        """Applies sophisticated bokeh effect with rotation and elongation control"""
        if intensity == 0:
            return image
            
        # Create rotatable oval kernel
        kernel_size = int(25 * intensity)
        if kernel_size % 2 == 0:
            kernel_size += 1
            
        kernel = torch.zeros((kernel_size, kernel_size), device=self.device)
        center = kernel_size // 2
        
        # Convert rotation to radians
        rot_rad = torch.tensor(rotation * np.pi / 180.0, device=self.device)
        cos_rot = torch.cos(rot_rad)
        sin_rot = torch.sin(rot_rad)
        
        for i in range(kernel_size):
            for j in range(kernel_size):
                # Center and normalize coordinates
                x = (i - center) / (kernel_size/2)
                y = (j - center) / (kernel_size/2)
                
                # Apply rotation
                x_rot = x * cos_rot - y * sin_rot
                y_rot = x * sin_rot + y * cos_rot
                
                # Apply elongation
                y_rot = y_rot * elongation
                
                # Calculate distance and apply kernel
                dist = torch.sqrt(x_rot**2 + y_rot**2)
                if dist <= 1:
                    # Smooth falloff
                    kernel[i, j] = torch.cos(dist * np.pi/2).item()
                    
        kernel = kernel / kernel.sum()
        
        # Create mask for bright areas with smooth transition
        luminance = 0.2989 * image[..., 0] + 0.5870 * image[..., 1] + 0.1140 * image[..., 2]
        bright_mask = torch.sigmoid((luminance - threshold) * 10)
        
        # Apply masked blur with edge preservation
        blurred = image.clone()
        for c in range(3):
            channel = image[..., c]
            blurred_channel = F.conv2d(
                channel.unsqueeze(1),
                kernel.unsqueeze(0).unsqueeze(0),
                padding=kernel_size//2
            ).squeeze(1)
            
            # Edge-aware blending
            edge_mask = torch.abs(blurred_channel - channel) < 0.1
            blurred[..., c] = channel * (1 - bright_mask * edge_mask) + \
                             blurred_channel * (bright_mask * edge_mask)
            
        return blurred

    def apply_color_science(self, image: torch.Tensor,
                          highlight_retention: float,
                          shadow_rolloff: float,
                          blacks_crush: float) -> torch.Tensor:
        """Applies sophisticated color science adjustments"""
        # Calculate luminance
        luminance = 0.2989 * image[..., 0] + 0.5870 * image[..., 1] + 0.1140 * image[..., 2]
        
        # Highlight retention curve
        highlights = torch.pow(luminance, 1.0 / (1.0 + highlight_retention))
        
        # Shadow rolloff curve
        shadows = torch.pow(luminance, 1.0 + shadow_rolloff)
        
        # Combine curves with smooth transition
        alpha = torch.sigmoid((luminance - 0.5) * 4)
        combined_curve = alpha * highlights + (1 - alpha) * shadows
        
        # Apply blacks crush
        combined_curve = torch.max(combined_curve - blacks_crush, torch.zeros_like(combined_curve))
        
        # Apply curve while preserving color ratios
        result = torch.zeros_like(image)
        for c in range(3):
            color_ratio = torch.where(luminance > 0.001, 
                                    image[..., c] / (luminance + 0.001),
                                    torch.ones_like(luminance))
            result[..., c] = color_ratio * combined_curve
            
        return torch.clamp(result, 0, 1)

    def apply_advanced_color_temperature(self, image: torch.Tensor,
                                      highlight_warmth: float,
                                      midtone_warmth: float,
                                      shadow_coolness: float) -> torch.Tensor:
        """Applies sophisticated color temperature adjustments across tonal ranges"""
        # Calculate luminance
        luminance = 0.2989 * image[..., 0] + 0.5870 * image[..., 1] + 0.1140 * image[..., 2]
        
        # Create tonal range masks
        highlight_mask = torch.sigmoid((luminance - 0.7) * 10)
        midtone_mask = torch.exp(-(luminance - 0.5)**2 / 0.1)
        shadow_mask = torch.sigmoid((0.3 - luminance) * 10)
        
        # Create color adjustment tensors
        highlight_adjust = torch.zeros_like(image)
        highlight_adjust[..., 0] = highlight_warmth  # Red
        highlight_adjust[..., 1] = highlight_warmth * 0.6  # Green
        
        midtone_adjust = torch.zeros_like(image)
        midtone_adjust[..., 0] = midtone_warmth
        midtone_adjust[..., 1] = midtone_warmth * 0.7
        
        shadow_adjust = torch.zeros_like(image)
        shadow_adjust[..., 2] = shadow_coolness  # Blue
        
        # Apply adjustments with masks
        result = image.clone()
        result += (highlight_adjust * highlight_mask.unsqueeze(-1))
        result += (midtone_adjust * midtone_mask.unsqueeze(-1))
        result += (shadow_adjust * shadow_mask.unsqueeze(-1))
        
        return torch.clamp(result, 0, 1)

    def apply_lens_distortion(self, image: torch.Tensor,
                            chromatic_aberration: float,
                            barrel_distortion: float) -> torch.Tensor:
        """Applies chromatic aberration and barrel distortion"""
        if chromatic_aberration == 0 and barrel_distortion == 0:
            return image
            
        B, H, W, C = image.shape
        
        # Create normalized coordinate grid
        x = torch.linspace(-1, 1, W, device=self.device)
        y = torch.linspace(-1, 1, H, device=self.device)
        xx, yy = torch.meshgrid(x, y, indexing='xy')
        
        # Calculate radial distance
        r = torch.sqrt(xx**2 + yy**2)
        
        # Apply barrel/pincushion distortion
        if barrel_distortion != 0:
            factor = 1 + barrel_distortion * r**2
            xx_distorted = xx * factor
            yy_distorted = yy * factor
        else:
            xx_distorted = xx
            yy_distorted = yy
        
        # Convert to pixel coordinates
        xx_pixels = ((xx_distorted + 1) * (W - 1)) / 2
        yy_pixels = ((yy_distorted + 1) * (H - 1)) / 2
        
        # Create sampling grid
        grid = torch.stack([xx_pixels, yy_pixels], dim=-1)
        grid = grid.unsqueeze(0).expand(B, -1, -1, -1)
        
        # Apply chromatic aberration
        result = torch.zeros_like(image)
        if chromatic_aberration > 0:
            # Shift red channel outward
            red_grid = grid * (1 + chromatic_aberration * 0.02)
            # Shift blue channel inward
            blue_grid = grid * (1 - chromatic_aberration * 0.02)
            
            # Sample each color channel with its own displacement
            result[..., 0] = F.grid_sample(
                image[..., 0].unsqueeze(1), 
                red_grid.to(self.device), 
                mode='bilinear', 
                padding_mode='border'
            ).squeeze(1)
            
            result[..., 1] = F.grid_sample(
                image[..., 1].unsqueeze(1), 
                grid.to(self.device), 
                mode='bilinear', 
                padding_mode='border'
            ).squeeze(1)
            
            result[..., 2] = F.grid_sample(
                image[..., 2].unsqueeze(1), 
                blue_grid.to(self.device), 
                mode='bilinear', 
                padding_mode='border'
            ).squeeze(1)
        else:
            # Without chromatic aberration, just apply the barrel distortion
            result = F.grid_sample(
                image.permute(0, 3, 1, 2), 
                grid.to(self.device), 
                mode='bilinear', 
                padding_mode='border'
            ).permute(0, 2, 3, 1)
            
        return torch.clamp(result, 0, 1)

    def apply_panavision_effect(self, images: torch.Tensor,
                              aspect_ratio: float,
                              anamorphic_squeeze: float,
                              bokeh_intensity: float,
                              bokeh_threshold: float,
                              bokeh_elongation: float,
                              bokeh_rotation: float,
                              primary_flare_intensity: float,
                              secondary_flare_intensity: float,
                              flare_position_y: float,
                              flare_stretch: float,
                              highlight_retention: float,
                              shadow_rolloff: float,
                              blacks_crush: float,
                              highlight_warmth: float,
                              midtone_warmth: float,
                              shadow_coolness: float,
                              chromatic_aberration: float,
                              barrel_distortion: float) -> Tuple[torch.Tensor]:
        """
        Apply complete Panavision lens simulation effect to a batch of images.
        
        Args:
            images: Input tensor of shape (B, H, W, C)
            [various effect parameters as described in INPUT_TYPES]
        
        Returns:
            Tuple containing the processed images tensor
        """
        
        # Ensure input is torch tensor on the correct device
        if not isinstance(images, torch.Tensor):
            images = torch.tensor(images, device=self.device)
        else:
            images = images.to(self.device)
        
        # Store original dimensions
        B, H, W, C = images.shape
        
        # Apply anamorphic squeeze
        if anamorphic_squeeze != 1.0:
            squeezed_width = int(W * anamorphic_squeeze)
            images = F.interpolate(
                images.permute(0, 3, 1, 2),
                size=(H, squeezed_width),
                mode='bilinear',
                align_corners=False
            ).permute(0, 2, 3, 1)
        
        # Apply lens distortions first
        images = self.apply_lens_distortion(
            images, chromatic_aberration, barrel_distortion
        )
        
        # Apply bokeh effect
        images = self.apply_advanced_bokeh(
            images, bokeh_intensity, bokeh_threshold,
            bokeh_elongation, bokeh_rotation
        )
        
        # Apply lens flares
        images = self.create_complex_flare_system(
            images, primary_flare_intensity,
            secondary_flare_intensity, flare_position_y,
            flare_stretch
        )
        
        # Apply color science
        images = self.apply_color_science(
            images, highlight_retention,
            shadow_rolloff, blacks_crush
        )
        
        # Apply color temperature adjustments
        images = self.apply_advanced_color_temperature(
            images, highlight_warmth,
            midtone_warmth, shadow_coolness
        )
        
        # Final aspect ratio adjustment
        current_ratio = W / H
        if current_ratio != aspect_ratio:
            new_width = int(H * aspect_ratio)
            images = F.interpolate(
                images.permute(0, 3, 1, 2),
                size=(H, new_width),
                mode='bilinear',
                align_corners=False
            ).permute(0, 2, 3, 1)
        
        return (torch.clamp(images, 0, 1),)

NODE_CLASS_MAPPINGS = {
    "PanavisionLensV2": PanavisionLensV2
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PanavisionLensV2": "Panavision Lens Effect v2"
}