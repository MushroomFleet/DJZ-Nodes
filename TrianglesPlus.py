"""
@author: DJZ-Nodes
Triangles Plus Generator - A node that generates abstract art using triangles
"""

from PIL import Image, ImageDraw
import random
import numpy as np
import torch

class TrianglesPlus:
    """A ComfyUI node that generates abstract art using triangles"""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "width": ("INT", {"default": 1024, "min": 64, "max": 4096}),
                "height": ("INT", {"default": 1024, "min": 64, "max": 4096}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 4294967295}),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate_art"
    CATEGORY = "DJZ-Nodes"

    def generate_art(self, width, height, seed):
        # Set random seed for reproducibility
        # Ensure seed is within numpy's valid range
        seed = seed % (2**32)
        random.seed(seed)
        np.random.seed(seed)

        # Create new image
        image = Image.new("RGB", (width, height))
        draw = ImageDraw.Draw(image)

        # Generate variations in segment points based on the seed
        def generate_segment_points():
            return [
                [(random.randint(0, width // 4), random.randint(0, height // 4)),
                 (random.randint(width // 4, width // 2), random.randint(0, height // 4)),
                 (random.randint(width // 8, width * 3 // 8), random.randint(height // 8, height * 3 // 8))],
                [(random.randint(width // 2, width * 3 // 4), random.randint(0, height // 4)),
                 (random.randint(width * 3 // 4, width), random.randint(0, height // 4)),
                 (random.randint(width * 5 // 8, width * 7 // 8), random.randint(height // 8, height * 3 // 8))],
                [(random.randint(0, width // 4), random.randint(height * 3 // 4, height)),
                 (random.randint(width // 4, width // 2), random.randint(height * 3 // 4, height)),
                 (random.randint(width // 8, width * 3 // 8), random.randint(height * 5 // 8, height * 7 // 8))],
                [(random.randint(width // 2, width * 3 // 4), random.randint(height * 3 // 4, height)),
                 (random.randint(width * 3 // 4, width), random.randint(height * 3 // 4, height)),
                 (random.randint(width * 5 // 8, width * 7 // 8), random.randint(height * 5 // 8, height * 7 // 8))],
                [(random.randint(0, width // 2), random.randint(height // 4, height * 3 // 4)),
                 (random.randint(width // 2, width), random.randint(height // 4, height * 3 // 4)),
                 (random.randint(width // 4, width * 3 // 4), random.randint(height // 8, height // 4))],
                [(random.randint(width // 8, width // 4), random.randint(0, height)),
                 (random.randint(width // 8, width // 4), random.randint(0, height)),
                 (random.randint(0, width // 8), random.randint(height // 4, height * 3 // 4))],
                [(random.randint(width * 3 // 4, width * 7 // 8), random.randint(0, height)),
                 (random.randint(width * 3 // 4, width * 7 // 8), random.randint(0, height)),
                 (random.randint(width * 7 // 8, width), random.randint(height // 4, height * 3 // 4))]
            ]

        points = generate_segment_points()

        # Define colors with the same seed
        colors = [
            (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(7)
        ]

        # Draw each segment with a different color
        for i, point_set in enumerate(points):
            draw.polygon(point_set, fill=colors[i])

        # Convert PIL image to tensor in the format ComfyUI expects (B,H,W,C)
        # Convert to RGB if not already
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Convert to numpy array and normalize to 0-1 range
        image_np = np.array(image).astype(np.float32) / 255.0
        
        # Convert to PyTorch tensor
        image_tensor = torch.from_numpy(image_np)
        
        # Ensure shape is (B,H,W,C)
        if len(image_tensor.shape) == 3:
            image_tensor = image_tensor.unsqueeze(0)
        
        return (image_tensor,)

# Node registration for ComfyUI
NODE_CLASS_MAPPINGS = {
    "TrianglesPlus": TrianglesPlus
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TrianglesPlus": "Triangles Plus Generator"
}
