"""
@author: DJZ-Nodes
Fractal Generator V3 - A CUDA-accelerated node that generates fractal art using various fractal types with advanced controls
"""

import numpy as np
from PIL import Image
import torch
import colorsys
import math

class FractalGeneratorV3:
    """A ComfyUI node that generates fractal art with CUDA acceleration"""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "width": ("INT", {"default": 1024, "min": 64, "max": 4096}),
                "height": ("INT", {"default": 1024, "min": 64, "max": 4096}),
                "max_iterations": ("INT", {"default": 500, "min": 50, "max": 2000}),
                "preset": (["Custom", "Classic Mandelbrot", "Julia Set", "Burning Ship", "Tricorn", "Newton"], {"default": "Classic Mandelbrot"}),
                "zoom_level": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 100.0, "step": 0.1}),
                "color_preset": ([
                    "Classic White-Grey", 
                    "Electric Blue", 
                    "Fire", 
                    "Rainbow", 
                    "Deep Space",
                    "Ocean",
                    "Forest",
                    "Psychedelic"
                ], {"default": "Classic White-Grey"}),
                "power": ("FLOAT", {"default": 2.0, "min": 2.0, "max": 5.0, "step": 0.1}),
                "escape_radius": ("FLOAT", {"default": 2.0, "min": 1.0, "max": 10.0, "step": 0.1}),
                "color_cycles": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 10.0, "step": 0.1}),
                "smooth_coloring": ("BOOLEAN", {"default": True}),
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
            "Julia Set": (0.0, 0.0, 1.5),
            "Burning Ship": (-0.5, -0.5, 0.8),
            "Tricorn": (0.0, 0.0, 1.2),
            "Newton": (0.0, 0.0, 1.0),
        }
        
        if preset in presets:
            x, y, base_zoom = presets[preset]
            actual_zoom = base_zoom * zoom_level
            return x, y, actual_zoom
        return None

    def get_color_function(self, preset):
        def classic_white_grey(value):
            grey = int(255 * (1 - value))
            return (grey, grey, grey)

        def electric_blue(value):
            if value > 0.95:
                return (255, 255, 255)
            blue = int(255 * (0.5 + 0.5 * value))
            green = int(128 * value)
            return (int(60 * value), green, blue)

        def fire(value):
            if value < 0.33:
                return (int(255 * (0.5 + 1.5 * value)), 0, 0)
            elif value < 0.66:
                v = (value - 0.33) * 3
                return (255, int(255 * v), 0)
            else:
                v = (value - 0.66) * 3
                return (255, 255, int(255 * v))

        def rainbow(value):
            hue = value % 1.0
            sat = 0.9
            val = 0.9
            rgb = colorsys.hsv_to_rgb(hue, sat, val)
            return tuple(int(255 * x) for x in rgb)

        def deep_space(value):
            if value > 0.95:
                return (255, 255, 255)
            elif value > 0.90:
                star_bright = int(200 * (value - 0.90) * 10)
                return (star_bright, star_bright, star_bright)
            
            hue = 0.75 + value * 0.15
            sat = 0.8 + value * 0.2
            val = 0.4 + value * 0.6
            rgb = colorsys.hsv_to_rgb(hue, sat, val)
            r, g, b = [int(255 * x) for x in rgb]
            if 0.3 < value < 0.6:
                r = min(255, r + int(100 * value))
            return (r, g, b)

        def ocean(value):
            if value > 0.9:
                foam = int(255 * (value - 0.9) * 10)
                return (foam, foam, foam)
            
            if value < 0.5:
                hue = 0.6 + value * 0.1
                sat = 0.9 - value * 0.3
                val = 0.3 + value * 0.7
            else:
                hue = 0.5 + value * 0.1
                sat = 0.7
                val = 0.6 + value * 0.4
            
            rgb = colorsys.hsv_to_rgb(hue, sat, val)
            return tuple(int(255 * x) for x in rgb)

        def forest(value):
            if value < 0.4:
                hue = 0.25 + value * 0.1
                sat = 0.9 - value * 0.2
                val = 0.3 + value * 0.7
            elif value < 0.7:
                hue = 0.28 + value * 0.05
                sat = 0.8
                val = 0.6 + value * 0.4
            else:
                hue = 0.08
                sat = 0.7 - (value - 0.7) * 0.5
                val = 0.6 + (value - 0.7) * 0.4
            
            rgb = colorsys.hsv_to_rgb(hue, sat, val)
            return tuple(int(255 * x) for x in rgb)

        def psychedelic(value):
            hue = (value * 5) % 1.0
            sat = 1.0
            val = 0.9
            rgb = colorsys.hsv_to_rgb(hue, sat, val)
            r, g, b = [int(255 * x) for x in rgb]
            
            pulse = abs(math.sin(value * math.pi * 2))
            r = min(255, r + int(50 * pulse))
            g = min(255, g + int(50 * pulse))
            b = min(255, b + int(50 * pulse))
            return (r, g, b)

        color_functions = {
            "Classic White-Grey": classic_white_grey,
            "Electric Blue": electric_blue,
            "Fire": fire,
            "Rainbow": rainbow,
            "Deep Space": deep_space,
            "Ocean": ocean,
            "Forest": forest,
            "Psychedelic": psychedelic
        }

        return color_functions.get(preset, classic_white_grey)

    def compute_fractal(self, width, height, x_min, x_max, y_min, y_max, max_iter, power, escape_radius, smooth, preset):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        x = torch.linspace(x_min, x_max, width, device=device).view(1, width)
        y = torch.linspace(y_min, y_max, height, device=device).view(height, 1)
        
        # Create complex plane using broadcasting
        real = x.expand(height, width)
        imag = y.expand(height, width)
        C = torch.complex(real, imag)
        
        if preset == "Julia Set":
            Z = C
            C = torch.full_like(Z, -0.4 + 0.6j)
        elif preset == "Burning Ship":
            Z = torch.zeros_like(C)
        elif preset == "Tricorn":
            Z = torch.zeros_like(C)
        elif preset == "Newton":
            Z = C
            roots = torch.tensor([1, -0.5 + 0.866j, -0.5 - 0.866j], device=device)
        else:  # Mandelbrot
            Z = torch.zeros_like(C)

        M = torch.full((height, width), max_iter, device=device, dtype=torch.float32)
        
        for i in range(max_iter):
            mask = torch.abs(Z) <= escape_radius
            
            if preset == "Burning Ship":
                Z[mask] = (torch.abs(Z[mask].real) + 1j * torch.abs(Z[mask].imag)) ** power + C[mask]
            elif preset == "Tricorn":
                Z[mask] = (Z[mask].conj()) ** power + C[mask]
            elif preset == "Newton":
                mask_newton = torch.abs(Z ** 3 - 1) > 1e-6
                Z[mask_newton] = Z[mask_newton] - (Z[mask_newton] ** 3 - 1) / (3 * Z[mask_newton] ** 2)
                for j, root in enumerate(roots):
                    close_to_root = torch.abs(Z - root) < 1e-6
                    M[close_to_root & (M == max_iter)] = i + j/3
            else:  # Mandelbrot and Julia
                Z[mask] = Z[mask] ** power + C[mask]
            
            if preset != "Newton":
                escaped = mask & (torch.abs(Z) > escape_radius)
                M[escaped] = i

        if smooth and preset != "Newton":
            abs_Z = torch.abs(Z)
            outside_set = M < max_iter
            smooth_M = M.float()
            
            if outside_set.any():
                valid_Z = abs_Z[outside_set]
                valid_Z = torch.maximum(valid_Z, torch.tensor(1e-6, device=device))
                
                nu = torch.zeros_like(valid_Z)
                valid_mask = valid_Z > 1e-6
                if valid_mask.any():
                    nu[valid_mask] = torch.log2(torch.log2(valid_Z[valid_mask])/math.log2(escape_radius))
                
                smooth_M[outside_set] = M[outside_set] + 1 - nu
            
            return (smooth_M / max_iter).cpu().numpy()
        else:
            return (M / max_iter).cpu().numpy()

    def apply_coloring(self, fractal, width, height, color_function, color_cycles):
        image = Image.new("RGB", (width, height))
        pixels = image.load()

        for y in range(height):
            for x in range(width):
                value = fractal[y, x]
                if value == 1.0:  # Inside set
                    pixels[x, y] = (0, 0, 0)
                else:
                    cycled_value = (value * color_cycles) % 1.0
                    pixels[x, y] = color_function(cycled_value)
        return image

    def generate_fractal(self, width, height, max_iterations, preset, zoom_level, color_preset, 
                        power, escape_radius, color_cycles, smooth_coloring, x_center=None, y_center=None):
        if preset != "Custom" and x_center is None:
            x_center, y_center, zoom_level = self.get_preset_coordinates(preset, zoom_level)
        elif x_center is None:
            x_center, y_center = -0.75, 0.0

        window_size = 4.0 / zoom_level
        x_min = x_center - window_size/2
        x_max = x_center + window_size/2
        y_min = y_center - window_size/2
        y_max = y_center + window_size/2

        fractal = self.compute_fractal(width, height, x_min, x_max, y_min, y_max, 
                                     max_iterations, power, escape_radius, smooth_coloring, preset)

        color_function = self.get_color_function(color_preset)
        image = self.apply_coloring(fractal, width, height, color_function, color_cycles)

        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        image_np = np.array(image).astype(np.float32) / 255.0
        image_tensor = torch.from_numpy(image_np)
        
        if len(image_tensor.shape) == 3:
            image_tensor = image_tensor.unsqueeze(0)
        
        return (image_tensor,)

# Node registration for ComfyUI
NODE_CLASS_MAPPINGS = {
    "FractalGeneratorV3": FractalGeneratorV3
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FractalGeneratorV3": "Fractal Gen Cuda"
}
