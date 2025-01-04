"""
@author: DJZ-Nodes
Fractal Generator - A node that generates fractal art using the Mandelbrot set
"""

import numpy as np
from PIL import Image
import torch

class FractalGenerator:
    """A ComfyUI node that generates fractal art"""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "width": ("INT", {"default": 1024, "min": 64, "max": 4096}),
                "height": ("INT", {"default": 1024, "min": 64, "max": 4096}),
                "max_iterations": ("INT", {"default": 500, "min": 50, "max": 2000}),
                "preset": (["Custom", "Classic Mandelbrot", "Spiral Galaxy", "Seahorse Valley", "Elephant Valley", "Mini Mandelbrot"], {"default": "Classic Mandelbrot"}),
                "zoom_level": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 100.0, "step": 0.1}),
            },
            "optional": {
                "x_center": ("FLOAT", {"default": -0.75, "min": -2.0, "max": 2.0, "step": 0.0001}),
                "y_center": ("FLOAT", {"default": 0.0, "min": -2.0, "max": 2.0, "step": 0.0001}),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate_fractal"
    CATEGORY = "DJZ-Nodes"

    def get_preset_coordinates(self, preset, zoom_level):
        presets = {
            "Classic Mandelbrot": (-0.75, 0.0, 1.0),
            "Spiral Galaxy": (-0.744, 0.1, 40.0),
            "Seahorse Valley": (-0.74877, 0.065053, 80.0),
            "Elephant Valley": (0.3, 0.0, 30.0),
            "Mini Mandelbrot": (-1.77, 0.0, 20.0),
        }
        
        if preset in presets:
            x, y, base_zoom = presets[preset]
            actual_zoom = base_zoom * zoom_level
            return x, y, actual_zoom
        return None

    def mandelbrot_set(self, width, height, x_min, x_max, y_min, y_max, max_iter):
        x = np.linspace(x_min, x_max, num=width).reshape((1, width))
        y = np.linspace(y_min, y_max, num=height).reshape((height, 1))
        C = np.tile(x, (height, 1)) + 1j * np.tile(y, (1, width))

        Z = np.zeros(C.shape, dtype=complex)
        M = np.full(C.shape, True, dtype=bool)
        
        for i in range(max_iter):
            Z[M] = Z[M] * Z[M] + C[M]
            M[np.abs(Z) > 2] = False
        
        return M

    def apply_gradient(self, fractal, width, height):
        image = Image.new("RGB", (width, height))
        pixels = image.load()

        color_top = (64, 64, 64)  # Dark grey
        color_bottom = (255, 255, 255)  # White
        gradient_steps = [tuple(int(color_top[j] + (color_bottom[j] - color_top[j]) * (i / height)) 
                              for j in range(3)) for i in range(height)]

        for y in range(height):
            gradient_color = gradient_steps[y]
            for x in range(width):
                if fractal[y, x]:
                    pixels[x, y] = gradient_color
        return image

    def generate_fractal(self, width, height, max_iterations, preset, zoom_level=1.0, x_center=None, y_center=None):
        # Calculate viewing window
        if preset != "Custom" and x_center is None:
            x_center, y_center, zoom_level = self.get_preset_coordinates(preset, zoom_level)
        elif x_center is None:
            x_center, y_center = -0.75, 0.0

        window_size = 4.0 / zoom_level
        x_min = x_center - window_size/2
        x_max = x_center + window_size/2
        y_min = y_center - window_size/2
        y_max = y_center + window_size/2

        # Generate the fractal
        fractal = self.mandelbrot_set(width, height, x_min, x_max, y_min, y_max, max_iterations)

        # Apply gradient and create image
        image = self.apply_gradient(fractal, width, height)

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
    "FractalGenerator": FractalGenerator
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FractalGenerator": "Fractal Art Generator"
}
