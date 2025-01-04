"""
@author: DJZ-Nodes
Fractal Generator V2 - An enhanced node that generates fractal art using various fractal types with advanced controls
"""

import numpy as np
from PIL import Image
import torch
import colorsys
import math

class FractalGeneratorV2:
    """A ComfyUI node that generates fractal art with advanced controls"""
    
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
            # Bright electric blue with white highlights
            if value > 0.95:  # Bright highlights
                return (255, 255, 255)
            # Base color is electric blue (0, 128, 255)
            blue = int(255 * (0.5 + 0.5 * value))  # Range from 128 to 255
            green = int(128 * value)  # Some green for vibrancy
            return (int(60 * value), green, blue)  # Less red for that electric feel

        def fire(value):
            # Fire gradient from deep red through orange to bright yellow
            if value < 0.33:
                # Deep red to red
                return (int(255 * (0.5 + 1.5 * value)), 0, 0)
            elif value < 0.66:
                # Red to orange
                v = (value - 0.33) * 3
                return (255, int(255 * v), 0)
            else:
                # Orange to yellow
                v = (value - 0.66) * 3
                return (255, 255, int(255 * v))

        def rainbow(value):
            # Full spectrum rainbow with increased saturation and brightness
            hue = value % 1.0
            sat = 0.9  # High saturation
            val = 0.9  # High brightness
            rgb = colorsys.hsv_to_rgb(hue, sat, val)
            return tuple(int(255 * x) for x in rgb)

        def deep_space(value):
            # Space theme with stars and nebula colors
            if value > 0.95:  # Bright stars
                return (255, 255, 255)
            elif value > 0.90:  # Dimmer stars
                star_bright = int(200 * (value - 0.90) * 10)
                return (star_bright, star_bright, star_bright)
            
            # Nebula colors - purple to blue with some pink
            hue = 0.75 + value * 0.15  # Range from purple to blue
            sat = 0.8 + value * 0.2  # High saturation
            val = 0.4 + value * 0.6  # Ensure visibility
            rgb = colorsys.hsv_to_rgb(hue, sat, val)
            r, g, b = [int(255 * x) for x in rgb]
            # Add some pink tint to certain ranges
            if 0.3 < value < 0.6:
                r = min(255, r + int(100 * value))
            return (r, g, b)

        def ocean(value):
            # Ocean colors from deep blue through turquoise to white foam
            if value > 0.9:  # White foam/caps
                foam = int(255 * (value - 0.9) * 10)
                return (foam, foam, foam)
            
            if value < 0.5:  # Deep ocean blues
                hue = 0.6 + value * 0.1  # Deep blue range
                sat = 0.9 - value * 0.3
                val = 0.3 + value * 0.7
            else:  # Turquoise shallows
                hue = 0.5 + value * 0.1  # Turquoise range
                sat = 0.7
                val = 0.6 + value * 0.4
            
            rgb = colorsys.hsv_to_rgb(hue, sat, val)
            return tuple(int(255 * x) for x in rgb)

        def forest(value):
            # Forest colors from dark green through bright green to brown
            if value < 0.4:  # Dark to medium green
                hue = 0.25 + value * 0.1
                sat = 0.9 - value * 0.2
                val = 0.3 + value * 0.7
            elif value < 0.7:  # Medium to bright green
                hue = 0.28 + value * 0.05
                sat = 0.8
                val = 0.6 + value * 0.4
            else:  # Brown highlights
                hue = 0.08  # Brown
                sat = 0.7 - (value - 0.7) * 0.5
                val = 0.6 + (value - 0.7) * 0.4
            
            rgb = colorsys.hsv_to_rgb(hue, sat, val)
            return tuple(int(255 * x) for x in rgb)

        def psychedelic(value):
            # Ultra-vibrant rainbow cycling with high saturation
            hue = (value * 5) % 1.0  # Faster color cycling
            sat = 1.0  # Maximum saturation
            val = 0.9  # High brightness but not full to maintain some color definition
            rgb = colorsys.hsv_to_rgb(hue, sat, val)
            r, g, b = [int(255 * x) for x in rgb]
            
            # Add pulsing brightness
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
        x = np.linspace(x_min, x_max, num=width).reshape((1, width))
        y = np.linspace(y_min, y_max, num=height).reshape((height, 1))
        C = np.tile(x, (height, 1)) + 1j * np.tile(y, (1, width))
        
        if preset == "Julia Set":
            # Julia set with interesting parameter
            Z = C
            C = -0.4 + 0.6j * np.ones_like(Z)
        elif preset == "Burning Ship":
            Z = np.zeros(C.shape, dtype=complex)
        elif preset == "Tricorn":
            Z = np.zeros(C.shape, dtype=complex)
        elif preset == "Newton":
            Z = C
            # Newton fractal for z³ - 1
            roots = np.array([1, -0.5 + 0.866j, -0.5 - 0.866j])
        else:  # Mandelbrot
            Z = np.zeros(C.shape, dtype=complex)

        M = np.full(C.shape, max_iter)
        
        for i in range(max_iter):
            mask = np.abs(Z) <= escape_radius
            
            if preset == "Burning Ship":
                Z[mask] = (abs(Z[mask].real) + 1j * abs(Z[mask].imag)) ** power + C[mask]
            elif preset == "Tricorn":
                Z[mask] = (Z[mask].conjugate()) ** power + C[mask]
            elif preset == "Newton":
                mask_newton = np.abs(Z ** 3 - 1) > 1e-6
                Z[mask_newton] = Z[mask_newton] - (Z[mask_newton] ** 3 - 1) / (3 * Z[mask_newton] ** 2)
                for j, root in enumerate(roots):
                    close_to_root = np.abs(Z - root) < 1e-6
                    M[close_to_root & (M == max_iter)] = i + j/3
            else:  # Mandelbrot and Julia
                Z[mask] = Z[mask] ** power + C[mask]
            
            if preset != "Newton":
                M[mask & (np.abs(Z) > escape_radius)] = i

        if smooth and preset != "Newton":
            abs_Z = np.abs(Z)
            outside_set = M < max_iter
            smooth_M = M.astype(np.float64)
            
            if np.any(outside_set):
                valid_Z = abs_Z[outside_set]
                valid_Z = np.maximum(valid_Z, 1e-6)
                
                nu = np.zeros_like(valid_Z)
                valid_mask = valid_Z > 1e-6
                if np.any(valid_mask):
                    nu[valid_mask] = np.log2(np.log2(valid_Z[valid_mask])/np.log2(escape_radius))
                
                smooth_M[outside_set] = M[outside_set] + 1 - nu
            
            return smooth_M / max_iter
        else:
            return M / max_iter

    def apply_coloring(self, fractal, width, height, color_function, color_cycles):
        image = Image.new("RGB", (width, height))
        pixels = image.load()

        for y in range(height):
            for x in range(width):
                value = fractal[y, x]
                if value == 1.0:  # Inside set
                    pixels[x, y] = (0, 0, 0)
                else:
                    # Apply color cycling
                    cycled_value = (value * color_cycles) % 1.0
                    pixels[x, y] = color_function(cycled_value)
        return image

    def generate_fractal(self, width, height, max_iterations, preset, zoom_level, color_preset, 
                        power, escape_radius, color_cycles, smooth_coloring, x_center=None, y_center=None):
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
        fractal = self.compute_fractal(width, height, x_min, x_max, y_min, y_max, 
                                     max_iterations, power, escape_radius, smooth_coloring, preset)

        # Get color function and apply coloring
        color_function = self.get_color_function(color_preset)
        image = self.apply_coloring(fractal, width, height, color_function, color_cycles)

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
    "FractalGeneratorV2": FractalGeneratorV2
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FractalGeneratorV2": "Fractal Art Generator V2"
}
