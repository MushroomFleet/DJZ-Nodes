import numpy as np
import torch
import cv2
import random

class LensLeaks:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),  # Batch of images input
                "effect_mode": (["lens_leaks", "lens_flares"],),  # Mode selector
                "intensity": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.05,
                }),
                "leak_color": (["warm", "cool", "rainbow"],),  # Color temperature of leaks
                "num_leaks": ("INT", {
                    "default": 3,
                    "min": 1,
                    "max": 10,
                    "step": 1,
                }),
                "leak_size": ("FLOAT", {
                    "default": 0.3,
                    "min": 0.1,
                    "max": 1.0,
                    "step": 0.05,
                }),
                "chromatic_aberration": ("FLOAT", {
                    "default": 0.2,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.05,
                }),
                "bloom_radius": ("INT", {
                    "default": 50,
                    "min": 10,
                    "max": 200,
                    "step": 10,
                }),
                "flare_position": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.1,
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_lens_effects"
    CATEGORY = "image/effects"

    def create_leak_mask(self, height, width, num_leaks, leak_size, color_mode):
        mask = np.zeros((height, width, 3), dtype=np.float32)
        
        for _ in range(num_leaks):
            # Random position for leak
            x = random.randint(0, width)
            y = random.randint(0, height)
            
            # Create radial gradient
            Y, X = np.ogrid[:height, :width]
            dist_from_center = np.sqrt((X - x)**2 + (Y - y)**2)
            
            # Size of the leak
            radius = int(min(height, width) * leak_size)
            
            # Create gradient falloff
            gradient = np.clip(1 - (dist_from_center / radius), 0, 1)
            
            # Apply color based on mode
            if color_mode == "warm":
                color = np.array([0.8, 0.4, 0.2])  # Warm orange
            elif color_mode == "cool":
                color = np.array([0.2, 0.4, 0.8])  # Cool blue
            else:  # rainbow
                angle = np.arctan2(Y - y, X - x)
                hue = (angle + np.pi) / (2 * np.pi)
                # Convert HSV to RGB
                color = cv2.cvtColor(np.uint8([[[hue * 180, 255, 255]]]), cv2.COLOR_HSV2RGB)[0][0] / 255.0
            
            # Apply color to mask
            for c in range(3):
                mask[:, :, c] += gradient * color[c]
        
        return np.clip(mask, 0, 1)

    def apply_chromatic_aberration(self, image, shift_amount):
        height, width = image.shape[:2]
        
        # Split into channels
        b, g, r = cv2.split(image)
        
        # Calculate shifts for red and blue channels
        shift_x = int(width * shift_amount * 0.02)
        shift_y = int(height * shift_amount * 0.02)
        
        # Create transformation matrices
        M_red = np.float32([[1, 0, shift_x], [0, 1, shift_y]])
        M_blue = np.float32([[1, 0, -shift_x], [0, 1, -shift_y]])
        
        # Apply shifts
        r = cv2.warpAffine(r, M_red, (width, height))
        b = cv2.warpAffine(b, M_blue, (width, height))
        
        # Merge channels back
        return cv2.merge([b, g, r])

    def create_lens_flare(self, height, width, position, intensity):
        # Create base flare
        flare = np.zeros((height, width, 3), dtype=np.float32)
        
        # Calculate flare position
        center_x = int(width * position)
        center_y = int(height * 0.5)
        
        # Create main flare
        Y, X = np.ogrid[:height, :width]
        dist_from_center = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
        
        # Create multiple flare components
        components = [
            {'radius': 50, 'intensity': 1.0, 'color': [1.0, 0.8, 0.6]},  # Main flare
            {'radius': 30, 'intensity': 0.7, 'color': [0.8, 0.8, 1.0]},  # Secondary flare
            {'radius': 70, 'intensity': 0.3, 'color': [1.0, 0.6, 0.4]}   # Outer glow
        ]
        
        for comp in components:
            radius = comp['radius']
            gradient = np.exp(-(dist_from_center**2) / (2 * radius**2))
            for c in range(3):
                flare[:, :, c] += gradient * comp['color'][c] * comp['intensity'] * intensity
        
        return np.clip(flare, 0, 1)

    def apply_bloom(self, image, radius):
        # Apply Gaussian blur for bloom effect
        bloom = cv2.GaussianBlur(image, (0, 0), radius)
        return cv2.addWeighted(image, 1.0, bloom, 0.3, 0)

    def apply_lens_effects(self, images, effect_mode, intensity, leak_color, 
                         num_leaks, leak_size, chromatic_aberration, 
                         bloom_radius, flare_position):
        
        # Convert from torch tensor to numpy array
        batch_numpy = images.cpu().numpy()
        batch_size, height, width, channels = batch_numpy.shape
        
        # Process each image in the batch
        processed_batch = np.zeros_like(batch_numpy)
        for i in range(batch_size):
            # Convert to BGR for processing
            frame = (batch_numpy[i] * 255).astype(np.uint8)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            
            # Apply effects based on mode
            if effect_mode == "lens_leaks":
                # Create and apply leak mask
                leak_mask = self.create_leak_mask(height, width, num_leaks, 
                                                leak_size, leak_color)
                frame = cv2.addWeighted(frame, 1.0, (leak_mask * 255).astype(np.uint8), 
                                      intensity, 0)
            
            else:  # lens_flares
                # Create and apply lens flare
                flare = self.create_lens_flare(height, width, flare_position, 
                                             intensity)
                frame = cv2.addWeighted(frame, 1.0, (flare * 255).astype(np.uint8), 
                                      1.0, 0)
            
            # Apply common effects
            if chromatic_aberration > 0:
                frame = self.apply_chromatic_aberration(frame, chromatic_aberration)
            
            if bloom_radius > 0:
                frame = self.apply_bloom(frame, bloom_radius)
            
            # Convert back to RGB and normalize
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            processed_batch[i] = frame.astype(np.float32) / 255.0
        
        # Convert back to torch tensor
        return (torch.from_numpy(processed_batch).to(images.device),)

NODE_CLASS_MAPPINGS = {
    "LensLeaks": LensLeaks
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LensLeaks": "Lens Leaks & Flares"
}