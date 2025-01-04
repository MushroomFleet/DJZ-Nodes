"""
@author: DJZ-Nodes
Dinsky Plus V2 Generator - A node that generates Kandinsky-style art from coordinate pairs
"""

import random
from PIL import Image, ImageDraw # type: ignore
import numpy as np # type: ignore
import torch # type: ignore

class DinskyPlusV2:
    """A ComfyUI node that generates Kandinsky-style abstract art from coordinate pairs"""
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
                "seed": ("INT", {"default": 0, "min": 0, "max": 2**32 - 1}),
                "x_coords": ("STRING", {"default": "100,200,300,400,500"}),
                "y_coords": ("STRING", {"default": "100,200,300,400,500"}),
                "shape_radius": ("INT", {"default": 50, "min": 1, "max": 500}),
                "line_width": ("INT", {"default": 5, "min": 1, "max": 50}),
                "color_palette": (list(s.COLOR_PALETTES.keys()),),
                "circle_weight": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 10.0, "step": 0.1}),
                "rectangle_weight": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 10.0, "step": 0.1}),
                "line_weight": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 10.0, "step": 0.1}),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate_art"
    CATEGORY = "DJZ-Nodes"

    def generate_art(self, width, height, seed, x_coords, y_coords, shape_radius, line_width,
                    color_palette, circle_weight, rectangle_weight, line_weight):
        # Set random seed for reproducibility
        # Ensure seed is within numpy's valid range
        seed = seed % (2**32)
        random.seed(seed)
        np.random.seed(seed)

        # Parse coordinate strings into lists
        try:
            x_list = [int(x.strip()) for x in x_coords.split(",")]
            y_list = [int(y.strip()) for y in y_coords.split(",")]
        except ValueError:
            # If parsing fails, use default coordinates
            x_list = [width//4, width//2, 3*width//4]
            y_list = [height//4, height//2, 3*height//4]

        # Ensure equal number of x and y coordinates
        num_points = min(len(x_list), len(y_list))
        x_list = x_list[:num_points]
        y_list = y_list[:num_points]

        # Create coordinate pairs
        pairs = list(zip(x_list, y_list))
        if len(pairs) < 2:
            # Add default points if not enough coordinates provided
            pairs.extend([(width//2, height//2), (3*width//4, 3*height//4)])

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

        # Generate shapes based on coordinate pairs
        for i, (x, y) in enumerate(pairs):
            color = random.choice(colors)
            shape_type = random.choices(shape_types, weights=shape_weights)[0]

            if shape_type == 'circle':
                draw.ellipse((x-shape_radius, y-shape_radius, x+shape_radius, y+shape_radius), 
                           fill=color, outline=None)

            elif shape_type == 'rectangle' and i < len(pairs) - 1:
                # Use the next pair for the second point of the rectangle
                x2, y2 = pairs[(i + 1) % len(pairs)]
                # Ensure coordinates are within canvas bounds
                x1, x2 = min(x, x2), max(x, x2)
                y1, y2 = min(y, y2), max(y, y2)
                x2 = min(x2, width)
                y2 = min(y2, height)
                draw.rectangle((x1, y1, x2, y2), fill=color, outline=None)

            elif shape_type == 'line' and i < len(pairs) - 1:
                # Use the next pair for the end point of the line
                x2, y2 = pairs[(i + 1) % len(pairs)]
                draw.line((x, y, x2, y2), fill=color, width=line_width)

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
    "DinskyPlusV2": DinskyPlusV2
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DinskyPlusV2": "Dinsky Plus V2 Generator"
}
