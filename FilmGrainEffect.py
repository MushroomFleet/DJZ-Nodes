import numpy as np
import torch
import cv2
from PIL import Image
from typing import Tuple

class FilmGrainEffect:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),  # Batch of images input
                "preset": (["subtle", "vintage", "unstable_signal", "dip", "ebb", "flow"], {
                    "default": "subtle"
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
                "noise_scale": ("FLOAT", {
                    "default": 0.2,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01
                }),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 0xffffffffffffffff
                })
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_film_grain"
    CATEGORY = "image/effects"

    # Preset expressions for different grain patterns
    PRESETS = {
        'unstable_signal': (
            "0.15 * normal(0.5, 0.3) * (1 + 0.5 * sin(t/5)) + "
            "0.1 * sin(t/3) * exp(-t/100 % 20) + "
            "0.05 * uniform(-1, 1) * sin(t/7)**2"
        ),
        'dip': (
            "0.1 * (1 - exp(-((t % 60) - 30)**2 / 100)) * "
            "normal(0.5, 0.2)"
        ),
        'ebb': (
            "0.12 * (sin(t/20) * 0.5 + 0.5) * "
            "normal(0.5, 0.15) * (1 + 0.3 * sin(t/7))"
        ),
        'flow': (
            "0.1 * (1 + 0.4 * sin(t/15)) * "
            "normal(0.6, 0.2) * (1 + 0.2 * sin(t/3))"
        ),
        'vintage': (
            "0.15 * normal(0.5, 0.25) * (1 + 0.3 * sin(t/12)) + "
            "0.05 * exp(-(t % 40)/10)"
        ),
        'subtle': (
            "0.08 * normal(0.5, 0.15) * (1 + 0.2 * sin(t/25))"
        )
    }

    def apply_grain_to_frame(
        self,
        image: np.ndarray,
        frame_number: int,
        base_intensity: float,
        noise_scale: float,
        time_scale: float,
        rng: np.random.RandomState,
        preset: str
    ) -> np.ndarray:
        """
        Apply film grain to a single frame.
        
        Args:
            image: Input image as numpy array (float32, range 0-1)
            frame_number: Current frame number
            base_intensity: Base intensity of the grain effect
            noise_scale: Scale of the noise pattern
            time_scale: Scale factor for temporal effects
            rng: Random number generator
            preset: Name of the preset pattern to use
        
        Returns:
            Processed image with film grain applied
        """
        # Calculate time-varying intensity based on preset pattern
        t = frame_number * time_scale
        
        # Simplified preset patterns (without expression parsing)
        if preset == 'subtle':
            intensity = base_intensity * (1 + 0.2 * np.sin(t/25))
        elif preset == 'vintage':
            intensity = base_intensity * (1 + 0.3 * np.sin(t/12) + 0.05 * np.exp(-(t % 40)/10))
        elif preset == 'unstable_signal':
            intensity = base_intensity * (1 + 0.5 * np.sin(t/5) + 0.1 * np.sin(t/3))
        elif preset == 'dip':
            intensity = base_intensity * (1 - np.exp(-((t % 60) - 30)**2 / 100))
        elif preset == 'ebb':
            intensity = base_intensity * (np.sin(t/20) * 0.5 + 0.5) * (1 + 0.3 * np.sin(t/7))
        elif preset == 'flow':
            intensity = base_intensity * (1 + 0.4 * np.sin(t/15)) * (1 + 0.2 * np.sin(t/3))
        else:
            intensity = base_intensity

        # Generate noise pattern
        noise = rng.normal(0, noise_scale, image.shape)
        
        # Apply noise to image
        grainy_image = image + intensity * noise
        
        # Clip values to valid range
        grainy_image = np.clip(grainy_image, 0, 1)
        
        return grainy_image

    def apply_film_grain(
        self,
        images: torch.Tensor,
        preset: str,
        base_intensity: float,
        time_scale: float,
        noise_scale: float,
        seed: int
    ) -> Tuple[torch.Tensor]:
        """
        Apply film grain effect to a batch of images.
        
        Args:
            images: Input tensor of shape (B, H, W, C)
            preset: Name of the grain pattern preset
            base_intensity: Base intensity of the grain effect
            time_scale: Scale factor for temporal variations
            noise_scale: Scale of the noise pattern
            seed: Random seed for reproducibility
        
        Returns:
            Tuple containing the processed tensor
        """
        # Convert from torch tensor to numpy array
        batch_numpy = images.cpu().numpy()
        batch_size, height, width, channels = batch_numpy.shape
        
        # Initialize random number generator
        rng = np.random.RandomState(seed)
        
        # Process each image in the batch
        processed_batch = np.zeros_like(batch_numpy)
        for i in range(batch_size):
            # Apply film grain effect
            processed_batch[i] = self.apply_grain_to_frame(
                batch_numpy[i],
                frame_number=i,
                base_intensity=base_intensity,
                noise_scale=noise_scale,
                time_scale=time_scale,
                rng=rng,
                preset=preset
            )
        
        # Convert back to torch tensor
        return (torch.from_numpy(processed_batch).to(images.device),)

NODE_CLASS_MAPPINGS = {
    "FilmGrainEffect": FilmGrainEffect
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FilmGrainEffect": "Film Grain Effect (video)"
}