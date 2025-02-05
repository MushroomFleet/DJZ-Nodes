"""
@author: Combined node based on FilmGrainEffect_v2 and NoiseFactoryV2
VideoNoiseFactory - Generates animated noise patterns with film grain effects
"""

import numpy as np
import torch
from PIL import Image
import random
from opensimplex import OpenSimplex
import re
import math
from typing import Tuple

class VideoNoiseFactory:
    """A ComfyUI node that generates animated noise patterns with film grain effects"""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "width": ("INT", {"default": 512, "min": 64, "max": 4096}),
                "height": ("INT", {"default": 512, "min": 64, "max": 4096}),
                "num_frames": ("INT", {"default": 24, "min": 1, "max": 1000}),
                # Noise pattern parameters
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
                "noise_scale": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 10.0, "step": 0.1}),
                "octaves": ("INT", {"default": 4, "min": 1, "max": 8}),
                "persistence": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.05}),
                "turbulence": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 2.0, "step": 0.1}),
                "frequency": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 5.0, "step": 0.1}),
                "saturation": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.1}),
                # Film grain parameters
                "grain_preset": (["custom", "subtle", "vintage", "unstable_signal", "dip", "ebb", "flow"], {
                    "default": "subtle"
                }),
                "grain_expression": ("STRING", {
                    "default": "0.08 * normal(0.5, 0.15) * (1 + 0.2 * sin(t/25))",
                    "multiline": True
                }),
                "base_intensity": ("FLOAT", {
                    "default": 0.1,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01
                }),
                "time_scale": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 10.0,
                    "step": 0.1
                }),
                "grain_scale": ("FLOAT", {
                    "default": 0.2,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01
                }),
                # Color balance
                "red_balance": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.1}),
                "green_balance": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.1}),
                "blue_balance": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.1}),
                # Seeds
                "noise_seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffff}),
                "grain_seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffff})
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate_video_noise"
    CATEGORY = "image/generation"

    # Preset expressions for different grain patterns
    GRAIN_PRESETS = {
        'unstable_signal': "0.15 * normal(0.5, 0.3) * (1 + 0.5 * sin(t/5)) + 0.1 * sin(t/3) * exp(-t/20) + 0.05 * uniform(-1, 1)",
        'dip': "0.1 * (1 - exp(-((t % 60) - 30)**2 / 100)) * normal(0.5, 0.2)",
        'ebb': "0.12 * (sin(t/20) * 0.5 + 0.5) * normal(0.5, 0.15) * (1 + 0.3 * sin(t/7))",
        'flow': "0.1 * (1 + 0.4 * sin(t/15)) * normal(0.6, 0.2) * (1 + 0.2 * sin(t/3))",
        'vintage': "0.15 * normal(0.5, 0.25) * (1 + 0.3 * sin(t/12)) + 0.05 * exp(-t/40)",
        'subtle': "0.08 * normal(0.5, 0.15) * (1 + 0.2 * sin(t/25))"
    }

    def safe_eval(self, expr: str, t: float, rng: np.random.RandomState) -> float:
        """Safely evaluate a mathematical expression with limited functions."""
        safe_dict = {
            'sin': math.sin,
            'cos': math.cos,
            'exp': math.exp,
            'abs': abs,
            'pow': pow,
            't': t,
            'pi': math.pi,
            'e': math.e,
            'normal': lambda mu, sigma: rng.normal(mu, sigma),
            'uniform': lambda a, b: rng.uniform(a, b)
        }
        
        try:
            clean_expr = re.sub(r'[^0-9+\-*/%()., \t\nabcdefghijklmnopqrstuvwxyzπ_]', '', expr)
            return float(eval(clean_expr, {"__builtins__": {}}, safe_dict))
        except Exception as e:
            print(f"Error evaluating expression: {e}")
            return 0.0

    def apply_turbulence(self, value, nx, ny, turbulence, noise_gen):
        """Apply turbulence distortion to the noise value"""
        if turbulence <= 0:
            return value
        
        turb = noise_gen.noise2(nx * 2, ny * 2) * turbulence
        displaced_x = nx + turb
        displaced_y = ny + turb
        turbulent_value = noise_gen.noise2(displaced_x, displaced_y)
        return value * (1 - turbulence) + turbulent_value * turbulence

    def apply_grain_to_frame(
        self,
        image: np.ndarray,
        frame_number: int,
        base_intensity: float,
        grain_scale: float,
        time_scale: float,
        rng: np.random.RandomState,
        grain_preset: str,
        expression: str
    ) -> np.ndarray:
        """Apply film grain to a single frame."""
        t = frame_number * time_scale
        
        if grain_preset == 'custom':
            intensity = base_intensity * self.safe_eval(expression, t, rng)
        else:
            preset_expr = self.GRAIN_PRESETS.get(grain_preset, self.GRAIN_PRESETS['subtle'])
            intensity = base_intensity * self.safe_eval(preset_expr, t, rng)

        noise = rng.normal(0, grain_scale, image.shape)
        grainy_image = image + intensity * noise
        return np.clip(grainy_image, 0, 1)

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
                        
                        base_noise = (noise_generators[c*2].noise2(nx, ny) * 
                                    noise_generators[c*2+1].noise2(ny, nx))
                        
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
                        
                        turbulent_value = self.apply_turbulence(
                            base_value, nx, ny, turbulence, turb_gen
                        )
                        
                        value += turbulent_value * amplitude
                        amplitude *= persistence
                        freq *= 2
                    
                    result[y, x, c] = (value + 1) / 2
        return result

    def generate_video_noise(
        self,
        width: int,
        height: int,
        num_frames: int,
        noise_type: str,
        noise_scale: float,
        octaves: int,
        persistence: float,
        turbulence: float,
        frequency: float,
        saturation: float,
        grain_preset: str,
        grain_expression: str,
        base_intensity: float,
        time_scale: float,
        grain_scale: float,
        red_balance: float,
        green_balance: float,
        blue_balance: float,
        noise_seed: int,
        grain_seed: int
    ) -> Tuple[torch.Tensor]:
        """Generate animated noise with film grain effects."""
        
        # Initialize random generators
        noise_rng = np.random.RandomState(noise_seed)
        grain_rng = np.random.RandomState(grain_seed)
        random.seed(noise_seed)  # For OpenSimplex noise
        
        # Prepare batch of frames
        batch = np.zeros((num_frames, height, width, 3), dtype=np.float32)
        
        # Generate base noise frames
        for frame in range(num_frames):
            # Generate noise frame
            if noise_type == "Plasma":
                noise = self.generate_plasma(width, height, noise_scale, octaves, persistence, turbulence, frequency)
            elif noise_type == "RGB Turbulence":
                noise = self.generate_rgb_turbulence(width, height, noise_scale, octaves, persistence, turbulence, frequency)
            elif noise_type == "Prismatic":
                noise = self.generate_prismatic(width, height, noise_scale, octaves, persistence, turbulence, frequency)
            elif noise_type == "HSV Noise":
                noise = self.generate_hsv_noise(width, height, noise_scale, octaves, persistence, turbulence, frequency, saturation)
            elif noise_type == "Perlin RGB":
                noise = self.generate_perlin_rgb(width, height, noise_scale, octaves, persistence, turbulence, frequency)
            elif noise_type == "Polychromatic Cellular":
                noise = self.generate_polychromatic_cellular(width, height, noise_scale, octaves, persistence, turbulence)
            elif noise_type == "Rainbow Fractal":
                noise = self.generate_rainbow_fractal(width, height, noise_scale, octaves, persistence, turbulence, frequency)
            elif noise_type == "Color Wavelet":
                noise = self.generate_color_wavelet(width, height, noise_scale, octaves, persistence, turbulence, frequency)
            else:
                noise = self.generate_plasma(width, height, noise_scale, octaves, persistence, turbulence, frequency)
            
            # Apply color balance
            noise[:,:,0] *= red_balance
            noise[:,:,1] *= green_balance
            noise[:,:,2] *= blue_balance
            
            # Apply film grain
            noise = self.apply_grain_to_frame(
                noise, frame,
                base_intensity, grain_scale,
                time_scale, grain_rng,
                grain_preset, grain_expression
            )
            
            batch[frame] = noise

        # Convert to tensor
        return (torch.from_numpy(batch),)

# Node registration
NODE_CLASS_MAPPINGS = {
    "VideoNoiseFactory": VideoNoiseFactory
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VideoNoiseFactory": "Video Noise Factory"
}