import os
import torch
import numpy as np
from PIL import Image

class djzTiling:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "tiling_mode": (["xy", "x", "y"],),
            }
        }

    RETURN_TYPES = ("MASK",)
    FUNCTION = "generate_tiling_mask"
    CATEGORY = "image/masking"

    def generate_tiling_mask(self, image, tiling_mode):
        # Determine the path to the tilingpresets folder relative to this file
        tiling_presets_folder = os.path.join(os.path.dirname(__file__), "tilingpresets")
        
        # Create the folder if it doesn't exist
        if not os.path.exists(tiling_presets_folder):
            os.makedirs(tiling_presets_folder)
            # Generate default masks if they don't exist (could be done externally)
            self.create_default_masks(tiling_presets_folder)
            
        # Load the appropriate mask based on tiling_mode
        mask_path = os.path.join(tiling_presets_folder, f"{tiling_mode}.png")
        
        # Check if the mask exists
        if not os.path.exists(mask_path):
            print(f"Warning: Mask {mask_path} not found. Creating default mask.")
            self.create_default_masks(tiling_presets_folder)
        
        try:
            # Load the mask
            mask_img = Image.open(mask_path).convert("L")  # Convert to grayscale
            
            # Get dimensions of input image
            _, h, w, _ = image.shape
            
            # Resize mask to match input image dimensions
            mask_img = mask_img.resize((w, h), Image.LANCZOS)
            
            # Convert PIL image to tensor
            mask_np = np.array(mask_img).astype(np.float32) / 255.0
            mask_tensor = torch.from_numpy(mask_np)
            
            # Add batch and channel dimensions to match ComfyUI format
            mask_tensor = mask_tensor.unsqueeze(0).unsqueeze(-1)
            
            return (mask_tensor,)
            
        except Exception as e:
            print(f"Error loading mask: {e}")
            # Return an empty mask
            empty_mask = torch.zeros((1, h, w, 1), dtype=torch.float32)
            return (empty_mask,)
    
    def create_default_masks(self, folder_path):
        """Create default tiling masks if they don't exist"""
        # Create xy tiling mask (circular gradient from center)
        self.create_xy_mask(os.path.join(folder_path, "xy.png"))
        # Create x tiling mask (horizontal gradient from center)
        self.create_x_mask(os.path.join(folder_path, "x.png"))
        # Create y tiling mask (vertical gradient from center)
        self.create_y_mask(os.path.join(folder_path, "y.png"))
    
    def create_xy_mask(self, file_path):
        """Create circular gradient mask for XY tiling"""
        size = 1024
        mask = Image.new("L", (size, size), 0)
        
        # Create a circular gradient
        center_x, center_y = size // 2, size // 2
        max_radius = min(center_x, center_y)
        
        for y in range(size):
            for x in range(size):
                # Calculate distance from center
                dx = abs(x - center_x)
                dy = abs(y - center_y)
                distance = (dx**2 + dy**2)**0.5
                
                # Normalize distance and invert (farther = darker)
                value = max(0, min(255, int(255 * (1 - distance / max_radius))))
                
                # Set pixel value
                mask.putpixel((x, y), value)
        
        mask.save(file_path)
    
    def create_x_mask(self, file_path):
        """Create horizontal gradient mask for X tiling"""
        size = 1024
        mask = Image.new("L", (size, size), 0)
        
        center_x = size // 2
        max_distance = center_x
        
        for y in range(size):
            for x in range(size):
                # Calculate horizontal distance from center
                dx = abs(x - center_x)
                
                # Normalize distance and invert
                value = max(0, min(255, int(255 * (1 - dx / max_distance))))
                
                # Set pixel value
                mask.putpixel((x, y), value)
        
        mask.save(file_path)
    
    def create_y_mask(self, file_path):
        """Create vertical gradient mask for Y tiling"""
        size = 1024
        mask = Image.new("L", (size, size), 0)
        
        center_y = size // 2
        max_distance = center_y
        
        for y in range(size):
            for x in range(size):
                # Calculate vertical distance from center
                dy = abs(y - center_y)
                
                # Normalize distance and invert
                value = max(0, min(255, int(255 * (1 - dy / max_distance))))
                
                # Set pixel value
                mask.putpixel((x, y), value)
        
        mask.save(file_path)

NODE_CLASS_MAPPINGS = {
    "djzTiling": djzTiling
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "djzTiling": "djz Tiling"
}
