import torch
import numpy as np
from typing import Tuple, Dict
from scipy.ndimage import map_coordinates

class FishEyeV2:
    # Lens presets based on common focal lengths
    LENS_PRESETS = {
        "14MM Ultra Wide": {"distortion": 0.35, "falloff": 3.0, "vignette": 0.3},
        "24MM Wide": {"distortion": 0.2, "falloff": 2.5, "vignette": 0.2},
        "35MM Standard": {"distortion": 0.1, "falloff": 2.0, "vignette": 0.15},
        "50MM Normal": {"distortion": 0.05, "falloff": 1.8, "vignette": 0.1},
        "85MM Portrait": {"distortion": 0.02, "falloff": 1.5, "vignette": 0.08},
        "100MM Telephoto": {"distortion": 0.01, "falloff": 1.3, "vignette": 0.05},
        "200MM Super Telephoto": {"distortion": 0.005, "falloff": 1.1, "vignette": 0.03},
        "Custom": {"distortion": 0.0, "falloff": 2.0, "vignette": 0.0}
    }

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
                "lens_preset": (list(s.LENS_PRESETS.keys()),),
                "fisheye_mode": ("BOOLEAN", {"default": False}),
                "custom_distortion": ("FLOAT", {
                    "default": 0.0,
                    "min": -1.0,
                    "max": 1.0,
                    "step": 0.01,
                    "display": "slider"
                }),
                "focus_distance": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 10.0,
                    "step": 0.1,
                    "display": "slider"
                }),
                "vignette_strength": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "display": "slider"
                }),
                "chromatic_aberration": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 0.02,
                    "step": 0.001,
                    "display": "slider"
                }),
                "bokeh_blur": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "display": "slider"
                })
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_lens_effect"
    CATEGORY = "image/effects"

    def create_lens_distortion_map(
        self,
        height: int,
        width: int,
        preset_values: Dict,
        fisheye_mode: bool,
        custom_distortion: float,
        focus_distance: float
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Create coordinate maps for lens distortion.
        """
        # Create normalized coordinate grid
        x = np.linspace(-1, 1, width)
        y = np.linspace(-1, 1, height)
        x_grid, y_grid = np.meshgrid(x, y)

        # Calculate polar coordinates
        r = np.sqrt(x_grid**2 + y_grid**2)
        theta = np.arctan2(y_grid, x_grid)

        # Get base distortion from preset
        base_distortion = preset_values["distortion"]
        
        # Combine preset and custom distortion
        if custom_distortion != 0:
            total_distortion = base_distortion + custom_distortion
        else:
            total_distortion = base_distortion

        # Apply different distortion models based on mode
        if fisheye_mode:
            # Fish-eye projection (equidistant)
            r_distorted = r * (1 + total_distortion * (r ** preset_values["falloff"]))
        else:
            # Regular lens distortion (polynomial)
            r_distorted = r * (1 + total_distortion * r + 0.1 * total_distortion * (r ** 3))

        # Apply focus distance effect
        focal_plane = 1.0 / focus_distance
        depth_factor = np.clip(1 - (r * focal_plane), 0, 1)
        r_distorted = r_distorted * (1 - depth_factor) + r * depth_factor

        # Convert back to Cartesian coordinates
        x_map = r_distorted * np.cos(theta)
        y_map = r_distorted * np.sin(theta)

        # Normalize and convert to pixel coordinates
        x_map = np.clip(x_map, -1, 1)
        y_map = np.clip(y_map, -1, 1)
        x_map = (x_map + 1) * (width - 1) / 2
        y_map = (y_map + 1) * (height - 1) / 2

        return x_map, y_map

    def apply_vignette(self, image: np.ndarray, strength: float) -> np.ndarray:
        """
        Apply vignette effect to the image.
        """
        height, width = image.shape[:2]
        x = np.linspace(-1, 1, width)
        y = np.linspace(-1, 1, height)
        x_grid, y_grid = np.meshgrid(x, y)
        
        # Calculate radial distance from center
        r = np.sqrt(x_grid**2 + y_grid**2)
        
        # Create vignette mask
        vignette = 1 - (r ** 2) * strength
        vignette = np.clip(vignette, 0, 1)
        
        # Apply vignette
        return image * vignette[..., np.newaxis]

    def apply_bokeh_blur(self, image: np.ndarray, strength: float, focus_distance: float) -> np.ndarray:
        """
        Apply depth-dependent bokeh blur effect.
        """
        if strength == 0:
            return image

        height, width = image.shape[:2]
        x = np.linspace(-1, 1, width)
        y = np.linspace(-1, 1, height)
        x_grid, y_grid = np.meshgrid(x, y)
        r = np.sqrt(x_grid**2 + y_grid**2)

        # Calculate blur amount based on distance from focus plane
        focal_plane = 1.0 / focus_distance
        blur_amount = np.abs(r - focal_plane) * strength
        
        # Apply gaussian blur with varying kernel sizes
        from scipy.ndimage import gaussian_filter
        blurred = np.zeros_like(image)
        for i in range(3):  # Process each color channel
            blurred[..., i] = gaussian_filter(image[..., i], sigma=blur_amount)
        
        return blurred

    def apply_lens_effect(
        self,
        images: torch.Tensor,
        lens_preset: str,
        fisheye_mode: bool,
        custom_distortion: float,
        focus_distance: float,
        vignette_strength: float,
        chromatic_aberration: float,
        bokeh_blur: float
    ) -> Tuple[torch.Tensor]:
        """
        Apply lens effects to a batch of images.
        """
        # Get preset values
        preset_values = self.LENS_PRESETS[lens_preset]
        
        # Convert to numpy for processing
        device = images.device
        batch_numpy = images.cpu().numpy()
        batch_size, height, width, channels = batch_numpy.shape

        # Create distortion maps
        x_map, y_map = self.create_lens_distortion_map(
            height, width, preset_values, fisheye_mode,
            custom_distortion, focus_distance
        )

        # Process each image in the batch
        processed_batch = np.zeros_like(batch_numpy)
        for i in range(batch_size):
            current_image = batch_numpy[i]

            # Apply main lens distortion
            distorted = np.zeros_like(current_image)
            if chromatic_aberration > 0:
                # Apply chromatic aberration with different offsets per channel
                for c in range(channels):
                    offset = (c - 1) * chromatic_aberration * width
                    x_offset = x_map + offset
                    distorted[..., c] = map_coordinates(
                        current_image[..., c],
                        [y_map, x_offset],
                        order=1
                    )
            else:
                # Apply uniform distortion
                for c in range(channels):
                    distorted[..., c] = map_coordinates(
                        current_image[..., c],
                        [y_map, x_map],
                        order=1
                    )

            # Apply bokeh blur
            if bokeh_blur > 0:
                distorted = self.apply_bokeh_blur(distorted, bokeh_blur, focus_distance)

            # Apply vignette
            final_vignette = preset_values["vignette"] + vignette_strength
            if final_vignette > 0:
                distorted = self.apply_vignette(distorted, final_vignette)

            processed_batch[i] = distorted

        # Convert back to torch tensor
        return (torch.from_numpy(processed_batch).to(device),)

NODE_CLASS_MAPPINGS = {
    "FishEyeV2": FishEyeV2
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FishEyeV2": "Fish Eye Effects V2"
}