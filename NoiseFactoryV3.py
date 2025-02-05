"""
@author: Based on DJZ-Nodes template
NoiseFactory V3 - A node that generates various types of colorful noise patterns and can blend with images
"""

import numpy as np
from PIL import Image
import torch
import random
from opensimplex import OpenSimplex

class NoiseFactoryV3:
    """A ComfyUI node that generates various noise patterns with image blending capability"""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "width": ("INT", {"default": 512, "min": 64, "max": 4096}),
                "height": ("INT", {"default": 512, "min": 64, "max": 4096}),
                "noise_type": ([
                    "Plasma", 
                    "RGB Turbulence",
                    "Prismatic",
                    "HSV Noise",
                    "Perlin RGB",
                    "Polychromatic Cellular",
                    "Rainbow Fractal",
                    "Color Wavelet"
                ], {"default": "Plasma"}),
                "scale": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 10.0, "step": 0.1}),
                "octaves": ("INT", {"default": 4, "min": 1, "max": 8}),
                "persistence": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.05}),
                "saturation": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.1}),
                "noise_strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
            },
            "optional": {
                "seed": ("INT", {"default": -1, "min": -1, "max": 0xffffffff}),
                "image": ("IMAGE",),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate_noise"
    CATEGORY = "DJZ-Nodes"

    def generate_plasma(self, width, height, scale, octaves, persistence):
        noise_generators = [OpenSimplex(seed=random.randint(0, 1000000)) for _ in range(3)]
        result = np.zeros((height, width, 3))
        
        # Parameters for plasma-like effect
        time_offset = random.random() * 1000
        plasma_scale = scale * 2.0  # Increased scale for more pronounced plasma effect
        
        for y in range(height):
            for x in range(width):
                # Base coordinates
                nx = x / width * plasma_scale
                ny = y / height * plasma_scale
                
                # Generate three different noise fields that will interact
                noise1 = noise2 = noise3 = 0
                amplitude = 1.0
                freq = 1.0
                
                for o in range(octaves):
                    # Add different frequencies with varying phase shifts
                    phase1 = time_offset + nx * freq
                    phase2 = time_offset + ny * freq
                    phase3 = time_offset + (nx + ny) * freq * 0.5
                    
                    noise1 += noise_generators[0].noise2(phase1, ny * freq) * amplitude
                    noise2 += noise_generators[1].noise2(nx * freq, phase2) * amplitude
                    noise3 += noise_generators[2].noise2(phase3, phase3) * amplitude
                    
                    amplitude *= persistence
                    freq *= 2.0
                
                # Combine noise fields with sine waves for plasma effect
                r = np.sin(noise1 * np.pi) * 0.5 + 0.5
                g = np.sin(noise2 * np.pi + 2.0944) * 0.5 + 0.5  # 2π/3 phase shift
                b = np.sin(noise3 * np.pi + 4.1888) * 0.5 + 0.5  # 4π/3 phase shift
                
                # Add interference patterns
                interference = np.sin((nx + ny) * 8.0) * 0.1
                r = np.clip(r + interference, 0, 1)
                g = np.clip(g + interference, 0, 1)
                b = np.clip(b + interference, 0, 1)
                
                result[y, x] = [r, g, b]
        
        # Create 2D mask with correct dimensions
        x = np.linspace(0, np.pi * 2, width)
        y = np.linspace(0, np.pi * 2, height)
        X, Y = np.meshgrid(x, y)
        mask = np.sin(X) * np.sin(Y)
        mask = mask[:,:,np.newaxis]  # Add channel dimension
        result = result * (0.8 + mask * 0.2)
        
        return result

    def generate_perlin_rgb(self, width, height, scale, octaves, persistence):
        noise_r = OpenSimplex(seed=random.randint(0, 1000000))
        noise_g = OpenSimplex(seed=random.randint(0, 1000000))
        noise_b = OpenSimplex(seed=random.randint(0, 1000000))
        
        result = np.zeros((height, width, 3))
        
        for y in range(height):
            for x in range(width):
                nx = x / width * scale
                ny = y / height * scale
                
                r = g = b = 0
                amplitude = 1.0
                freq = 1.0
                
                for _ in range(octaves):
                    r += noise_r.noise2(nx * freq, ny * freq) * amplitude
                    g += noise_g.noise2(nx * freq, ny * freq) * amplitude
                    b += noise_b.noise2(nx * freq, ny * freq) * amplitude
                    amplitude *= persistence
                    freq *= 2
                
                result[y, x] = [(r + 1) / 2, (g + 1) / 2, (b + 1) / 2]
        
        return result

    def generate_hsv_noise(self, width, height, scale, octaves, persistence, saturation):
        noise_h = OpenSimplex(seed=random.randint(0, 1000000))
        noise_s = OpenSimplex(seed=random.randint(0, 1000000))
        noise_v = OpenSimplex(seed=random.randint(0, 1000000))
        
        def hsv_to_rgb(h, s, v):
            h = h % 1.0
            c = v * s
            x = c * (1 - abs((h * 6) % 2 - 1))
            m = v - c
            
            if h < 1/6:
                r, g, b = c, x, 0
            elif h < 2/6:
                r, g, b = x, c, 0
            elif h < 3/6:
                r, g, b = 0, c, x
            elif h < 4/6:
                r, g, b = 0, x, c
            elif h < 5/6:
                r, g, b = x, 0, c
            else:
                r, g, b = c, 0, x
                
            return r + m, g + m, b + m
        
        result = np.zeros((height, width, 3))
        
        for y in range(height):
            for x in range(width):
                nx = x / width * scale
                ny = y / height * scale
                
                h = v = 0
                amplitude = 1.0
                freq = 1.0
                
                for _ in range(octaves):
                    h += noise_h.noise2(nx * freq, ny * freq) * amplitude
                    v += noise_v.noise2(nx * freq, ny * freq) * amplitude
                    amplitude *= persistence
                    freq *= 2
                
                h = (h + 1) / 2
                v = ((v + 1) / 2) * 0.8 + 0.2  # Ensure some minimum brightness
                
                result[y, x] = hsv_to_rgb(h, saturation, v)
        
        return result

    def generate_rgb_turbulence(self, width, height, scale, octaves, persistence):
        result = np.zeros((height, width, 3))
        noise_generators = [OpenSimplex(seed=random.randint(0, 1000000)) for _ in range(6)]  # 2 per channel
        
        for y in range(height):
            for x in range(width):
                for c in range(3):  # RGB channels
                    value = 0
                    amplitude = 1.0
                    freq = 1.0
                    # Use two noise generators per channel for more turbulent effect
                    for o in range(octaves):
                        nx = x / width * scale * freq
                        ny = y / height * scale * freq
                        value += (noise_generators[c*2].noise2(nx, ny) * 
                                noise_generators[c*2+1].noise2(ny, nx)) * amplitude
                        amplitude *= persistence
                        freq *= 2
                    result[y, x, c] = (value + 1) / 2
        return result

    def generate_prismatic(self, width, height, scale, octaves, persistence):
        base_noise = OpenSimplex(seed=random.randint(0, 1000000))
        result = np.zeros((height, width, 3))
        
        for y in range(height):
            for x in range(width):
                value = 0
                amplitude = 1.0
                freq = 1.0
                
                for o in range(octaves):
                    nx = x / width * scale * freq
                    ny = y / height * scale * freq
                    value += base_noise.noise2(nx, ny) * amplitude
                    amplitude *= persistence
                    freq *= 2
                
                # Convert noise to spectral colors
                hue = (value + 1) / 2  # Normalize to 0-1
                # Convert spectral hue to RGB
                h = hue * 6
                if h < 1:
                    result[y, x] = [1, h, 0]
                elif h < 2:
                    result[y, x] = [2-h, 1, 0]
                elif h < 3:
                    result[y, x] = [0, 1, h-2]
                elif h < 4:
                    result[y, x] = [0, 4-h, 1]
                elif h < 5:
                    result[y, x] = [h-4, 0, 1]
                else:
                    result[y, x] = [1, 0, 6-h]
        return result

    def generate_polychromatic_cellular(self, width, height, scale, octaves, persistence):
        result = np.zeros((height, width, 3))
        # Generate random points for cellular noise
        num_points = 20 * scale
        points = np.random.rand(int(num_points), 2)  # Random points in 0-1 space
        colors = np.random.rand(int(num_points), 3)  # Random colors for each point
        
        for y in range(height):
            for x in range(width):
                px = x / width
                py = y / height
                # Find distances to all points
                distances = np.sqrt(((points - [px, py]) ** 2).sum(axis=1))
                # Get indices of two closest points
                closest_idx = np.argpartition(distances, 2)[:2]
                # Interpolate between colors of two closest points
                d1, d2 = distances[closest_idx]
                t = d1 / (d1 + d2)  # Interpolation factor
                result[y, x] = colors[closest_idx[0]] * (1-t) + colors[closest_idx[1]] * t
        return result

    def generate_rainbow_fractal(self, width, height, scale, octaves, persistence):
        result = np.zeros((height, width, 3))
        noise_gen = OpenSimplex(seed=random.randint(0, 1000000))
        
        for y in range(height):
            for x in range(width):
                value = 0
                amplitude = 1.0
                freq = 1.0
                
                for o in range(octaves):
                    nx = x / width * scale * freq
                    ny = y / height * scale * freq
                    value += noise_gen.noise2(nx, ny) * amplitude
                    amplitude *= persistence
                    freq *= 2.5  # Use 2.5 for more interesting fractal patterns
                
                # Convert to rainbow colors using polar coordinates
                angle = np.arctan2(value, amplitude) + np.pi
                hue = (angle / (2 * np.pi) + value) % 1.0
                
                # Convert hue to RGB
                h = hue * 6
                x_val = 1 - abs(h % 2 - 1)
                if h < 1:
                    result[y, x] = [1, x_val, 0]
                elif h < 2:
                    result[y, x] = [x_val, 1, 0]
                elif h < 3:
                    result[y, x] = [0, 1, x_val]
                elif h < 4:
                    result[y, x] = [0, x_val, 1]
                elif h < 5:
                    result[y, x] = [x_val, 0, 1]
                else:
                    result[y, x] = [1, 0, x_val]
        return result

    def generate_color_wavelet(self, width, height, scale, octaves, persistence):
        result = np.zeros((height, width, 3))
        noise_gens = [OpenSimplex(seed=random.randint(0, 1000000)) for _ in range(3)]
        
        for y in range(height):
            for x in range(width):
                for c in range(3):
                    value = 0
                    amplitude = 1.0
                    freq = 1.0
                    phase = c * 2 * np.pi / 3  # Phase shift for each color channel
                    
                    for o in range(octaves):
                        nx = x / width * scale * freq
                        ny = y / height * scale * freq
                        # Add wavelet-like behavior with phase shifts
                        value += (noise_gens[c].noise2(nx, ny) * 
                                np.sin(freq * phase + nx * 2 * np.pi)) * amplitude
                        amplitude *= persistence
                        freq *= 2
                    
                    result[y, x, c] = (value + 1) / 2
        return result

    def blend_with_image(self, noise, image_tensor, strength):
        """Blend noise with input image based on strength parameter"""
        if image_tensor is None:
            return noise
            
        # Convert noise to tensor
        noise_tensor = torch.from_numpy(noise)
        
        # Convert image tensor to same format as noise
        image = image_tensor.squeeze(0) if len(image_tensor.shape) == 4 else image_tensor
        
        # Resize image if dimensions don't match
        if image.shape[:2] != noise_tensor.shape[:2]:
            image_np = image.cpu().numpy()
            image_pil = Image.fromarray((image_np * 255).astype(np.uint8))
            image_pil = image_pil.resize((noise_tensor.shape[1], noise_tensor.shape[0]), Image.LANCZOS)
            image_np = np.array(image_pil).astype(np.float32) / 255.0
            image = torch.from_numpy(image_np)
        
        # Perform the blending in tensor space
        blended = noise_tensor * strength + image * (1 - strength)
        
        # Convert back to numpy and ensure proper range
        return blended.cpu().numpy().clip(0, 1)

    def generate_noise(self, width, height, noise_type, scale=1.0, octaves=4, 
                      persistence=0.5, saturation=1.0, noise_strength=1.0,
                      seed=-1, image=None):
        if seed != -1:
            np.random.seed(seed)
            random.seed(seed)
            
        # Generate base noise using existing methods
        if noise_type == "Plasma":
            noise = self.generate_plasma(width, height, scale, octaves, persistence)
        elif noise_type == "Perlin RGB":
            noise = self.generate_perlin_rgb(width, height, scale, octaves, persistence)
        elif noise_type == "HSV Noise":
            noise = self.generate_hsv_noise(width, height, scale, octaves, persistence, saturation)
        elif noise_type == "RGB Turbulence":
            noise = self.generate_rgb_turbulence(width, height, scale, octaves, persistence)
        elif noise_type == "Prismatic":
            noise = self.generate_prismatic(width, height, scale, octaves, persistence)
        elif noise_type == "Polychromatic Cellular":
            noise = self.generate_polychromatic_cellular(width, height, scale, octaves, persistence)
        elif noise_type == "Rainbow Fractal":
            noise = self.generate_rainbow_fractal(width, height, scale, octaves, persistence)
        elif noise_type == "Color Wavelet":
            noise = self.generate_color_wavelet(width, height, scale, octaves, persistence)
        else:
            noise = self.generate_plasma(width, height, scale, octaves, persistence)
        
        # Ensure values are in valid range
        noise = np.clip(noise, 0, 1)
        
        # Blend with input image if provided
        if image is not None:
            noise = self.blend_with_image(noise, image, noise_strength)
        
        # Convert to tensor in ComfyUI format (B,H,W,C)
        noise = noise.astype(np.float32)
        noise_tensor = torch.from_numpy(noise)
        
        # Ensure shape is (B,H,W,C)
        if len(noise_tensor.shape) == 3:  # If shape is (H,W,C)
            noise_tensor = noise_tensor.unsqueeze(0)  # Add batch dimension
        
        # Double check dimensions are correct
        if noise_tensor.shape[3] != 3:  # If channels are not in last dimension
            noise_tensor = noise_tensor.permute(0, 2, 3, 1)  # Reorder to (B,H,W,C)
            
        return (noise_tensor,)

# Node registration for ComfyUI
NODE_CLASS_MAPPINGS = {
    "NoiseFactoryV3": NoiseFactoryV3
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "NoiseFactoryV3": "Noise Factory V3"
}
