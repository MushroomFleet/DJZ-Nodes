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
                "preset": (["Custom", "Classic Mandelbrot", "Julia Set", "Burning Ship", "Tricorn", "Newton"], {"default": "Classic Mandelbrot"}),
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
            "Classic Mandelbrot": (-0.5, 0.0, 0.8),  # Shows the full set
            "Julia Set": (0.0, 0.0, 0.8),  # Centered view of Julia set
            "Burning Ship": (-0.4, -0.6, 0.6),  # Shows the main "ship" structure
            "Tricorn": (0.0, 0.0, 0.8),  # Centered view of tricorn
            "Newton": (0.0, 0.0, 0.7),  # Shows full Newton basins
        }
        
        if preset in presets:
            x, y, base_zoom = presets[preset]
            actual_zoom = base_zoom * zoom_level
            return x, y, actual_zoom
        return None

    def compute_fractal(self, width, height, x_min, x_max, y_min, y_max, max_iter, preset):
        x = np.linspace(x_min, x_max, num=width).reshape((1, width))
        y = np.linspace(y_min, y_max, num=height).reshape((height, 1))
        C = np.tile(x, (height, 1)) + 1j * np.tile(y, (1, width))
        
        # Set initial conditions and parameters based on fractal type
        if preset == "Julia Set":
            Z = C.copy()
            C = -0.4 + 0.6j * np.ones_like(Z)  # Classic Julia set parameter
            escape_radius = 2.0
            power = 2
        elif preset == "Burning Ship":
            Z = np.zeros_like(C)
            escape_radius = 2.0
            power = 2
        elif preset == "Tricorn":
            Z = np.zeros_like(C)
            escape_radius = 2.0
            power = 2
        elif preset == "Newton":
            Z = C.copy()
            roots = np.array([1, -0.5 + 0.866j, -0.5 - 0.866j])  # Cube roots of 1
            tolerance = 1e-6
            power = 3
        else:  # Classic Mandelbrot
            Z = np.zeros_like(C)
            escape_radius = 2.0
            power = 2

        M = np.full(C.shape, max_iter)
        
        if preset == "Newton":
            # Special handling for Newton fractal
            for i in range(max_iter):
                # Newton's method for z^3 - 1
                not_converged = np.abs(Z ** power - 1) > tolerance
                Z[not_converged] = Z[not_converged] - (Z[not_converged] ** power - 1) / (power * Z[not_converged] ** (power - 1))
                
                # Check convergence to each root
                for j, root in enumerate(roots):
                    converged_to_root = (np.abs(Z - root) < tolerance) & (M == max_iter)
                    M[converged_to_root] = i + j/len(roots)
        else:
            # Standard escape-time fractals
            for i in range(max_iter):
                mask = np.abs(Z) <= escape_radius
                
                if preset == "Burning Ship":
                    Z[mask] = (abs(Z[mask].real) + 1j * abs(Z[mask].imag)) ** power + C[mask]
                elif preset == "Tricorn":
                    Z[mask] = np.conj(Z[mask]) ** power + C[mask]
                else:  # Mandelbrot and Julia
                    Z[mask] = Z[mask] ** power + C[mask]
                
                M[mask & (np.abs(Z) > escape_radius)] = i
        
        return M / max_iter

    def apply_gradient(self, fractal, width, height):
        image = Image.new("RGB", (width, height))
        pixels = image.load()

        color_inside = (0, 0, 0)  # Black for points inside the set
        color_outside = (255, 255, 255)  # White for points outside

        for y in range(height):
            for x in range(width):
                value = fractal[y, x]
                if value == 1.0:  # Inside the set
                    pixels[x, y] = color_inside
                else:
                    # Create a gradient based on iteration count
                    intensity = int(255 * (1 - value))
                    pixels[x, y] = (intensity, intensity, intensity)
        return image

    def generate_fractal(self, width, height, max_iterations, preset, zoom_level=1.0, x_center=None, y_center=None):
        # Calculate viewing window
        if preset != "Custom" and x_center is None:
            x_center, y_center, zoom_level = self.get_preset_coordinates(preset, zoom_level)
        elif x_center is None:
            x_center, y_center = -0.75, 0.0

        window_size = 3.0 / zoom_level  # Reduced from 4.0 to 3.0 for better default zoom
        x_min = x_center - window_size/2
        x_max = x_center + window_size/2
        y_min = y_center - window_size/2
        y_max = y_center + window_size/2

        # Generate the fractal
        fractal = self.compute_fractal(width, height, x_min, x_max, y_min, y_max, max_iterations, preset)

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
