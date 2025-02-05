import numpy as np
import torch
import cv2
from math import *  # For custom expression evaluation

class CathodeRayEffect:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
                "preset": (["static", "fluctuating", "degraded", "custom"], {"default": "static"}),
                "custom_expression": ("STRING", {
                    "default": "sin(t/10) * 0.1 + 0.2",
                    "multiline": False
                }),
                "screen_curvature": ("FLOAT", {
                    "default": 0.2,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01
                }),
                "scanline_intensity": ("FLOAT", {
                    "default": 0.3,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01
                }),
                "glow_amount": ("FLOAT", {
                    "default": 0.2,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01
                }),
                "color_bleeding": ("FLOAT", {
                    "default": 0.15,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01
                }),
                "noise_amount": ("FLOAT", {
                    "default": 0.05,
                    "min": 0.0,
                    "max": 0.5,
                    "step": 0.01
                }),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_effect"
    CATEGORY = "image/effects"

    def create_time_variation(self, preset, custom_expr, frame_idx, batch_size):
        t = frame_idx % batch_size  # Time variable for expressions
        
        if preset == "static":
            return 1.0
        elif preset == "fluctuating":
            return 0.8 + 0.2 * sin(t / 5)
        elif preset == "degraded":
            return max(0.5, 1.0 - t / (batch_size * 2))
        elif preset == "custom":
            try:
                return eval(custom_expr)
            except:
                return 1.0

    def apply_screen_curvature(self, image, amount):
        rows, cols = image.shape[:2]
        
        # Create displacement maps
        X, Y = np.meshgrid(np.linspace(-1, 1, cols), np.linspace(-1, 1, rows))
        R = np.sqrt(X**2 + Y**2)
        displacement = (1 + amount * R**2)
        
        map_x = cols/2 + (X * cols/2) / displacement
        map_y = rows/2 + (Y * rows/2) / displacement
        
        return cv2.remap(image, map_x.astype(np.float32), map_y.astype(np.float32), 
                        cv2.INTER_LINEAR)

    def apply_scanlines(self, image, intensity, variation):
        height = image.shape[0]
        scanline_pattern = np.ones(height)
        scanline_pattern[::2] = 1.0 - (intensity * variation)
        return image * scanline_pattern.reshape(-1, 1, 1)

    def apply_glow(self, image, amount, variation):
        blur_size = int(31 * amount * variation)
        if blur_size % 2 == 0:
            blur_size += 1
        return cv2.GaussianBlur(image, (blur_size, blur_size), 0)

    def apply_color_bleeding(self, image, amount, variation):
        kernel_size = int(max(3, 15 * amount * variation))
        if kernel_size % 2 == 0:
            kernel_size += 1
            
        kernel = np.zeros((kernel_size, 1))
        kernel[:kernel_size//2 + 1, 0] = np.linspace(1, 0, kernel_size//2 + 1)
        kernel = kernel / kernel.sum()
        
        channels = cv2.split(image)
        result_channels = []
        
        for i, channel in enumerate(channels):
            shifted_kernel = np.roll(kernel, i - 1, axis=0)
            result_channels.append(cv2.filter2D(channel, -1, shifted_kernel))
            
        return cv2.merge(result_channels)

    def apply_noise(self, image, amount, variation):
        noise = np.random.normal(0, amount * variation * 255, image.shape)
        return np.clip(image + noise, 0, 255).astype(np.uint8)

    def apply_effect(self, images, preset, custom_expression, screen_curvature, 
                    scanline_intensity, glow_amount, color_bleeding, noise_amount):
        
        batch_numpy = images.cpu().numpy()
        batch_size = batch_numpy.shape[0]
        processed_batch = np.zeros_like(batch_numpy)
        
        for i in range(batch_size):
            # Calculate time-based variation
            variation = self.create_time_variation(preset, custom_expression, i, batch_size)
            
            # Convert to uint8 for processing
            frame = (batch_numpy[i] * 255).astype(np.uint8)
            
            # Apply effects
            frame = self.apply_screen_curvature(frame, screen_curvature * variation)
            frame = self.apply_glow(frame, glow_amount, variation)
            frame = self.apply_color_bleeding(frame, color_bleeding, variation)
            frame = self.apply_noise(frame, noise_amount, variation)
            frame = self.apply_scanlines(frame, scanline_intensity, variation)
            
            # Normalize back to float32
            processed_batch[i] = np.clip(frame, 0, 255).astype(np.float32) / 255.0
        
        return (torch.from_numpy(processed_batch).to(images.device),)

NODE_CLASS_MAPPINGS = {
    "CathodeRayEffect": CathodeRayEffect
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CathodeRayEffect": "Cathode Ray Effect"
}