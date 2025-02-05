import numpy as np
import torch
import cv2
import random

class KinescopeEffectV1:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),  # Batch of images input
                "black_and_white": ("BOOLEAN", {
                    "default": True,
                }),
                "contrast": ("FLOAT", {
                    "default": 1.2,
                    "min": 0.1,
                    "max": 3.0,
                    "step": 0.1,
                }),
                "brightness": ("FLOAT", {
                    "default": 1.1,
                    "min": 0.1,
                    "max": 3.0,
                    "step": 0.1,
                }),
                "film_grain": ("FLOAT", {
                    "default": 35.0,
                    "min": 0.0,
                    "max": 100.0,
                    "step": 1.0,
                }),
                "phosphor_persistence": ("FLOAT", {
                    "default": 0.3,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.1,
                }),
                "scanline_intensity": ("FLOAT", {
                    "default": 0.15,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.05,
                }),
                "edge_bleeding": ("FLOAT", {
                    "default": 1.5,
                    "min": 0.0,
                    "max": 5.0,
                    "step": 0.1,
                }),
                "vertical_blur": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 21,
                    "step": 2,
                }),
                "horizontal_blur": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 21,
                    "step": 2,
                }),
                "generations": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 5,
                    "step": 1,
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_kinescope_effect"
    CATEGORY = "image/effects"

    def add_film_grain(self, image, intensity):
        height, width = image.shape[:2]
        grain = np.random.normal(0, intensity, (height, width))
        grain = np.dstack([grain] * image.shape[2])
        noisy_image = np.clip(image + grain, 0, 255).astype(np.uint8)
        return noisy_image

    def apply_scanlines(self, image, intensity):
        height, width = image.shape[:2]
        scanlines = np.zeros((height, width), dtype=np.float32)
        scanlines[::2] = 1.0
        scanlines = 1.0 - (intensity * (1.0 - scanlines))
        scanlines = np.dstack([scanlines] * image.shape[2])
        return np.clip(image * scanlines, 0, 255).astype(np.uint8)

    def apply_phosphor_ghosting(self, image, persistence):
        kernel_size = int(25 * persistence)
        if kernel_size % 2 == 0:
            kernel_size += 1
        if kernel_size < 3:
            return image
        
        ghost = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
        return cv2.addWeighted(image, 1.0, ghost, persistence, 0)

    def apply_edge_bleeding(self, image, intensity):
        kernel_size = int(intensity * 10) | 1  # Ensure odd number
        if kernel_size < 3:
            return image
            
        # Create progressively blurred versions
        blurred1 = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
        blurred2 = cv2.GaussianBlur(image, (kernel_size * 2 + 1, kernel_size * 2 + 1), 0)
        
        # Detect edges
        edges = cv2.Laplacian(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), cv2.CV_64F)
        edges = np.abs(edges)
        edges = edges / edges.max()
        
        # Create bleeding effect by combining original and blurred versions
        result = image.copy().astype(np.float32)
        for i in range(3):  # Process each color channel
            result[..., i] = (
                image[..., i] * (1 - edges) +  # Original where no edges
                blurred1[..., i] * edges * 0.7 +  # First blur level
                blurred2[..., i] * edges * 0.3  # Second blur level
            )
        
        return np.clip(result, 0, 255).astype(np.uint8)

    def adjust_contrast_brightness(self, image, contrast, brightness):
        return np.clip(contrast * image + (brightness - 1) * 255, 0, 255).astype(np.uint8)

    def process_frame(self, image, params):
        # Apply contrast and brightness adjustments
        image = self.adjust_contrast_brightness(
            image,
            params["contrast"],
            params["brightness"]
        )
        
        # Convert to black and white if enabled
        if params["black_and_white"]:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        
        # Apply kinescope effects
        image = self.add_film_grain(
            image,
            params["film_grain"]
        )
        
        image = self.apply_phosphor_ghosting(
            image,
            params["phosphor_persistence"]
        )
        
        image = self.apply_edge_bleeding(
            image,
            params["edge_bleeding"]
        )
        
        image = self.apply_scanlines(
            image,
            params["scanline_intensity"]
        )
        
        # Apply final blur effects
        if params["vertical_blur"] > 1 or params["horizontal_blur"] > 1:
            image = cv2.blur(
                image,
                (params["horizontal_blur"], params["vertical_blur"])
            )
        
        return image

    def apply_kinescope_effect(self, images, black_and_white, contrast, brightness,
                             film_grain, phosphor_persistence, scanline_intensity,
                             edge_bleeding, vertical_blur, horizontal_blur, generations):
        
        # Convert from torch tensor to numpy array
        batch_numpy = images.cpu().numpy()
        batch_size, height, width, channels = batch_numpy.shape
        
        # Prepare parameters
        params = {
            "black_and_white": black_and_white,
            "contrast": contrast,
            "brightness": brightness,
            "film_grain": film_grain * generations,
            "phosphor_persistence": phosphor_persistence,
            "scanline_intensity": scanline_intensity,
            "edge_bleeding": edge_bleeding,
            "vertical_blur": vertical_blur if vertical_blur % 2 == 1 else vertical_blur + 1,
            "horizontal_blur": horizontal_blur if horizontal_blur % 2 == 1 else horizontal_blur + 1,
        }
        
        # Process each image in the batch
        processed_batch = np.zeros_like(batch_numpy)
        for i in range(batch_size):
            # Convert to BGR for processing
            frame = (batch_numpy[i] * 255).astype(np.uint8)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            
            # Apply kinescope effects
            frame = self.process_frame(frame, params)
            
            # Convert back to RGB and normalize
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            processed_batch[i] = frame.astype(np.float32) / 255.0
        
        # Convert back to torch tensor
        return (torch.from_numpy(processed_batch).to(images.device),)

NODE_CLASS_MAPPINGS = {
    "KinescopeEffectV1": KinescopeEffectV1
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "KinescopeEffectV1": "Kinescope Effect v1"
}
