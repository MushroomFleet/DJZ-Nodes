import torch
import numpy as np
from typing import Tuple

class FishEyeEffect:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),  # Batch of images input
                "distortion_strength": ("FLOAT", {
                    "default": 0.2,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.005,
                    "display": "slider"
                }),
                "barrel_vs_pincushion": ("FLOAT", {
                    "default": 0.0,
                    "min": -1.0,
                    "max": 1.0,
                    "step": 0.01,
                    "display": "slider"
                }),
                "radial_falloff": ("FLOAT", {
                    "default": 2.0,
                    "min": 1.0,
                    "max": 4.0,
                    "step": 0.1,
                    "display": "slider"
                }),
                "edge_softness": ("FLOAT", {
                    "default": 0.1,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "display": "slider"
                }),
                "zoom": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.5,
                    "max": 2.0,
                    "step": 0.01,
                    "display": "slider"
                }),
                "spherical_aberration": ("FLOAT", {
                    "default": 0.0,
                    "min": -0.5,
                    "max": 0.5,
                    "step": 0.01,
                    "display": "slider"
                }),
                "chromatic_aberration": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 0.02,
                    "step": 0.001,
                    "display": "slider"
                })
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_fisheye"
    CATEGORY = "image/effects"

    def create_fisheye_map(self, height: int, width: int, strength: float, barrel_vs_pincushion: float,
                          radial_falloff: float, edge_softness: float, zoom: float, 
                          spherical_aberration: float) -> Tuple[np.ndarray, np.ndarray]:
        """
        Create coordinate maps for fisheye distortion.
        
        Args:
            height: Image height
            width: Image width
            strength: Distortion strength
            edge_softness: Softness of the edge falloff
            zoom: Zoom factor
            spherical_aberration: Amount of spherical aberration
            
        Returns:
            Tuple of coordinate maps (x_map, y_map)
        """
        # Create normalized coordinate grid
        x = np.linspace(-1, 1, width)
        y = np.linspace(-1, 1, height)
        x_grid, y_grid = np.meshgrid(x, y)

        # Calculate polar coordinates
        r = np.sqrt(x_grid**2 + y_grid**2)
        theta = np.arctan2(y_grid, x_grid)

        # Apply non-linear distortion with smooth falloff
        max_r = np.sqrt(2)  # Maximum radius (corner of image)
        normalized_r = r / max_r
        
        # Create smooth falloff at edges
        edge_mask = 1 - np.clip(normalized_r / (1 - edge_softness), 0, 1)
        
        # Apply spherical aberration
        aberration = spherical_aberration * (r**3)
        
        # Calculate distorted radius with more nuanced control
        # Blend between barrel (positive) and pincushion (negative) distortion
        barrel = r * (1 + strength * (r**radial_falloff))
        pincushion = r * (1 - strength * (r**radial_falloff))
        # Linear interpolation between barrel and pincushion distortion
        blend_factor = (barrel_vs_pincushion + 1) / 2  # Convert from [-1,1] to [0,1]
        r_distorted = barrel * (1 - blend_factor) + pincushion * blend_factor
        
        # Apply zoom and other effects
        r_distorted = r_distorted * zoom * edge_mask + aberration
        
        # Convert back to Cartesian coordinates
        x_map = r_distorted * np.cos(theta)
        y_map = r_distorted * np.sin(theta)
        
        # Normalize coordinates to [-1, 1]
        x_map = np.clip(x_map, -1, 1)
        y_map = np.clip(y_map, -1, 1)
        
        # Convert to pixel coordinates
        x_map = (x_map + 1) * (width - 1) / 2
        y_map = (y_map + 1) * (height - 1) / 2
        
        return x_map, y_map

    def apply_chromatic_aberration(self, image: torch.Tensor, x_map: np.ndarray, y_map: np.ndarray, 
                                 strength: float) -> torch.Tensor:
        """
        Apply chromatic aberration effect.
        
        Args:
            image: Input image tensor
            x_map: X coordinate map
            y_map: Y coordinate map
            strength: Chromatic aberration strength
            
        Returns:
            Image with chromatic aberration applied
        """
        height, width = image.shape[:2]
        
        # Create offset maps for red and blue channels
        x_map_r = x_map + strength * width
        x_map_b = x_map - strength * width
        
        # Ensure coordinates are within bounds
        x_map_r = np.clip(x_map_r, 0, width - 1)
        x_map_b = np.clip(x_map_b, 0, width - 1)
        y_map = np.clip(y_map, 0, height - 1)
        
        # Sample each color channel separately
        result = torch.zeros_like(image)
        result[..., 0] = torch.from_numpy(
            np.array([map_coordinates(image[..., 0].numpy(), [y_map, x_map_r], order=1)])
        )
        result[..., 1] = torch.from_numpy(
            np.array([map_coordinates(image[..., 1].numpy(), [y_map, x_map], order=1)])
        )
        result[..., 2] = torch.from_numpy(
            np.array([map_coordinates(image[..., 2].numpy(), [y_map, x_map_b], order=1)])
        )
        
        return result

    def apply_fisheye(
        self,
        images: torch.Tensor,
        distortion_strength: float,
        barrel_vs_pincushion: float,
        radial_falloff: float,
        edge_softness: float,
        zoom: float,
        spherical_aberration: float,
        chromatic_aberration: float
    ) -> Tuple[torch.Tensor]:
        """
        Apply fisheye effect to a batch of images.
        
        Args:
            images: Input tensor of shape (B, H, W, C)
            distortion_strength: Strength of the fisheye distortion
            edge_softness: Softness of the edge falloff
            zoom: Zoom factor
            spherical_aberration: Amount of spherical aberration
            chromatic_aberration: Strength of chromatic aberration
            
        Returns:
            Tuple containing the processed tensor
        """
        # Convert to numpy for processing
        device = images.device
        batch_numpy = images.cpu().numpy()
        batch_size, height, width, channels = batch_numpy.shape
        
        # Create coordinate maps for the fisheye distortion
        x_map, y_map = self.create_fisheye_map(
            height, width, distortion_strength, barrel_vs_pincushion,
            radial_falloff, edge_softness, zoom, spherical_aberration
        )
        
        # Process each image in the batch
        processed_batch = np.zeros_like(batch_numpy)
        for i in range(batch_size):
            # Apply main fisheye distortion
            if chromatic_aberration > 0:
                # Apply chromatic aberration
                processed_batch[i] = self.apply_chromatic_aberration(
                    torch.from_numpy(batch_numpy[i]),
                    x_map, y_map,
                    chromatic_aberration
                ).numpy()
            else:
                # Apply regular distortion without chromatic aberration
                for c in range(channels):
                    processed_batch[i, ..., c] = map_coordinates(
                        batch_numpy[i, ..., c],
                        [y_map, x_map],
                        order=1
                    )
        
        # Convert back to torch tensor
        return (torch.from_numpy(processed_batch).to(device),)

# Import scipy's map_coordinates here to avoid circular import
from scipy.ndimage import map_coordinates

NODE_CLASS_MAPPINGS = {
    "FishEyeEffect": FishEyeEffect
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FishEyeEffect": "Fish Eye Effect"
}
