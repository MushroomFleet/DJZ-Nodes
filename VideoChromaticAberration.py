import numpy as np
import torch
import cv2
import random
import math

class VideoChromaticAberration:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),  # Batch of images input
                "red_offset_x": ("FLOAT", {
                    "default": 5.0,
                    "min": -50.0,
                    "max": 50.0,
                    "step": 0.5,
                }),
                "red_offset_y": ("FLOAT", {
                    "default": 0.0,
                    "min": -50.0,
                    "max": 50.0,
                    "step": 0.5,
                }),
                "blue_offset_x": ("FLOAT", {
                    "default": -5.0,
                    "min": -50.0,
                    "max": 50.0,
                    "step": 0.5,
                }),
                "blue_offset_y": ("FLOAT", {
                    "default": 0.0,
                    "min": -50.0,
                    "max": 50.0,
                    "step": 0.5,
                }),
                "animation_preset": (["none", "custom", "pulse", "broken_lighting", "wave", "random_jitter", "strobe"],),
                "custom_expression": ("STRING", {
                    "default": "sin(t * 2 * pi) * intensity",
                    "multiline": False
                }),
                "animation_speed": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 10.0,
                    "step": 0.1
                }),
                "effect_intensity": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 5.0,
                    "step": 0.1
                }),
                "chromatic_blur": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 10.0,
                    "step": 0.1
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_chromatic_aberration"
    CATEGORY = "image/effects"

    def evaluate_time_expression(self, expression, t, intensity):
        """Evaluates custom mathematical expressions for time-based effects"""
        # Define allowed mathematical functions and constants
        safe_dict = {
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'pi': math.pi,
            'abs': abs,
            'pow': pow,
            't': t,
            'intensity': intensity
        }
        try:
            return eval(expression, {"__builtins__": {}}, safe_dict)
        except:
            return 1.0  # Default multiplier if expression fails

    def get_animation_multiplier(self, preset, frame_idx, total_frames, speed, intensity, custom_expr):
        """Calculate the animation multiplier based on the selected preset"""
        t = (frame_idx / max(1, total_frames - 1)) * speed * 2 * math.pi
        
        if preset == "none":
            return 1.0
        elif preset == "custom":
            return self.evaluate_time_expression(custom_expr, t, intensity)
        elif preset == "pulse":
            return abs(math.sin(t)) * intensity
        elif preset == "broken_lighting":
            return (1.0 + random.random() * math.sin(t * 3)) * intensity
        elif preset == "wave":
            return (1.0 + math.sin(t) * 0.5) * intensity
        elif preset == "random_jitter":
            return (1.0 + (random.random() - 0.5) * 0.3) * intensity
        elif preset == "strobe":
            return (1.0 if math.sin(t * 2) > 0 else 0.2) * intensity
        return 1.0

    def apply_channel_offset(self, image, offset_x, offset_y, channel_idx, blur_amount):
        """Apply offset to a specific color channel with optional blur"""
        height, width = image.shape[:2]
        channel = image[:, :, channel_idx].copy()
        
        if blur_amount > 0:
            blur_size = int(blur_amount * 2) * 2 + 1
            channel = cv2.GaussianBlur(channel, (blur_size, blur_size), blur_amount)

        M = np.float32([[1, 0, offset_x], [0, 1, offset_y]])
        shifted = cv2.warpAffine(channel, M, (width, height), borderMode=cv2.BORDER_REFLECT)
        
        return shifted

    def apply_chromatic_aberration(self, images, red_offset_x, red_offset_y, 
                                 blue_offset_x, blue_offset_y, animation_preset,
                                 custom_expression, animation_speed, effect_intensity,
                                 chromatic_blur):
        
        # Convert from torch tensor to numpy array
        batch_numpy = images.cpu().numpy()
        batch_size, height, width, channels = batch_numpy.shape
        
        # Process each image in the batch
        processed_batch = np.zeros_like(batch_numpy)
        for i in range(batch_size):
            # Get animation multiplier for current frame
            multiplier = self.get_animation_multiplier(
                animation_preset, i, batch_size,
                animation_speed, effect_intensity,
                custom_expression
            )
            
            # Convert to float32 for processing
            frame = (batch_numpy[i] * 255).astype(np.float32)
            
            # Process each channel separately
            r_channel = self.apply_channel_offset(
                frame,
                red_offset_x * multiplier,
                red_offset_y * multiplier,
                0,  # Red channel
                chromatic_blur
            )
            
            g_channel = frame[:, :, 1]  # Green channel stays centered
            
            b_channel = self.apply_channel_offset(
                frame,
                blue_offset_x * multiplier,
                blue_offset_y * multiplier,
                2,  # Blue channel
                chromatic_blur
            )
            
            # Merge channels
            processed_frame = np.dstack((r_channel, g_channel, b_channel))
            
            # Normalize and store
            processed_batch[i] = np.clip(processed_frame, 0, 255) / 255.0

        # Convert back to torch tensor
        return (torch.from_numpy(processed_batch).to(images.device),)

NODE_CLASS_MAPPINGS = {
    "VideoChromaticAberration": VideoChromaticAberration
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VideoChromaticAberration": "Video Chromatic Aberration"
}