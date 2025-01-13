import torch
import numpy as np
import cv2
from typing import Tuple, Dict
from dataclasses import dataclass

@dataclass
class FilmStock:
    """Represents characteristics of different film stocks"""
    name: str
    color_temp: int
    contrast: float
    saturation: float
    highlight_rolloff: float
    shadow_rolloff: float
    grain_size: float

class ClassicFilmEffect:
    """ComfyUI node for applying classic film effects to image sequences"""
    
    FILM_STOCKS = {
        'kodachrome64': FilmStock(
            name='Kodachrome 64',
            color_temp=6500,
            contrast=1.08,
            saturation=1.1,
            highlight_rolloff=0.95,
            shadow_rolloff=0.92,
            grain_size=0.3
        ),
        'trix400': FilmStock(
            name='Tri-X 400',
            color_temp=5500,
            contrast=1.12,
            saturation=0.0,  # B&W film
            highlight_rolloff=0.9,
            shadow_rolloff=0.85,
            grain_size=0.5
        ),
        'portra400': FilmStock(
            name='Portra 400',
            color_temp=5900,
            contrast=1.02,
            saturation=1.02,
            highlight_rolloff=0.98,
            shadow_rolloff=0.95,
            grain_size=0.4
        ),
        'velvia50': FilmStock(
            name='Fuji Velvia 50',
            color_temp=5500,
            contrast=1.15,
            saturation=1.15,
            highlight_rolloff=0.92,
            shadow_rolloff=0.9,
            grain_size=0.25  # Very fine grain
        ),
        'hp5plus': FilmStock(
            name='Ilford HP5 Plus',
            color_temp=5500,
            contrast=1.08,
            saturation=0.0,  # B&W film
            highlight_rolloff=0.92,
            shadow_rolloff=0.88,
            grain_size=0.45
        ),
        'ektachrome100': FilmStock(
            name='Ektachrome E100',
            color_temp=6200,
            contrast=1.05,
            saturation=1.05,
            highlight_rolloff=0.96,
            shadow_rolloff=0.94,
            grain_size=0.3
        ),
        'pro400h': FilmStock(
            name='Fuji Pro 400H',
            color_temp=5800,
            contrast=1.0,
            saturation=1.04,
            highlight_rolloff=0.98,
            shadow_rolloff=0.96,
            grain_size=0.35
        ),
        'delta3200': FilmStock(
            name='Ilford Delta 3200',
            color_temp=5500,
            contrast=1.15,
            saturation=0.0,  # B&W film
            highlight_rolloff=0.85,
            shadow_rolloff=0.8,
            grain_size=0.7  # Pronounced grain
        ),
        'cinestill800t': FilmStock(
            name='Cinestill 800T',
            color_temp=3200,  # Tungsten-balanced
            contrast=1.05,
            saturation=1.08,
            highlight_rolloff=0.94,
            shadow_rolloff=0.9,
            grain_size=0.5
        )
    }

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),  # Batch of images input
                "film_stock": (list(s.FILM_STOCKS.keys()), {
                    "default": "portra400"
                }),
                "grain_intensity": ("FLOAT", {
                    "default": 0.04,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01
                }),
                "vignette_strength": ("FLOAT", {
                    "default": 0.1,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01
                }),
                "scratch_probability": ("FLOAT", {
                    "default": 0.02,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01
                }),
                "dust_density": ("FLOAT", {
                    "default": 0.001,
                    "min": 0.0,
                    "max": 0.1,
                    "step": 0.001
                }),
                "halation_strength": ("FLOAT", {
                    "default": 0.05,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01
                }),
                "enable_jitter": ("BOOLEAN", {
                    "default": True,
                }),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 2147483647  # 2**31 - 1, safe value for numpy RandomState
                })
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_film_effect"
    CATEGORY = "image/effects"

    def adjust_color_temperature(self, image: np.ndarray, target_temp: int, 
                               current_temp: int = 6500) -> np.ndarray:
        """Adjust color temperature of the image using a more gradual approach"""
        ratio = (target_temp / current_temp) ** 0.5  # Softened ratio
        
        # Split channels
        b, g, r = cv2.split(image)
        
        # Apply smoother adjustments
        if ratio > 1:  # Warming
            r = np.clip(r + (ratio - 1) * 0.5, 0, 1)
            b = np.clip(b - (ratio - 1) * 0.5, 0, 1)
        else:  # Cooling
            r = np.clip(r - (1 - ratio) * 0.5, 0, 1)
            b = np.clip(b + (1 - ratio) * 0.5, 0, 1)
            
        return cv2.merge([b, g, r])

    def add_film_grain(self, image: np.ndarray, intensity: float, 
                      rng: np.random.RandomState) -> np.ndarray:
        """Add film grain effect"""
        noise = rng.normal(0, intensity, image.shape)
        grainy = image + noise
        return np.clip(grainy, 0, 1)

    def add_vignette(self, image: np.ndarray, strength: float) -> np.ndarray:
        """Add vignette effect"""
        height, width = image.shape[:2]
        
        # Create radial gradient
        Y, X = np.ogrid[:height, :width]
        center_y, center_x = height/2, width/2
        radius = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
        
        # Normalize radius
        max_radius = np.sqrt(center_x**2 + center_y**2)
        normalized_radius = radius / max_radius
        
        # Create vignette mask
        mask = 1 - normalized_radius * strength
        mask = np.clip(mask, 0, 1)
        
        # Apply vignette
        if len(image.shape) == 3:
            mask = np.dstack([mask] * image.shape[2])
        return image * mask

    def add_scratches(self, image: np.ndarray, probability: float,
                     rng: np.random.RandomState) -> np.ndarray:
        """Add vertical scratches that scale with image width"""
        height, width = image.shape[:2]
        result = image.copy()
        
        # Scale scratch width with image size
        min_scratch_width = max(1, int(width * 0.0005))  # 0.05% of width
        max_scratch_width = max(2, int(width * 0.001))   # 0.1% of width
        
        num_scratches = int(width * probability)
        for _ in range(num_scratches):
            x = rng.randint(0, width)
            intensity = rng.uniform(0.3, 0.7)
            scratch_width = rng.randint(min_scratch_width, max_scratch_width + 1)
            scratch = np.ones((height, scratch_width)) * intensity
            
            if len(image.shape) == 3:
                scratch = np.dstack([scratch] * image.shape[2])
            
            # Calculate scratch position with width-aware bounds
            start_x = max(0, x - scratch_width // 2)
            end_x = min(width, start_x + scratch_width)
            
            # Blend the scratch with existing image
            alpha = rng.uniform(0.3, 0.7)  # Vary scratch visibility
            result[:, start_x:end_x] = result[:, start_x:end_x] * (1 - alpha) + scratch[:, :end_x-start_x] * alpha
            
        return result

    def add_dust(self, image: np.ndarray, density: float,
                rng: np.random.RandomState) -> np.ndarray:
        """Add dust and specs that scale with image dimensions"""
        height, width = image.shape[:2]
        dust = np.zeros_like(image)
        
        # Calculate base size relative to image dimensions
        base_size = max(1, int(min(width, height) * 0.001))  # 0.1% of smallest dimension
        
        num_particles = int(width * height * density)
        for _ in range(num_particles):
            x = rng.randint(0, width)
            y = rng.randint(0, height)
            
            # Scale dust size relative to image
            size = rng.randint(base_size, int(base_size * 2))
            intensity = rng.uniform(0.5, 0.8)  # Reduced intensity for subtlety
            
            # Create dust particle with gaussian falloff
            y1 = max(0, y-size)
            y2 = min(height, y+size)
            x1 = max(0, x-size)
            x2 = min(width, x+size)
            
            # Create gaussian falloff for more natural looking dust
            yy, xx = np.ogrid[y1:y2, x1:x2]
            dist = np.sqrt((xx - x)**2 + (yy - y)**2)
            falloff = np.exp(-(dist**2)/(2*(size/3)**2))
            
            if len(image.shape) == 3:
                falloff = np.dstack([falloff] * image.shape[2])
            
            dust[y1:y2, x1:x2] = np.maximum(dust[y1:y2, x1:x2], falloff * intensity)
            
        return np.clip(image + dust * 0.7, 0, 1)  # Blend more subtly

    def apply_jitter(self, image: np.ndarray, rng: np.random.RandomState
                    ) -> np.ndarray:
        """Apply random frame jitter"""
        height, width = image.shape[:2]
        
        # Random displacement
        dx = rng.randint(-3, 4)
        dy = rng.randint(-3, 4)
        
        # Create translation matrix
        M = np.float32([[1, 0, dx], [0, 1, dy]])
        
        # Apply transformation
        if len(image.shape) == 3:
            result = np.zeros_like(image)
            for c in range(image.shape[2]):
                result[:,:,c] = cv2.warpAffine(image[:,:,c], M, (width, height))
        else:
            result = cv2.warpAffine(image, M, (width, height))
            
        return result

    def add_halation(self, image: np.ndarray, strength: float) -> np.ndarray:
        """Add halation (highlight bloom) effect"""
        # Extract highlights
        highlights = np.mean(image, axis=2) if len(image.shape) == 3 else image
        highlights = np.clip((highlights - 0.7) * 3.3, 0, 1)
        
        # Create blur
        blur_size = max(3, int(min(image.shape[:2]) * 0.03))
        if blur_size % 2 == 0:
            blur_size += 1
            
        blurred = cv2.GaussianBlur(image, (blur_size, blur_size), 0)
        
        # Blend based on highlights
        if len(image.shape) == 3:
            highlights = np.dstack([highlights] * image.shape[2])
        return image + (blurred - image) * highlights * strength

    def adjust_tone_curve(self, image: np.ndarray, highlight_rolloff: float,
                         shadow_rolloff: float) -> np.ndarray:
        """Apply tone curve adjustments with smoother transitions"""
        # Create high-resolution lookup table for smoother gradients
        x = np.linspace(0, 1, 1024)
        y = x.copy()
        
        # Create smooth transition points
        mid_point = 0.5
        transition_width = 0.1
        
        # Smooth highlight transition
        highlight_mask = x > (mid_point - transition_width)
        highlight_factor = np.clip((x[highlight_mask] - (mid_point - transition_width)) / (2 * transition_width), 0, 1)
        y[highlight_mask] = (x[highlight_mask] * (1 - highlight_factor) + 
                           (mid_point + (x[highlight_mask] - mid_point) * highlight_rolloff) * highlight_factor)
        
        # Smooth shadow transition
        shadow_mask = x < (mid_point + transition_width)
        shadow_factor = np.clip(((mid_point + transition_width) - x[shadow_mask]) / (2 * transition_width), 0, 1)
        y[shadow_mask] = (x[shadow_mask] * (1 - shadow_factor) + 
                         (x[shadow_mask] * shadow_rolloff) * shadow_factor)
        
        # Apply tone curve with high precision
        result = np.zeros_like(image)
        if len(image.shape) == 3:
            for c in range(image.shape[2]):
                result[:,:,c] = np.interp(image[:,:,c], x, y)
        else:
            result = np.interp(image, x, y)
            
        return result

    def apply_film_effect(
        self,
        images: torch.Tensor,
        film_stock: str,
        grain_intensity: float,
        vignette_strength: float,
        scratch_probability: float,
        dust_density: float,
        halation_strength: float,
        enable_jitter: bool,
        seed: int
    ) -> Tuple[torch.Tensor]:
        """
        Apply film effect to a batch of images
        """
        # Convert from torch tensor to numpy array
        batch_numpy = images.cpu().numpy()
        
        # Initialize RNG
        rng = np.random.RandomState(seed)
        
        # Get film stock parameters
        stock = self.FILM_STOCKS[film_stock]
        
        # Process each image in the batch
        processed_batch = np.zeros_like(batch_numpy)
        for i in range(len(batch_numpy)):
            image = batch_numpy[i]
            
            # Apply film stock characteristics with floating-point precision
            result = self.adjust_color_temperature(image, stock.color_temp)
            
            # Apply contrast in floating point
            result = np.clip((result - 0.5) * stock.contrast + 0.5, 0, 1)
            
            # Apply saturation with smoother transitions
            if stock.saturation > 0:
                # Convert to HSV while preserving floating point precision
                hsv = cv2.cvtColor((result * 255).astype(np.uint8), cv2.COLOR_RGB2HSV).astype(np.float32) / 255.0
                hsv[:,:,1] = np.clip(hsv[:,:,1] * stock.saturation, 0, 1)
                # Convert back to RGB
                result = cv2.cvtColor((hsv * 255).astype(np.uint8), cv2.COLOR_HSV2RGB).astype(np.float32) / 255.0
            else:
                # Convert to black and white with proper weighting
                result = np.clip(0.2989 * result[:,:,0] + 0.5870 * result[:,:,1] + 0.1140 * result[:,:,2], 0, 1)
                result = np.stack([result] * 3, axis=-1)
            
            # Apply effects
            result = self.add_film_grain(result, 
                                       grain_intensity * stock.grain_size, rng)
            result = self.add_vignette(result, vignette_strength)
            result = self.add_scratches(result, scratch_probability, rng)
            result = self.add_dust(result, dust_density, rng)
            result = self.add_halation(result, halation_strength)
            
            if enable_jitter:
                result = self.apply_jitter(result, rng)
            
            # Apply tone curve
            result = self.adjust_tone_curve(result, 
                                          stock.highlight_rolloff,
                                          stock.shadow_rolloff)
            
            processed_batch[i] = result
        
        # Convert back to torch tensor
        return (torch.from_numpy(processed_batch).to(images.device),)

NODE_CLASS_MAPPINGS = {
    "ClassicFilmEffect": ClassicFilmEffect
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ClassicFilmEffect": "Classic Film Effect"
}
