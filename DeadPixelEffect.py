import numpy as np
import torch
import cv2
from enum import Enum

class PixelDefectMode(Enum):
    DEAD_BLACK = 0
    DEAD_WHITE = 1
    STUCK_COLOR = 2
    HOT_PIXEL = 3
    SUBPIXEL = 4
    CLUSTER = 5

class DeadPixelEffect:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
                "defect_mode": (["DEAD_BLACK", "DEAD_WHITE", "STUCK_COLOR", "HOT_PIXEL", "SUBPIXEL", "CLUSTER"],),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 0xffffffffffffffff
                }),
                "defect_rate": ("FLOAT", {
                    "default": 0.001,
                    "min": 0.0001,
                    "max": 0.1,
                    "step": 0.0001,
                }),
                "cluster_size": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 10,
                    "step": 1,
                }),
                "color_intensity": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.1,
                }),
                "flicker_rate": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.1,
                }),
                "subpixel_mode": (["RED", "GREEN", "BLUE", "RANDOM"],),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_dead_pixel_effect"
    CATEGORY = "image/effects"

    def generate_defect_mask(self, height, width, defect_rate, cluster_size, rng):
        total_pixels = height * width
        n_defects = int(total_pixels * defect_rate)
        mask = np.zeros((height, width), dtype=bool)

        for _ in range(n_defects):
            y = rng.integers(0, height - cluster_size)
            x = rng.integers(0, width - cluster_size)
            mask[y:y+cluster_size, x:x+cluster_size] = True

        return mask

    def apply_defect(self, image, mask, mode, color_intensity, subpixel_mode, rng):
        result = image.copy()
        
        if mode == PixelDefectMode.DEAD_BLACK:
            result[mask] = 0
        elif mode == PixelDefectMode.DEAD_WHITE:
            result[mask] = 1
        elif mode == PixelDefectMode.STUCK_COLOR:
            color = rng.random(3) * color_intensity
            result[mask] = color
        elif mode == PixelDefectMode.HOT_PIXEL:
            result[mask] = rng.random(3) * color_intensity + (1 - color_intensity)
        elif mode == PixelDefectMode.SUBPIXEL:
            channel = {"RED": 0, "GREEN": 1, "BLUE": 2, "RANDOM": rng.integers(0, 3)}[subpixel_mode]
            result[mask, channel] = 1
        elif mode == PixelDefectMode.CLUSTER:
            for _ in range(3):
                result[mask, rng.integers(0, 3)] = rng.random() * color_intensity

        return result

    def apply_dead_pixel_effect(self, images, defect_mode, seed, defect_rate, cluster_size, 
                               color_intensity, flicker_rate, subpixel_mode):
        # Initialize random number generator with seed
        base_rng = np.random.default_rng(seed)
        
        batch_numpy = images.cpu().numpy()
        batch_size, height, width, channels = batch_numpy.shape
        processed_batch = np.zeros_like(batch_numpy)
        
        print(f"Processing {batch_size} images with {defect_mode} defects (seed: {seed})...")
        mode = PixelDefectMode[defect_mode]
        
        # Generate consistent defect mask for non-flickering pixels using base seed
        base_mask = self.generate_defect_mask(
            height, width, 
            defect_rate * (1 - flicker_rate), 
            cluster_size,
            base_rng
        )
        
        for i in range(batch_size):
            # Generate frame-specific RNG for flickering based on base seed
            frame_rng = np.random.default_rng(base_rng.integers(0, 2**32))
            
            # Generate additional random defects for flickering
            flicker_mask = self.generate_defect_mask(
                height, width,
                defect_rate * flicker_rate,
                cluster_size,
                frame_rng
            )
            
            combined_mask = base_mask | flicker_mask
            
            processed_batch[i] = self.apply_defect(
                batch_numpy[i], 
                combined_mask, 
                mode,
                color_intensity,
                subpixel_mode,
                frame_rng
            )
            
            print(f"Processed image {i+1}/{batch_size}")
        
        return (torch.from_numpy(processed_batch).to(images.device),)

NODE_CLASS_MAPPINGS = {
    "DeadPixelEffect": DeadPixelEffect
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DeadPixelEffect": "Dead Pixel Effect"
}