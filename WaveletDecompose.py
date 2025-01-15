import torch
import torch.nn.functional as F
from typing import Tuple, Dict, Any

class WaveletDecompose:
    """
    ComfyUI custom node for performing wavelet decomposition on images.
    Extracts detail scales with proper visualization while preserving reconstruction values.
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
    RETURN_NAMES = ("residual", "scale_1", "scale_2", "scale_3", "scale_4", "original", "scale_5")
    FUNCTION = "decompose"
    CATEGORY = "image/processing"

    def gaussian_kernel(self, kernel_size: int, sigma: float, device: str) -> torch.Tensor:
        """Create 2D Gaussian kernel"""
        x = torch.linspace(-3*sigma, 3*sigma, kernel_size, device=device)
        x = x.view(1, -1).repeat(kernel_size, 1)
        y = x.t()
        kernel = torch.exp(-(x ** 2 + y ** 2) / (2 * sigma ** 2))
        return kernel / kernel.sum()

    def gaussian_blur(self, img: torch.Tensor, kernel_size: int, sigma: float) -> torch.Tensor:
        """Apply Gaussian blur with reflection padding"""
        device = img.device
        
        # Create kernel
        kernel = self.gaussian_kernel(kernel_size, sigma, device)
        kernel = kernel.view(1, 1, kernel_size, kernel_size)
        kernel = kernel.repeat(img.shape[-1], 1, 1, 1)
        
        # Convert image to BCHW format
        img = img.permute(0, 3, 1, 2)
        
        # Apply reflection padding
        pad_size = kernel_size // 2
        img = F.pad(img, (pad_size, pad_size, pad_size, pad_size), mode='reflect')
        
        # Perform convolution
        blurred = F.conv2d(img, kernel, groups=img.shape[1])
        
        # Return to BHWC format
        return blurred.permute(0, 2, 3, 1)

    def normalize_for_display(self, detail: torch.Tensor) -> torch.Tensor:
        """
        Normalize detail coefficients to 0-1 range for display.
        Maps the range [-max(abs), +max(abs)] to [0, 1] with 0.5 being neutral.
        """
        abs_max = torch.abs(detail).max()
        if abs_max == 0:
            return torch.ones_like(detail) * 0.5
        return (detail / (2 * abs_max) + 0.5).clamp(0, 1)

    def decompose(self, image: torch.Tensor, scales: int) -> Tuple[torch.Tensor]:
        """
        Decompose image into frequency bands using Gaussian pyramid.
        
        Args:
            image: Input image tensor (B, H, W, C)
            scales: Number of detail scales to extract
            
        Returns:
            Tuple of tensors containing residual and detail scales
        """
        # Ensure proper type
        device = image.device
        image = image.to(dtype=torch.float32)
        if image.max() > 1.0:
            image = image / 255.0

        outputs = []
        current = image.clone()
        original = image.clone()
        detail_scales = []

        # Process each scale
        for i in range(scales):
            # Calculate blur parameters for this scale
            sigma = 2.0 ** i
            kernel_size = int(sigma * 6) | 1  # Ensure odd
            kernel_size = max(3, kernel_size)
            
            # Apply Gaussian blur
            blurred = self.gaussian_blur(current, kernel_size, sigma)
            
            if i < scales - 1:
                # Extract detail as exact difference
                detail = current - blurred
                
                # Normalize detail for display while preserving values for reconstruction
                detail_display = self.normalize_for_display(detail)
                
                # Store display version
                detail_scales.append(detail_display)
                
                # Update for next iteration
                current = blurred
            else:
                # Last iteration - store residual
                outputs.append(blurred)  # First output is residual

        # Add detail scales in order
        outputs.extend(detail_scales[:5])  # Add first 5 detail scales
        outputs.append(original)  # Add original image at position 5 (zero-based index)
        
        if len(detail_scales) > 5:
            outputs.append(detail_scales[5])  # Add scale_5 as last output if it exists
        else:
            outputs.append(torch.zeros_like(image, device=device))  # Pad with zeros if needed

        # Ensure exactly 7 outputs
        outputs = outputs[:7]

        return tuple(outputs)

NODE_CLASS_MAPPINGS = {
    "WaveletDecompose": WaveletDecompose
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "WaveletDecompose": "Wavelet Decomposition"
}