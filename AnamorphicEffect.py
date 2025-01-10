import torch
import torch.nn.functional as F
import numpy as np

class AnamorphicEffect:
    """
    A ComfyUI custom node that simulates anamorphic lens characteristics including
    oval bokeh, lens flares, and aspect ratio adjustments typical of anamorphic cinematography.
    """
    
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                # Aspect ratio and squeeze
                "squeeze_ratio": ("FLOAT", {
                    "default": 1.33,
                    "min": 1.0,
                    "max": 2.0,
                    "step": 0.01,
                    "display": "slider"
                }),
                # Lens flare controls
                "flare_intensity": ("FLOAT", {
                    "default": 0.3,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.05,
                    "display": "slider"
                }),
                "flare_length": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.1,
                    "max": 1.0,
                    "step": 0.05,
                    "display": "slider"
                }),
                "flare_color": ("FLOAT", {
                    "default": 0.7,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.05,
                    "display": "slider"
                }),
                # Bokeh controls
                "bokeh_amount": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.05,
                    "display": "slider"
                }),
                "bokeh_elliptical": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.05,
                    "display": "slider"
                }),
                # Chromatic aberration
                "chromatic_aberration": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.05,
                    "display": "slider"
                })
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_anamorphic_effect"
    CATEGORY = "image/effects"

    def create_lens_flare(self, image, intensity, length, color):
        """Creates horizontal lens flare effect"""
        B, H, W, C = image.shape
        
        # Create base flare mask
        x = torch.linspace(-1, 1, W)
        y = torch.linspace(-1, 1, H)
        xx, yy = torch.meshgrid(x, y, indexing='xy')
        
        # Create horizontal streaks
        flare = torch.exp(-torch.abs(yy) / 0.1) * torch.exp(-torch.abs(xx) / length)
        flare = flare.to(self.device)
        
        # Adjust color and intensity
        flare = flare.unsqueeze(-1).repeat(1, 1, 3)
        flare = flare * torch.tensor([1.0, color, color]).to(self.device)
        flare = flare * intensity
        
        # Repeat for batch size
        flare = flare.unsqueeze(0).repeat(B, 1, 1, 1)
        
        return torch.clamp(image + flare, 0, 1)

    def apply_chromatic_aberration(self, image, amount):
        """Applies horizontal chromatic aberration"""
        if amount == 0:
            return image
            
        B, H, W, C = image.shape
        
        # Calculate shift amount
        shift = int(W * amount * 0.02)
        if shift == 0:
            return image
            
        # Create padded version of the image
        padded = F.pad(image, (0, 0, shift, shift), mode='replicate')
        
        # Extract shifted channels
        r = padded[..., shift:shift+W, 0:1]  # Shift red right
        g = image[..., 1:2]                  # Green stays centered
        b = padded[..., :W, 2:3]             # Shift blue left
        
        # Combine channels
        return torch.cat([r, g, b], dim=-1)

    def apply_oval_bokeh(self, image, amount, elliptical):
        """Applies oval bokeh blur effect"""
        if amount == 0:
            return image
            
        # Create elliptical kernel
        kernel_size = int(25 * amount)
        if kernel_size % 2 == 0:
            kernel_size += 1
            
        kernel = torch.zeros((kernel_size, kernel_size))
        center = kernel_size // 2
        
        for i in range(kernel_size):
            for j in range(kernel_size):
                x = torch.tensor((i - center) / (kernel_size/2), device=self.device)
                y = torch.tensor((j - center) / (kernel_size/2), device=self.device)
                # Create elliptical distribution
                dist = torch.sqrt(x**2 + (y**2 * (1 + elliptical)))
                if dist <= 1:
                    kernel[i, j] = 1 - dist.item()
                    
        kernel = kernel / kernel.sum()
        kernel = kernel.to(self.device)
        
        # Apply separable blur for efficiency
        blurred = image
        for c in range(3):
            channel = blurred[..., c]
            channel = F.conv2d(
                channel.unsqueeze(1),
                kernel.unsqueeze(0).unsqueeze(0),
                padding=kernel_size//2
            )
            blurred[..., c] = channel.squeeze(1)
            
        return blurred

    def apply_anamorphic_effect(self, images, squeeze_ratio, flare_intensity, 
                              flare_length, flare_color, bokeh_amount,
                              bokeh_elliptical, chromatic_aberration):
        """
        Apply anamorphic effect to a batch of images.
        
        Args:
            images: Input tensor of shape (B, H, W, C)
            squeeze_ratio: Horizontal squeeze factor
            flare_intensity: Intensity of lens flares
            flare_length: Length of lens flares
            flare_color: Color temperature of flares
            bokeh_amount: Amount of bokeh blur
            bokeh_elliptical: How elliptical the bokeh should be
            chromatic_aberration: Amount of color separation
        
        Returns:
            Processed images tensor of shape (B, H, W, C)
        """
        
        # Convert images to torch tensor if needed
        if not isinstance(images, torch.Tensor):
            images = torch.tensor(images)
        images = images.to(self.device)
        
        # Apply horizontal squeeze
        B, H, W, C = images.shape
        squeezed_width = int(W * squeeze_ratio)
        images = F.interpolate(
            images.permute(0, 3, 1, 2),
            size=(H, squeezed_width),
            mode='bilinear',
            align_corners=False
        ).permute(0, 2, 3, 1)
        
        # Apply oval bokeh effect
        images = self.apply_oval_bokeh(images, bokeh_amount, bokeh_elliptical)
        
        # Apply lens flares
        images = self.create_lens_flare(
            images, flare_intensity, flare_length, flare_color
        )
        
        # Apply chromatic aberration
        images = self.apply_chromatic_aberration(images, chromatic_aberration)
        
        # Ensure output is in correct range
        images = torch.clamp(images, 0, 1)
        
        return (images,)

NODE_CLASS_MAPPINGS = {
    "AnamorphicEffect": AnamorphicEffect
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AnamorphicEffect": "Anamorphic Lens Effect"
}