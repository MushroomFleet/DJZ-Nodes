import os
import torch
import numpy as np
from PIL import Image, ImageFilter

class djzTilingV2:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "tiling_mode": (["xy", "x", "y"],),
                "feathering_strength": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 5.0,
                    "step": 0.1
                }),
                "feathering_curve": (["linear", "exponential", "sinusoidal", "quadratic"],),
                "invert_mask": ("BOOLEAN", {"default": False}),
                "inner_radius_percent": ("FLOAT", {
                    "default": 50.0,
                    "min": 1.0,
                    "max": 100.0,
                    "step": 1.0
                }),
                "preview_mask": ("BOOLEAN", {"default": False})
            }
        }

    RETURN_TYPES = ("MASK", "IMAGE")
    RETURN_NAMES = ("mask", "preview")
    FUNCTION = "generate_tiling_mask"
    CATEGORY = "image/masking"
    
    def apply_feathering_curve(self, normalized_distance, curve_type, strength):
        """Apply different feathering curves to the normalized distance"""
        # Adjust the effect of strength (higher = more affected)
        if curve_type == "linear":
            # Linear falloff (default)
            result = normalized_distance ** strength
        elif curve_type == "exponential":
            # Exponential falloff (sharper transition at edges)
            result = np.exp((normalized_distance - 1) * strength)
        elif curve_type == "sinusoidal":
            # Sinusoidal falloff (smoother, wave-like)
            result = 0.5 * (1 + np.cos(np.pi * (1 - normalized_distance ** strength)))
        elif curve_type == "quadratic":
            # Quadratic falloff (more gradual near center, quicker at edges)
            result = 1 - (1 - normalized_distance) ** (2 * strength)
        else:
            # Default to linear if unknown
            result = normalized_distance
            
        # Ensure result is in [0, 1] range
        return np.clip(result, 0, 1)

    def generate_tiling_mask(self, image, tiling_mode, feathering_strength=1.0, 
                            feathering_curve="linear", invert_mask=False, 
                            inner_radius_percent=50.0, preview_mask=False):
        # Get dimensions of input image
        _, h, w, _ = image.shape
        
        # Calculate normalized center coordinates
        center_x, center_y = w // 2, h // 2
        
        # Calculate maximum distance based on image dimensions
        if tiling_mode == "xy":
            max_distance = min(center_x, center_y)
        elif tiling_mode == "x":
            max_distance = center_x
        else:  # y mode
            max_distance = center_y
        
        # Calculate inner radius (area that stays unaffected)
        inner_radius = max_distance * (inner_radius_percent / 100.0)
        
        # Create mask array
        mask_array = np.zeros((h, w), dtype=np.float32)
        
        # Generate mask based on tiling mode
        for y in range(h):
            for x in range(w):
                # Calculate distance based on tiling mode
                if tiling_mode == "xy":
                    # Distance from center for xy tiling
                    dx = abs(x - center_x)
                    dy = abs(y - center_y)
                    distance = (dx**2 + dy**2)**0.5
                elif tiling_mode == "x":
                    # Horizontal distance for x tiling
                    distance = abs(x - center_x)
                elif tiling_mode == "y":
                    # Vertical distance for y tiling
                    distance = abs(y - center_y)
                
                # Apply inner radius - anything inside remains at full strength
                if distance <= inner_radius:
                    normalized_distance = 0.0
                else:
                    # Normalize distance to 0-1 range, but only for the area outside inner_radius
                    # This creates a feathered edge only in the outer region
                    normalized_distance = (distance - inner_radius) / (max_distance - inner_radius)
                    normalized_distance = min(1.0, normalized_distance)  # Cap at 1.0
                
                # Apply feathering curve
                value = self.apply_feathering_curve(normalized_distance, feathering_curve, feathering_strength)
                
                # Set pixel value (0 = fully masked, 1 = unmasked)
                mask_array[y, x] = 1.0 - value  # Invert since 0 is usually masked in inpainting
        
        # Invert mask if requested
        if invert_mask:
            mask_array = 1.0 - mask_array
            
        # Convert numpy array to tensor
        mask_tensor = torch.from_numpy(mask_array)
        
        # Add batch and channel dimensions to match ComfyUI format
        mask_tensor = mask_tensor.unsqueeze(0).unsqueeze(-1)
        
        # Create preview image (RGB visualization of mask)
        if preview_mask:
            # Convert mask to RGB for preview
            mask_rgb = np.stack([mask_array] * 3, axis=-1)
            mask_rgb_tensor = torch.from_numpy(mask_rgb).unsqueeze(0)
        else:
            # Just return the input image as preview if preview not requested
            mask_rgb_tensor = image.clone()
        
        return (mask_tensor, mask_rgb_tensor)

    @classmethod
    def IS_CHANGED(cls, image, tiling_mode, feathering_strength, feathering_curve, 
                  invert_mask, inner_radius_percent, preview_mask):
        # This ensures the node updates when any parameter changes
        return (tiling_mode, feathering_strength, feathering_curve, 
                invert_mask, inner_radius_percent, preview_mask)

NODE_CLASS_MAPPINGS = {
    "djzTilingV2": djzTilingV2
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "djzTilingV2": "DJZ Tiling V2"
}
