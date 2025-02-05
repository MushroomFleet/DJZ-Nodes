import torch
import torch.nn.functional as F
from typing import Tuple

class BlackBarsV1:
    """
    ComfyUI custom node that applies letterboxing or pillarboxing to a sequence of images.
    Adds black bars either horizontally (letterbox) or vertically (pillarbox).
    """
    
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "box_mode": (["letterbox", "pillarbox"],),
                "bar_size": ("INT", {
                    "default": 100,
                    "min": 0,
                    "max": 500,
                    "step": 1,
                    "display": "slider"
                }),
                "bar_feather": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 50,
                    "step": 1,
                    "display": "slider",
                    "description": "Softens the edge of the bars"
                })
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_black_bars"
    CATEGORY = "image/format"

    def create_mask(self, height: int, width: int, box_mode: str, 
                   bar_size: int, feather: int) -> torch.Tensor:
        """Creates a mask for the letterbox/pillarbox effect"""
        mask = torch.ones((height, width), device=self.device)
        
        if box_mode == "letterbox":
            # Create horizontal bars
            if bar_size > 0:
                # Top bar
                if feather > 0:
                    for i in range(feather):
                        mask[bar_size - feather + i, :] = i / feather
                mask[:bar_size - feather, :] = 0
                
                # Bottom bar
                if feather > 0:
                    for i in range(feather):
                        mask[height - bar_size + i, :] = i / feather
                mask[height - bar_size + feather:, :] = 0
                
        else:  # pillarbox
            # Create vertical bars
            if bar_size > 0:
                # Left bar
                if feather > 0:
                    for i in range(feather):
                        mask[:, bar_size - feather + i] = i / feather
                mask[:, :bar_size - feather] = 0
                
                # Right bar
                if feather > 0:
                    for i in range(feather):
                        mask[:, width - bar_size + i] = i / feather
                mask[:, width - bar_size + feather:] = 0
        
        return mask

    def apply_black_bars(self, images: torch.Tensor,
                        box_mode: str,
                        bar_size: int,
                        bar_feather: int) -> Tuple[torch.Tensor]:
        """
        Apply letterboxing or pillarboxing effect to a batch of images.
        
        Args:
            images: Input tensor of shape (B, H, W, C)
            box_mode: Either "letterbox" or "pillarbox"
            bar_size: Size of the black bars in pixels
            bar_feather: Size of the feathered edge in pixels
        
        Returns:
            Tuple containing the processed images tensor
        """
        
        # Ensure input is torch tensor on the correct device
        if not isinstance(images, torch.Tensor):
            images = torch.tensor(images, device=self.device)
        else:
            images = images.to(self.device)
        
        # Get dimensions
        B, H, W, C = images.shape
        
        # Create the mask
        mask = self.create_mask(H, W, box_mode, bar_size, bar_feather)
        
        # Expand mask for broadcasting
        mask = mask.unsqueeze(0).unsqueeze(-1).expand(B, -1, -1, C)
        
        # Apply the mask to create the letterbox/pillarbox effect
        result = images * mask
        
        return (result,)

NODE_CLASS_MAPPINGS = {
    "BlackBarsV1": BlackBarsV1
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BlackBarsV1": "Black Bars V1"
}