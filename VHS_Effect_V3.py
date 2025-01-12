import numpy as np
import torch
import cv2
import random
from enum import Enum
import math
import os

class VHSSpeed(Enum):
    VHS_SP = (2400000.0, 320000.0, 9)
    VHS_LP = (1900000.0, 300000.0, 12)
    VHS_EP = (1400000.0, 280000.0, 14)
    
    def __init__(self, luma_cut, chroma_cut, chroma_delay):
        self.luma_cut = luma_cut
        self.chroma_cut = chroma_cut
        self.chroma_delay = chroma_delay

class VHS_Effect_V3:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
                # Base VHS parameters from V2
                "tape_speed": (["SP", "LP", "EP"],),
                "composite_preemphasis": ("FLOAT", {
                    "default": 4.0,
                    "min": 0.0,
                    "max": 8.0,
                    "step": 0.1
                }),
                # New horizontal noise line parameters
                "noise_line_intensity": ("FLOAT", {
                    "default": 0.8,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.1
                }),
                "noise_line_thickness": ("INT", {
                    "default": 2,
                    "min": 1,
                    "max": 10,
                    "step": 1
                }),
                "noise_line_count": ("INT", {
                    "default": 1,
                    "min": 0,
                    "max": 5,
                    "step": 1
                }),
                # Shifting distortion parameters
                "distortion_bands": ("INT", {
                    "default": 3,
                    "min": 0,
                    "max": 10,
                    "step": 1
                }),
                "max_band_offset": ("INT", {
                    "default": 10,
                    "min": 0,
                    "max": 30,
                    "step": 1
                }),
                # Color bleeding parameters
                "color_bleed_strength": ("FLOAT", {
                    "default": 0.3,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.1
                }),
                "color_bleed_offset": ("INT", {
                    "default": 2,
                    "min": 1,
                    "max": 5,
                    "step": 1
                }),
                # Enhancement parameters
                "sharpen_amount": ("FLOAT", {
                    "default": 1.5,
                    "min": 1.0,
                    "max": 3.0,
                    "step": 0.1
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_vhs_effect"
    CATEGORY = "image/effects"

    def add_horizontal_noise_lines(self, img_array, thickness, intensity, count):
        """Add multiple horizontal noise lines to the image."""
        height, width, channels = img_array.shape
        
        for _ in range(count):
            position = random.randint(0, height - thickness)
            noise = np.random.random((thickness, width, channels)) * 255 * intensity
            
            blend_factor = 0.7
            img_array[position:position+thickness] = (
                img_array[position:position+thickness] * (1 - blend_factor) +
                noise * blend_factor
            ).astype(np.uint8)
        
        return img_array

    def add_shifting_distortion(self, img_array, num_bands, max_offset):
        """Add horizontal shifting distortion bands."""
        height, width, channels = img_array.shape
        
        for _ in range(num_bands):
            band_height = random.randint(5, 20)
            band_position = random.randint(0, height - band_height)
            offset = random.randint(-max_offset, max_offset)
            
            if offset > 0:
                img_array[band_position:band_position+band_height, offset:] = \
                    img_array[band_position:band_position+band_height, :-offset]
                noise = np.random.random((band_height, offset, channels)) * 255
                img_array[band_position:band_position+band_height, :offset] = noise.astype(np.uint8)
            elif offset < 0:
                img_array[band_position:band_position+band_height, :offset] = \
                    img_array[band_position:band_position+band_height, -offset:]
                noise = np.random.random((band_height, -offset, channels)) * 255
                img_array[band_position:band_position+band_height, offset:] = noise.astype(np.uint8)
        
        return img_array

    def add_color_bleeding(self, img_array, strength, offset):
        """Simulate color bleeding/ghosting effect."""
        r, g, b = img_array[:,:,0], img_array[:,:,1], img_array[:,:,2]
        
        # Shift red channel to the right
        r_shift = np.roll(r, offset, axis=1)
        # Shift blue channel to the left
        b_shift = np.roll(b, -offset, axis=1)
        
        # Blend shifted channels with original
        r = (r * (1 - strength) + r_shift * strength).astype(np.uint8)
        b = (b * (1 - strength) + b_shift * strength).astype(np.uint8)
        
        return np.stack([r, g, b], axis=2)

    def apply_tape_speed_effects(self, img_array, speed):
        """Apply blur based on tape speed."""
        kernel_size = {
            VHSSpeed.VHS_SP: 3,
            VHSSpeed.VHS_LP: 5,
            VHSSpeed.VHS_EP: 7
        }[speed]
        
        if kernel_size > 1:
            img_array = cv2.GaussianBlur(img_array, (kernel_size, 1), 0)
        
        return img_array

    def apply_sharpening(self, img_array, amount):
        """Apply sharpening to the image."""
        if amount > 1.0:
            kernel_size = (3, 3)
            sigma = 1.0
            blurred = cv2.GaussianBlur(img_array, kernel_size, sigma)
            img_array = cv2.addWeighted(img_array, amount, blurred, -(amount - 1.0), 0)
        
        return np.clip(img_array, 0, 255).astype(np.uint8)

    def process_frame(self, frame, params):
        """Process a single frame with all VHS effects."""
        # Convert to proper format for processing
        frame = frame.astype(np.float32)
        
        # Apply tape speed effects first
        frame = self.apply_tape_speed_effects(frame, params["tape_speed"])
        
        # Apply horizontal noise lines
        frame = self.add_horizontal_noise_lines(
            frame,
            params["noise_line_thickness"],
            params["noise_line_intensity"],
            params["noise_line_count"]
        )
        
        # Apply shifting distortion
        frame = self.add_shifting_distortion(
            frame,
            params["distortion_bands"],
            params["max_band_offset"]
        )
        
        # Apply color bleeding
        frame = self.add_color_bleeding(
            frame,
            params["color_bleed_strength"],
            params["color_bleed_offset"]
        )
        
        # Final sharpening
        frame = self.apply_sharpening(frame, params["sharpen_amount"])
        
        return frame

    def apply_vhs_effect(self, images, tape_speed, composite_preemphasis,
                        noise_line_intensity, noise_line_thickness, noise_line_count,
                        distortion_bands, max_band_offset,
                        color_bleed_strength, color_bleed_offset,
                        sharpen_amount):
        """Main entry point for the node."""
        batch_numpy = images.cpu().numpy()
        batch_size, height, width, channels = batch_numpy.shape
        
        params = {
            "tape_speed": getattr(VHSSpeed, f"VHS_{tape_speed}"),
            "composite_preemphasis": composite_preemphasis,
            "noise_line_thickness": noise_line_thickness,
            "noise_line_intensity": noise_line_intensity,
            "noise_line_count": noise_line_count,
            "distortion_bands": distortion_bands,
            "max_band_offset": max_band_offset,
            "color_bleed_strength": color_bleed_strength,
            "color_bleed_offset": color_bleed_offset,
            "sharpen_amount": sharpen_amount
        }
        
        processed_batch = np.zeros_like(batch_numpy)
        for i in range(batch_size):
            frame = (batch_numpy[i] * 255).astype(np.uint8)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            
            frame = self.process_frame(frame, params)
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            processed_batch[i] = frame.astype(np.float32) / 255.0
        
        return (torch.from_numpy(processed_batch).to(images.device),)

NODE_CLASS_MAPPINGS = {
    "VHS_Effect_V3": VHS_Effect_V3
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VHS_Effect_V3": "VHS Effect v3"
}