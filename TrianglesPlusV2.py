"""
@author: DJZ-Nodes
Triangles Plus V2 Generator - A node that generates abstract art using triangles with enhanced customization
"""

from PIL import Image, ImageDraw
import random
import numpy as np
import torch

class TrianglesPlusV2:
    """A ComfyUI node that generates abstract art using triangles with enhanced customization"""
    
    # Color palettes inspired by DinskyPlusV2
    COLOR_PALETTES = {
        "kandinsky": ['#69D2E7', '#A7DBD8', '#E0E4CC', '#F38630', '#FA6900', '#FF4E50', '#F9D423'],
        "warm": ['#FF4E50', '#FC913A', '#F9D423', '#EDE574', '#E1F5C4'],
        "cool": ['#69D2E7', '#A7DBD8', '#E0E4CC', '#B2C2C1', '#8AB8B2'],
        "monochrome": ['#FFFFFF', '#D9D9D9', '#BFBFBF', '#8C8C8C', '#404040'],
        "vibrant": ['#FF1E1E', '#FF9900', '#FFFF00', '#00FF00', '#0000FF', '#9900FF']
    }

    # Shape size presets (multipliers for width/height divisions)
    SIZE_PRESETS = {
        "small": 0.5,
        "medium": 1.0,
        "large": 2.0
    }

    # Count presets (number of triangles)
    COUNT_PRESETS = {
        "sparse": 4,
        "medium": 7,
        "dense": 12
    }
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "width": ("INT", {"default": 1024, "min": 64, "max": 4096}),
                "height": ("INT", {"default": 1024, "min": 64, "max": 4096}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 4294967295}),
                "background_color": ("STRING", {"default": "#000000"}),
                "color_palette": (list(s.COLOR_PALETTES.keys()),),
                "size_preset": (list(s.SIZE_PRESETS.keys()),),
                "count_preset": (list(s.COUNT_PRESETS.keys()),),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate_art"
    CATEGORY = "DJZ-Nodes"

    def hex_to_rgb(self, hex_color):
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def generate_art(self, width, height, seed, background_color, color_palette, size_preset, count_preset):
        # Set random seed for reproducibility
        seed = seed % (2**32)
        random.seed(seed)
        np.random.seed(seed)

        # Create new image with specified background color
        image = Image.new("RGB", (width, height), self.hex_to_rgb(background_color))
        draw = ImageDraw.Draw(image)

        # Get size multiplier from preset
        size_multiplier = self.SIZE_PRESETS[size_preset]
        
        # Get number of triangles from count preset
        num_triangles = self.COUNT_PRESETS[count_preset]

        def generate_triangle_points(size_mult):
            """Generate points for a single triangle with size multiplier"""
            section_w = width // 4
            section_h = height // 4
            
            # Adjust section size based on multiplier
            adj_w = int(section_w * size_mult)
            adj_h = int(section_h * size_mult)
            
            # Random position for triangle
            x = random.randint(0, width - adj_w)
            y = random.randint(0, height - adj_h)
            
            return [
                (x + random.randint(0, adj_w), y + random.randint(0, adj_h)),
                (x + random.randint(0, adj_w), y + random.randint(0, adj_h)),
                (x + random.randint(0, adj_w), y + random.randint(0, adj_h))
            ]

        # Get colors from selected palette
        palette_colors = [color for color in self.COLOR_PALETTES[color_palette]]
        
        # Generate and draw triangles
        for _ in range(num_triangles):
            points = generate_triangle_points(size_multiplier)
            color = random.choice(palette_colors)
            draw.polygon(points, fill=color)

        # Convert PIL image to tensor in the format ComfyUI expects (B,H,W,C)
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
    "TrianglesPlusV2": TrianglesPlusV2
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TrianglesPlusV2": "Triangles Plus V2 Generator"
}
