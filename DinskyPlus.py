"""
@author: DJZ-Nodes
Dinsky Plus Generator - A node that generates Kandinsky-style abstract art
"""

import random
from PIL import Image, ImageDraw
import numpy as np
import torch

class DinskyPlus:
    """A ComfyUI node that generates Kandinsky-style abstract art"""
    COLOR_PALETTES = {
        "kandinsky": ['#69D2E7', '#A7DBD8', '#E0E4CC', '#F38630', '#FA6900', '#FF4E50', '#F9D423'],
        "warm": ['#FF4E50', '#FC913A', '#F9D423', '#EDE574', '#E1F5C4'],
        "cool": ['#69D2E7', '#A7DBD8', '#E0E4CC', '#B2C2C1', '#8AB8B2'],
        "monochrome": ['#FFFFFF', '#D9D9D9', '#BFBFBF', '#8C8C8C', '#404040'],
        "vibrant": ['#FF1E1E', '#FF9900', '#FFFF00', '#00FF00', '#0000FF', '#9900FF']
    }

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "width": ("INT", {"default": 1024, "min": 64, "max": 4096}),
                "height": ("INT", {"default": 1024, "min": 64, "max": 4096}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 4294967295}),
                "num_shapes": ("INT", {"default": 100, "min": 1, "max": 1000}),
                "min_size": ("INT", {"default": 10, "min": 1, "max": 500}),
                "max_size": ("INT", {"default": 100, "min": 1, "max": 1000}),
                "color_palette": (list(s.COLOR_PALETTES.keys()),),
                "circle_weight": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 10.0, "step": 0.1}),
                "rectangle_weight": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 10.0, "step": 0.1}),
                "line_weight": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 10.0, "step": 0.1}),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate_art"
    CATEGORY = "DJZ-Nodes"

    def generate_art(self, width, height, seed, num_shapes, min_size, max_size, 
                    color_palette, circle_weight, rectangle_weight, line_weight):
        # Set random seed for reproducibility
        # Ensure seed is within numpy's valid range
        seed = seed % (2**32)
        random.seed(seed)
        np.random.seed(seed)

        # Create a blank canvas
        image = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(image)

        # Get colors for selected palette
        colors = self.COLOR_PALETTES[color_palette]

        # Calculate shape type probabilities
        total_weight = circle_weight + rectangle_weight + line_weight
        shape_types = []
        shape_weights = []
        if circle_weight > 0:
            shape_types.append('circle')
            shape_weights.append(circle_weight)
        if rectangle_weight > 0:
            shape_types.append('rectangle')
            shape_weights.append(rectangle_weight)
        if line_weight > 0:
            shape_types.append('line')
            shape_weights.append(line_weight)
        
        # Normalize weights
        shape_weights = [w/total_weight for w in shape_weights]

        # Generate random shapes
        for _ in range(num_shapes):
            shape_type = random.choices(shape_types, weights=shape_weights)[0]
            color = random.choice(colors)

            if shape_type == 'circle':
                radius = random.randint(min_size, max_size)
                x = random.randint(0, width)
                y = random.randint(0, height)
                draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=color, outline=None)

            elif shape_type == 'rectangle':
                x1 = random.randint(0, width)
                y1 = random.randint(0, height)
                size_w = random.randint(min_size, max_size)
                size_h = random.randint(min_size, max_size)
                x2 = min(x1 + size_w, width)
                y2 = min(y1 + size_h, height)
                draw.rectangle((x1, y1, x2, y2), fill=color, outline=None)

            elif shape_type == 'line':
                x1 = random.randint(0, width)
                y1 = random.randint(0, height)
                angle = random.uniform(0, 2 * np.pi)
                length = random.randint(min_size, max_size)
                x2 = int(x1 + length * np.cos(angle))
                y2 = int(y1 + length * np.sin(angle))
                line_width = max(1, min_size // 10)  # Scale line width with min_size
                draw.line((x1, y1, x2, y2), fill=color, width=line_width)

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
    "DinskyPlus": DinskyPlus
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DinskyPlus": "Dinsky Plus Generator"
}
