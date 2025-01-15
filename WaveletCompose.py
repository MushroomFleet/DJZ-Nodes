import torch
from typing import Tuple, Dict, Any

class WaveletCompose:
    """
    ComfyUI custom node for reconstructing an image from wavelet decomposition scales.
    Handles denormalized detail coefficients to reconstruct the original image.
    """
    
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
    
    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Any]:
        return {
            "required": {
                "residual": ("IMAGE",),
                "scale_1": ("IMAGE",),
                "scale_2": ("IMAGE",),
                "scale_3": ("IMAGE",),
                "scale_4": ("IMAGE",),
                "scale_5": ("IMAGE",)
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("composed_image",)
    FUNCTION = "compose"
    CATEGORY = "image/processing"

    def denormalize_detail(self, detail: torch.Tensor) -> torch.Tensor:
        """
        Convert normalized detail coefficients back to difference space.
        Maps [0, 1] range back to [-max(abs), +max(abs)] range.
        """
        return (detail - 0.5) * 2

    def compose(self,
               residual: torch.Tensor,
               scale_1: torch.Tensor,
               scale_2: torch.Tensor,
               scale_3: torch.Tensor,
               scale_4: torch.Tensor,
               scale_5: torch.Tensor) -> Tuple[torch.Tensor]:
        """
        Reconstruct image by combining wavelet scales.
        
        Args:
            residual: Base residual layer (most blurred)
            scale_1-5: Detail scales containing display-normalized differences
            
        Returns:
            Reconstructed image tensor
        """
        # Ensure all inputs are on the same device and type
        device = residual.device
        dtype = torch.float32
        
        # Convert inputs to proper type
        layers = [residual, scale_1, scale_2, scale_3, scale_4, scale_5]
        layers = [layer.to(device, dtype=dtype) for layer in layers]
        
        # Normalize value ranges if needed
        layers = [layer / 255.0 if layer.max() > 1.0 else layer for layer in layers]
        
        # Start with residual
        result = layers[0]
        
        # Add each denormalized detail scale
        for i, layer in enumerate(layers[1:], 1):
            if layer is not None and not torch.all(layer == 0):
                detail = self.denormalize_detail(layer)
                result = result + detail
        
        # Ensure output is in valid range
        result = result.clamp(0, 1)
        
        return (result,)

NODE_CLASS_MAPPINGS = {
    "WaveletCompose": WaveletCompose
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "WaveletCompose": "Wavelet Composition"
}