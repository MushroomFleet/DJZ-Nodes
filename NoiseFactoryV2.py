"""
@author: Based on DJZ-Nodes template
NoiseFactoryV2 - An enhanced node that generates various types of colorful noise patterns with turbulence control
"""

import numpy as np
from PIL import Image
import torch
import random
from opensimplex import OpenSimplex

class NoiseFactoryV2:
    """An enhanced ComfyUI node that generates various noise patterns with turbulence control"""
    
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
                ], {"default": "RGB Turbulence"}),
                "scale": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 10.0, "step": 0.1}),
                "octaves": ("INT", {"default": 4, "min": 1, "max": 8}),
                "persistence": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.05}),
                "turbulence": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 2.0, "step": 0.1}),
                "frequency": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 5.0, "step": 0.1}),
                "saturation": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.1}),
                "red_balance": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.1}),
                "green_balance": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.1}),
                "blue_balance": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.1}),
            },
            "optional": {
                "seed": ("INT", {"default": -1, "min": -1, "max": 0xffffffff}),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate_noise"
    CATEGORY = "DJZ-Nodes"

    def apply_turbulence(self, value, nx, ny, turbulence, noise_gen):
        """Apply turbulence distortion to the noise value"""
        if turbulence <= 0:
            return value
        
        # Generate turbulence field
        turb = noise_gen.noise2(nx * 2, ny * 2) * turbulence
        
        # Apply turbulent displacement
        displaced_x = nx + turb
        displaced_y = ny + turb
        
        # Mix original and turbulent value
        turbulent_value = noise_gen.noise2(displaced_x, displaced_y)
        return value * (1 - turbulence) + turbulent_value * turbulence

    def generate_plasma(self, width, height, scale, octaves, persistence, turbulence, frequency):
        noise_generators = [OpenSimplex(seed=random.randint(0, 1000000)) for _ in range(3)]
        turb_gen = OpenSimplex(seed=random.randint(0, 1000000))
        result = np.zeros((height, width, 3))
        
        time_offset = random.random() * 1000
        plasma_scale = scale * 2.0
        
        for y in range(height):
            for x in range(width):
                nx = x / width * plasma_scale * frequency
                ny = y / height * plasma_scale * frequency
                
                noise1 = noise2 = noise3 = 0
                amplitude = 1.0
                freq = 1.0
                
                for o in range(octaves):
                    phase1 = time_offset + nx * freq
                    phase2 = time_offset + ny * freq
                    phase3 = time_offset + (nx + ny) * freq * 0.5
                    
                    # Apply turbulence to each noise component
                    n1 = self.apply_turbulence(
                        noise_generators[0].noise2(phase1, ny * freq),
                        phase1, ny * freq, turbulence, turb_gen
                    )
                    n2 = self.apply_turbulence(
                        noise_generators[1].noise2(nx * freq, phase2),
                        nx * freq, phase2, turbulence, turb_gen
                    )
                    n3 = self.apply_turbulence(
                        noise_generators[2].noise2(phase3, phase3),
                        phase3, phase3, turbulence, turb_gen
                    )
                    
                    noise1 += n1 * amplitude
                    noise2 += n2 * amplitude
                    noise3 += n3 * amplitude
                    
                    amplitude *= persistence
                    freq *= 2.0
                
                r = np.sin(noise1 * np.pi) * 0.5 + 0.5
                g = np.sin(noise2 * np.pi + 2.0944) * 0.5 + 0.5
                b = np.sin(noise3 * np.pi + 4.1888) * 0.5 + 0.5
                
                interference = np.sin((nx + ny) * 8.0) * 0.1
                r = np.clip(r + interference, 0, 1)
                g = np.clip(g + interference, 0, 1)
                b = np.clip(b + interference, 0, 1)
                
                result[y, x] = [r, g, b]
        
        x = np.linspace(0, np.pi * 2, width)
        y = np.linspace(0, np.pi * 2, height)
        X, Y = np.meshgrid(x, y)
        mask = np.sin(X) * np.sin(Y)
        mask = mask[:,:,np.newaxis]
        result = result * (0.8 + mask * 0.2)
        
        return result

    def generate_rgb_turbulence(self, width, height, scale, octaves, persistence, turbulence, frequency):
        result = np.zeros((height, width, 3))
        noise_generators = [OpenSimplex(seed=random.randint(0, 1000000)) for _ in range(6)]
        turb_gen = OpenSimplex(seed=random.randint(0, 1000000))
        
        for y in range(height):
            for x in range(width):
                for c in range(3):
                    value = 0
                    amplitude = 1.0
                    freq = 1.0
                    
                    for o in range(octaves):
                        nx = x / width * scale * freq * frequency
                        ny = y / height * scale * freq * frequency
                        
                        # Enhanced turbulent noise calculation
                        base_noise = (noise_generators[c*2].noise2(nx, ny) * 
                                    noise_generators[c*2+1].noise2(ny, nx))
                        
                        # Apply turbulence distortion
                        turbulent_value = self.apply_turbulence(
                            base_noise, nx, ny, turbulence, turb_gen
                        )
                        
                        value += turbulent_value * amplitude
                        amplitude *= persistence
                        freq *= 2
                    
                    result[y, x, c] = (value + 1) / 2
        
        return result

    def generate_perlin_rgb(self, width, height, scale, octaves, persistence, turbulence, frequency):
        noise_r = OpenSimplex(seed=random.randint(0, 1000000))
        noise_g = OpenSimplex(seed=random.randint(0, 1000000))
        noise_b = OpenSimplex(seed=random.randint(0, 1000000))
        turb_gen = OpenSimplex(seed=random.randint(0, 1000000))
        
        result = np.zeros((height, width, 3))
        
        for y in range(height):
            for x in range(width):
                nx = x / width * scale * frequency
                ny = y / height * scale * frequency
                
                r = g = b = 0
                amplitude = 1.0
                freq = 1.0
                
                for _ in range(octaves):
                    # Apply turbulence to each color channel
                    r_val = self.apply_turbulence(
                        noise_r.noise2(nx * freq, ny * freq),
                        nx * freq, ny * freq, turbulence, turb_gen
                    )
                    g_val = self.apply_turbulence(
                        noise_g.noise2(nx * freq, ny * freq),
                        nx * freq, ny * freq, turbulence, turb_gen
                    )
                    b_val = self.apply_turbulence(
                        noise_b.noise2(nx * freq, ny * freq),
                        nx * freq, ny * freq, turbulence, turb_gen
                    )
                    
                    r += r_val * amplitude
                    g += g_val * amplitude
                    b += b_val * amplitude
                    
                    amplitude *= persistence
                    freq *= 2
                
                result[y, x] = [(r + 1) / 2, (g + 1) / 2, (b + 1) / 2]
        
        return result

    def generate_hsv_noise(self, width, height, scale, octaves, persistence, turbulence, frequency, saturation):
        noise_h = OpenSimplex(seed=random.randint(0, 1000000))
        noise_s = OpenSimplex(seed=random.randint(0, 1000000))
        noise_v = OpenSimplex(seed=random.randint(0, 1000000))
        turb_gen = OpenSimplex(seed=random.randint(0, 1000000))
        
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
                nx = x / width * scale * frequency
                ny = y / height * scale * frequency
                
                h = v = 0
                amplitude = 1.0
                freq = 1.0
                
                for _ in range(octaves):
                    h_val = self.apply_turbulence(
                        noise_h.noise2(nx * freq, ny * freq),
                        nx * freq, ny * freq, turbulence, turb_gen
                    )
                    v_val = self.apply_turbulence(
                        noise_v.noise2(nx * freq, ny * freq),
                        nx * freq, ny * freq, turbulence, turb_gen
                    )
                    
                    h += h_val * amplitude
                    v += v_val * amplitude
                    amplitude *= persistence
                    freq *= 2
                
                h = (h + 1) / 2
                v = ((v + 1) / 2) * 0.8 + 0.2
                
                result[y, x] = hsv_to_rgb(h, saturation, v)
        
        return result

    def generate_prismatic(self, width, height, scale, octaves, persistence, turbulence, frequency):
        base_noise = OpenSimplex(seed=random.randint(0, 1000000))
        turb_gen = OpenSimplex(seed=random.randint(0, 1000000))
        result = np.zeros((height, width, 3))
        
        for y in range(height):
            for x in range(width):
                value = 0
                amplitude = 1.0
                freq = 1.0
                
                for o in range(octaves):
                    nx = x / width * scale * freq * frequency
                    ny = y / height * scale * freq * frequency
                    
                    noise_val = self.apply_turbulence(
                        base_noise.noise2(nx, ny),
                        nx, ny, turbulence, turb_gen
                    )
                    value += noise_val * amplitude
                    amplitude *= persistence
                    freq *= 2
                
                hue = (value + 1) / 2
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

    def generate_polychromatic_cellular(self, width, height, scale, octaves, persistence, turbulence):
        result = np.zeros((height, width, 3))
        num_points = 20 * scale
        points = np.random.rand(int(num_points), 2)
        colors = np.random.rand(int(num_points), 3)
        turb_gen = OpenSimplex(seed=random.randint(0, 1000000))
        
        for y in range(height):
            for x in range(width):
                px = x / width
                py = y / height
                
                # Apply turbulence to sampling position
                if turbulence > 0:
                    turb_x = self.apply_turbulence(px, px * 2, py * 2, turbulence, turb_gen)
                    turb_y = self.apply_turbulence(py, px * 2, py * 2, turbulence, turb_gen)
                    px = turb_x
                    py = turb_y
                
                distances = np.sqrt(((points - [px, py]) ** 2).sum(axis=1))
                closest_idx = np.argpartition(distances, 2)[:2]
                d1, d2 = distances[closest_idx]
                t = d1 / (d1 + d2)
                result[y, x] = colors[closest_idx[0]] * (1-t) + colors[closest_idx[1]] * t
        return result

    def generate_rainbow_fractal(self, width, height, scale, octaves, persistence, turbulence, frequency):
        result = np.zeros((height, width, 3))
        noise_gen = OpenSimplex(seed=random.randint(0, 1000000))
        turb_gen = OpenSimplex(seed=random.randint(0, 1000000))
        
        for y in range(height):
            for x in range(width):
                value = 0
                amplitude = 1.0
                freq = 1.0
                
                for o in range(octaves):
                    nx = x / width * scale * freq * frequency
                    ny = y / height * scale * freq * frequency
                    
                    noise_val = self.apply_turbulence(
                        noise_gen.noise2(nx, ny),
                        nx, ny, turbulence, turb_gen
                    )
                    value += noise_val * amplitude
                    amplitude *= persistence
                    freq *= 2.5
                
                angle = np.arctan2(value, amplitude) + np.pi
                hue = (angle / (2 * np.pi) + value) % 1.0
                
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

    def generate_color_wavelet(self, width, height, scale, octaves, persistence, turbulence, frequency):
        result = np.zeros((height, width, 3))
        noise_gens = [OpenSimplex(seed=random.randint(0, 1000000)) for _ in range(3)]
        turb_gen = OpenSimplex(seed=random.randint(0, 1000000))
        
        for y in range(height):
            for x in range(width):
                for c in range(3):
                    value = 0
                    amplitude = 1.0
                    freq = 1.0
                    phase = c * 2 * np.pi / 3
                    
                    for o in range(octaves):
                        nx = x / width * scale * freq * frequency
                        ny = y / height * scale * freq * frequency
                        
                        base_value = (noise_gens[c].noise2(nx, ny) * 
                                    np.sin(freq * phase + nx * 2 * np.pi))
                        
                        # Apply turbulence
                        turbulent_value = self.apply_turbulence(
                            base_value, nx, ny, turbulence, turb_gen
                        )
                        
                        value += turbulent_value * amplitude
                        amplitude *= persistence
                        freq *= 2
                    
                    result[y, x, c] = (value + 1) / 2
        return result

    def generate_noise(self, width, height, noise_type, scale=1.0, octaves=4, 
                      persistence=0.5, turbulence=0.5, frequency=1.0, saturation=1.0,
                      red_balance=1.0, green_balance=1.0, blue_balance=1.0, seed=-1):
        if seed != -1:
            np.random.seed(seed)
            random.seed(seed)
            
        # Generate noise based on selected type
        if noise_type == "Plasma":
            noise = self.generate_plasma(width, height, scale, octaves, persistence, turbulence, frequency)
        elif noise_type == "Perlin RGB":
            noise = self.generate_perlin_rgb(width, height, scale, octaves, persistence, turbulence, frequency)
        elif noise_type == "HSV Noise":
            noise = self.generate_hsv_noise(width, height, scale, octaves, persistence, turbulence, frequency, saturation)
        elif noise_type == "RGB Turbulence":
            noise = self.generate_rgb_turbulence(width, height, scale, octaves, persistence, turbulence, frequency)
        elif noise_type == "Prismatic":
            noise = self.generate_prismatic(width, height, scale, octaves, persistence, turbulence, frequency)
        elif noise_type == "Polychromatic Cellular":
            noise = self.generate_polychromatic_cellular(width, height, scale, octaves, persistence, turbulence)
        elif noise_type == "Rainbow Fractal":
            noise = self.generate_rainbow_fractal(width, height, scale, octaves, persistence, turbulence, frequency)
        elif noise_type == "Color Wavelet":
            noise = self.generate_color_wavelet(width, height, scale, octaves, persistence, turbulence, frequency)
        else:
            noise = self.generate_plasma(width, height, scale, octaves, persistence, turbulence, frequency)
        
        # Apply color balance
        noise[:,:,0] *= red_balance
        noise[:,:,1] *= green_balance
        noise[:,:,2] *= blue_balance
        
        # Ensure values are in valid range
        noise = np.clip(noise, 0, 1)
        
        # Convert to tensor in ComfyUI format (B,H,W,C)
        noise = noise.astype(np.float32)
        noise_tensor = torch.from_numpy(noise)
        
        # Ensure shape is (B,H,W,C)
        if len(noise_tensor.shape) == 3:
            noise_tensor = noise_tensor.unsqueeze(0)
        
        # Double check dimensions are correct
        if noise_tensor.shape[3] != 3:
            noise_tensor = noise_tensor.permute(0, 2, 3, 1)
            
        return (noise_tensor,)

# Node registration for ComfyUI
NODE_CLASS_MAPPINGS = {
    "NoiseFactoryV2": NoiseFactoryV2
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "NoiseFactoryV2": "Noise Factory V2"
}
