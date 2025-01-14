import torch
import torch.nn.functional as F
import numpy as np
from typing import Tuple, Dict, Any

class WaveletDecompose:
    """
    ComfyUI custom node for performing Photoshop-style wavelet decomposition on images.
    Uses Gaussian blur and blend operations to create detail scales.
    """
    
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
    
    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Any]:
        return {
            "required": {
                "image": ("IMAGE",),
                "scales": ("INT", {
                    "default": 5,
                    "min": 1,
                    "max": 10,
                    "step": 1,
                    "display": "number"
                })
            }
        }

    RETURN_TYPES = ("IMAGE", "IMAGE", "IMAGE", "IMAGE", "IMAGE", "IMAGE", "IMAGE")
    RETURN_NAMES = ("residual", "scale_1", "scale_2", "scale_3", "scale_4", "scale_5", "original")
    FUNCTION = "decompose"
    CATEGORY = "image/processing"

    def gaussian_kernel(self, kernel_size: int, sigma: float, device: str) -> torch.Tensor:
        """Create 2D Gaussian kernel"""
        x = torch.linspace(-sigma, sigma, kernel_size, device=device)
        x = x.view(1, -1).repeat(kernel_size, 1)
        y = x.t()
        kernel = torch.exp(-(x ** 2 + y ** 2) / (2 * sigma ** 2))
        return kernel / kernel.sum()

    def gaussian_blur(self, img: torch.Tensor, kernel_size: int, sigma: float) -> torch.Tensor:
        """Apply Gaussian blur to image"""
        # Ensure image is on the correct device
        device = img.device
        
        # Create kernel for each channel
        kernel = self.gaussian_kernel(kernel_size, sigma, device)
        kernel = kernel.view(1, 1, kernel_size, kernel_size)
        kernel = kernel.repeat(img.shape[-1], 1, 1, 1)
        
        # Prepare image for convolution
        img = img.permute(0, 3, 1, 2)  # BCHW
        
        # Apply padding
        pad_size = kernel_size // 2
        img = F.pad(img, (pad_size, pad_size, pad_size, pad_size), mode='reflect')
        
        # Apply convolution for each channel
        blurred = F.conv2d(img, kernel, groups=img.shape[1])
        
        return blurred.permute(0, 2, 3, 1)  # Back to BHWC

    def linear_light_blend(self, top: torch.Tensor, bottom: torch.Tensor) -> torch.Tensor:
        """Apply linear light blend mode"""
        return torch.clamp(2 * top + 2 * bottom - 1, 0, 1)

    def decompose(self, image: torch.Tensor, scales: int) -> Tuple[torch.Tensor, ...]:
        """
        Perform Photoshop-style wavelet decomposition on the input image.
        
        Args:
            image: Input image tensor (B, H, W, C)
            scales: Number of detail scales to extract
            
        Returns:
            Tuple of tensors containing residual and detail scales
        """
        # Move image to appropriate device and ensure float type
        device = image.device
        image = image.to(device, dtype=torch.float32)
        if image.max() > 1.0:
            image = image / 255.0

        outputs = []
        current = image
        original = image.clone()

        # Process each scale
        for i in range(scales):
            # Calculate blur radius based on scale
            blur_radius = 2.0 ** i - 0.5
            kernel_size = int(blur_radius * 6) | 1  # Ensure odd kernel size
            kernel_size = max(3, kernel_size)
            
            # Create blurred version
            blurred = self.gaussian_blur(current, kernel_size, blur_radius)
            
            if i < scales - 1:
                # Calculate detail layer (original - blur)
                detail = (current - blurred + 0.5).clamp(0, 1)
                outputs.append(detail)
                
                # Update current for next iteration
                current = blurred
            else:
                # Last iteration - this is our residual
                residual = blurred
                outputs.insert(0, residual)  # Residual goes first

        # Add original image as last output
        outputs.append(original)

        # Pad with zeros if we need more outputs
        while len(outputs) < 7:
            outputs.append(torch.zeros_like(image, device=device))

        # Ensure we only return 7 outputs
        outputs = outputs[:7]

        # Ensure all outputs are on the correct device
        outputs = [x.to(device) for x in outputs]

        return tuple(outputs)

NODE_CLASS_MAPPINGS = {
    "WaveletDecompose": WaveletDecompose
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "WaveletDecompose": "Wavelet Decomposition (Photoshop Style)"
}