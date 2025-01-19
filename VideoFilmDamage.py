import numpy as np
import torch
import cv2
import random
import math

class VideoFilmDamage:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),  # Batch of images input
                "damage_preset": (["none", "light", "medium", "heavy", "severe", "custom"], {
                    "default": "medium"
                }),
                "scratch_density": ("FLOAT", {
                    "default": 0.3,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.05
                }),
                "scratch_width_scale": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 5.0,
                    "step": 0.1
                }),
                "dust_amount": ("FLOAT", {
                    "default": 0.2,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.05
                }),
                "dust_size_scale": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 5.0,
                    "step": 0.1
                }),
                "deterioration_strength": ("FLOAT", {
                    "default": 0.25,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.05
                }),
                "time_variance": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.05
                }),
                "custom_expression": ("STRING", {
                    "default": "sin(t * 0.1) * 0.5 + 0.5",
                    "multiline": False
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_film_damage"
    CATEGORY = "image/effects"

    def evaluate_expression(self, expression, t):
        """Safely evaluate a mathematical expression with 't' as time variable"""
        # Create a safe dict with math functions
        safe_dict = {
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'exp': math.exp,
            'sqrt': math.sqrt,
            'pi': math.pi,
            't': t
        }
        try:
            return float(eval(expression, {"__builtins__": {}}, safe_dict))
        except:
            return 0.5  # Default value if expression is invalid

    def generate_scratches(self, height, width, density, seed, width_scale=1.0):
        """Generate vertical scratches with varying intensity"""
        np.random.seed(seed)
        scratch_mask = np.zeros((height, width), dtype=np.float32)
        
        # Scale scratch parameters based on image size
        longest_edge = max(width, height)
        base_thickness = max(1, int(longest_edge / 1000))  # Base thickness scaled with image size
        
        num_scratches = int(width * density * 0.1)
        for _ in range(num_scratches):
            x = np.random.randint(0, width)
            # Scale thickness based on image size and user parameter
            thickness = int(np.random.randint(base_thickness, base_thickness * 2) * width_scale)
            intensity = np.random.uniform(0.3, 1.0)
            
            # Create varying scratch pattern
            scratch_length = np.random.randint(height // 4, height)
            start_y = np.random.randint(0, height - scratch_length)
            
            for y in range(start_y, start_y + scratch_length):
                if 0 <= x < width:
                    for t in range(-thickness, thickness + 1):
                        if 0 <= x + t < width:
                            # Add some variation to the scratch intensity
                            var_intensity = intensity * (0.8 + 0.4 * np.random.random())
                            scratch_mask[y, x + t] = max(scratch_mask[y, x + t], var_intensity)
        
        return scratch_mask

    def add_dust_and_hair(self, image, amount, seed, size_scale=1.0):
        """Add dust particles and hair-like artifacts"""
        np.random.seed(seed)
        height, width = image.shape[:2]
        dust_mask = np.zeros((height, width), dtype=np.float32)
        
        # Scale parameters based on image size
        longest_edge = max(width, height)
        base_dust_size = max(1, int(longest_edge / 500))  # Base dust size scaled with image size
        base_hair_length = max(20, int(longest_edge / 20))  # Base hair length scaled with image size
        
        # Add dust particles
        num_particles = int(width * height * amount * 0.0001)
        for _ in range(num_particles):
            x = np.random.randint(0, width)
            y = np.random.randint(0, height)
            size = int(np.random.randint(base_dust_size, base_dust_size * 3) * size_scale)
            intensity = np.random.uniform(0.3, 0.8)
            
            cv2.circle(dust_mask, (x, y), size, intensity, -1)
        
        # Add hair-like artifacts
        num_hairs = int(width * amount * 0.02)
        for _ in range(num_hairs):
            points = []
            x = np.random.randint(0, width)
            y = np.random.randint(0, height)
            length = np.random.randint(base_hair_length // 2, base_hair_length)
            
            for i in range(length):
                points.append((x, y))
                x += np.random.randint(-2, 3)
                y += np.random.randint(-2, 3)
                x = min(max(x, 0), width - 1)
                y = min(max(y, 0), height - 1)
            
            if len(points) > 1:
                points = np.array(points)
                cv2.polylines(dust_mask, [points], False, np.random.uniform(0.3, 0.6), 1)
        
        return dust_mask

    def apply_chemical_deterioration(self, image, strength, seed):
        """Simulate chemical deterioration and color fading"""
        np.random.seed(seed)
        height, width = image.shape[:2]
        
        # Create deterioration pattern
        pattern = np.zeros((height, width), dtype=np.float32)
        
        # Generate organic-looking deterioration using Perlin-like noise
        scale = 20
        for y in range(height):
            for x in range(width):
                nx = x / width * scale
                ny = y / height * scale
                value = np.sin(nx) * np.cos(ny) * np.sin(nx * 0.5) * np.cos(ny * 0.5)
                pattern[y, x] = (value + 1) * 0.5

        # Apply deterioration
        deteriorated = image.copy()
        pattern = cv2.GaussianBlur(pattern, (7, 7), 0)
        
        # Affect different color channels differently
        for c in range(3):
            channel_effect = pattern * strength * np.random.uniform(0.8, 1.2)
            # Apply the effect directly using numpy operations instead of cv2.addWeighted
            channel_pattern = (255 * channel_effect).astype(np.float32)
            deteriorated[..., c] = deteriorated[..., c].astype(np.float32) * (1 - channel_effect * 0.5) + channel_pattern * 0.5
        
        return deteriorated

    def get_preset_values(self, preset):
        """Get parameter values for different presets"""
        # Format: (scratch_density, dust_amount, deterioration_strength, time_variance, scratch_width_scale, dust_size_scale)
        presets = {
            "none": (0.0, 0.0, 0.0, 0.0, 1.0, 1.0),
            "light": (0.1, 0.1, 0.1, 0.2, 0.8, 0.8),
            "medium": (0.3, 0.2, 0.25, 0.5, 1.0, 1.0),
            "heavy": (0.6, 0.4, 0.5, 0.7, 1.2, 1.2),
            "severe": (0.8, 0.6, 0.8, 1.0, 1.5, 1.5),
        }
        return presets.get(preset, None)

    def apply_film_damage(self, images, damage_preset, scratch_density, scratch_width_scale,
                         dust_amount, dust_size_scale, deterioration_strength, time_variance, 
                         custom_expression):
        # Convert from torch tensor to numpy array
        batch_numpy = images.cpu().numpy()
        batch_size, height, width, channels = batch_numpy.shape
        
        # Get preset values if not using custom
        if damage_preset != "custom":
            preset_values = self.get_preset_values(damage_preset)
            if preset_values:
                (scratch_density, dust_amount, deterioration_strength, time_variance,
                 scratch_width_scale, dust_size_scale) = preset_values
        
        # Process each image in the batch
        processed_batch = np.zeros_like(batch_numpy)
        for i in range(batch_size):
            # Convert to float32 for processing
            frame = (batch_numpy[i] * 255).astype(np.float32)
            
            # Calculate time-based variation
            if damage_preset != "none":
                t = i / max(1, batch_size - 1)  # Normalized time from 0 to 1
                if damage_preset == "custom":
                    variation = self.evaluate_expression(custom_expression, t)
                else:
                    variation = 0.5 + 0.5 * math.sin(t * math.pi * 2)  # Simple sinusoidal variation
                
                # Apply time variance
                current_scratch = scratch_density * (1 + variation * time_variance - time_variance/2)
                current_dust = dust_amount * (1 + variation * time_variance - time_variance/2)
                current_deterioration = deterioration_strength * (1 + variation * time_variance - time_variance/2)
                
                # Generate frame-specific seed
                frame_seed = i * 1000 + int(t * 1000)
                
                # Apply effects
                if current_scratch > 0:
                    scratch_mask = self.generate_scratches(height, width, current_scratch, frame_seed, scratch_width_scale)
                    frame = frame * (1 - scratch_mask[..., np.newaxis])
                
                if current_dust > 0:
                    dust_mask = self.add_dust_and_hair(frame, current_dust, frame_seed + 1, dust_size_scale)
                    frame = frame * (1 - dust_mask[..., np.newaxis])
                
                if current_deterioration > 0:
                    frame = self.apply_chemical_deterioration(frame, current_deterioration, frame_seed + 2)
            
            # Normalize and store result
            processed_batch[i] = np.clip(frame, 0, 255) / 255.0
        
        # Convert back to torch tensor
        return (torch.from_numpy(processed_batch).to(images.device),)

NODE_CLASS_MAPPINGS = {
    "VideoFilmDamage": VideoFilmDamage
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VideoFilmDamage": "Film Damage Effect"
}
