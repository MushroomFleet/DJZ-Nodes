import numpy as np
import torch
import cv2

class CRT_Effect_v1:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),  # Batch of images input
                "preset_mode": (["Custom", "Arcade", "Consumer TV", "Professional Monitor", "Black & White TV"], {
                    "default": "Custom"
                }),
                "scanline_intensity": ("FLOAT", {
                    "default": 0.3,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.05,
                }),
                "scanline_spacing": ("INT", {
                    "default": 2,
                    "min": 1,
                    "max": 10,
                    "step": 1,
                }),
                "phosphor_blur": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.1,
                }),
                "bloom_intensity": ("FLOAT", {
                    "default": 0.2,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.05,
                }),
                "bloom_spread": ("INT", {
                    "default": 15,
                    "min": 3,
                    "max": 51,
                    "step": 2,
                }),
                "curvature": ("FLOAT", {
                    "default": 0.1,
                    "min": 0.0,
                    "max": 0.5,
                    "step": 0.05,
                }),
                "vignette_intensity": ("FLOAT", {
                    "default": 0.2,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.05,
                }),
                "brightness": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.5,
                    "max": 2.0,
                    "step": 0.1,
                }),
                "contrast": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.5,
                    "max": 2.0,
                    "step": 0.1,
                }),
                "rgb_offset": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.0,
                    "max": 5.0,
                    "step": 0.5,
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_crt_effect"
    CATEGORY = "image/effects"

    def get_preset_parameters(self, preset_mode):
        presets = {
            "Arcade": {
                "scanline_intensity": 0.4,
                "scanline_spacing": 2,
                "phosphor_blur": 0.6,
                "bloom_intensity": 0.3,
                "bloom_spread": 15,
                "curvature": 0.15,
                "vignette_intensity": 0.3,
                "brightness": 1.2,
                "contrast": 1.2,
                "rgb_offset": 1.0
            },
            "Consumer TV": {
                "scanline_intensity": 0.25,
                "scanline_spacing": 3,
                "phosphor_blur": 0.8,
                "bloom_intensity": 0.2,
                "bloom_spread": 21,
                "curvature": 0.2,
                "vignette_intensity": 0.25,
                "brightness": 1.1,
                "contrast": 1.1,
                "rgb_offset": 1.5
            },
            "Professional Monitor": {
                "scanline_intensity": 0.15,
                "scanline_spacing": 2,
                "phosphor_blur": 0.3,
                "bloom_intensity": 0.1,
                "bloom_spread": 9,
                "curvature": 0.05,
                "vignette_intensity": 0.1,
                "brightness": 1.0,
                "contrast": 1.2,
                "rgb_offset": 0.0
            },
            "Black & White TV": {
                "scanline_intensity": 0.35,
                "scanline_spacing": 3,
                "phosphor_blur": 1.0,
                "bloom_intensity": 0.25,
                "bloom_spread": 25,
                "curvature": 0.25,
                "vignette_intensity": 0.35,
                "brightness": 1.1,
                "contrast": 1.3,
                "rgb_offset": 0.0
            }
        }
        return presets.get(preset_mode, None)

    def apply_scanlines(self, image, intensity, spacing):
        height, width = image.shape[:2]
        scanline_mask = np.ones((height, width))
        scanline_mask[::spacing] = 1.0 - intensity
        return image * scanline_mask[:, :, np.newaxis]

    def apply_phosphor_blur(self, image, blur_amount):
        if blur_amount == 0:
            return image
        kernel_size = int(blur_amount * 10) * 2 + 1
        return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)

    def apply_bloom(self, image, intensity, spread):
        if intensity == 0:
            return image
        bloom = cv2.GaussianBlur(image, (spread, spread), 0)
        return cv2.addWeighted(image, 1.0, bloom, intensity, 0)

    def apply_curvature(self, image, amount):
        if amount == 0:
            return image
            
        height, width = image.shape[:2]
        map_x = np.zeros((height, width), np.float32)
        map_y = np.zeros((height, width), np.float32)
        
        for y in range(height):
            for x in range(width):
                nx = (2.0 * x - width) / width
                ny = (2.0 * y - height) / height
                r = np.sqrt(nx * nx + ny * ny)
                
                if r == 0:
                    map_x[y, x] = x
                    map_y[y, x] = y
                else:
                    factor = 1.0 + r * amount
                    map_x[y, x] = (nx * factor + 1.0) * width * 0.5
                    map_y[y, x] = (ny * factor + 1.0) * height * 0.5

        return cv2.remap(image, map_x, map_y, cv2.INTER_LINEAR)

    def apply_vignette(self, image, intensity):
        if intensity == 0:
            return image
            
        height, width = image.shape[:2]
        y, x = np.ogrid[0:height, 0:width]
        center_y, center_x = height/2, width/2
        mask = np.sqrt((x - center_x)**2 + (y - center_y)**2)
        mask = 1 - (mask / (np.sqrt(center_x**2 + center_y**2)))
        mask = np.clip(mask, 0, 1)
        mask = mask ** (1/intensity)
        return image * mask[:, :, np.newaxis]

    def apply_rgb_offset(self, image, offset):
        if offset == 0:
            return image
            
        height, width = image.shape[:2]
        result = np.zeros_like(image)
        
        # Offset red channel slightly right
        offset_px = int(offset)
        result[:, offset_px:, 2] = image[:, :-offset_px, 2] if offset_px > 0 else image[:, :, 2]
        
        # Keep green channel centered
        result[:, :, 1] = image[:, :, 1]
        
        # Offset blue channel slightly left
        result[:, :-offset_px, 0] = image[:, offset_px:, 0] if offset_px > 0 else image[:, :, 0]
        
        return result

    def adjust_brightness_contrast(self, image, brightness, contrast):
        return np.clip((image * contrast + (brightness - 1.0)), 0, 1)

    def apply_crt_effect(self, images, preset_mode, scanline_intensity, scanline_spacing,
                        phosphor_blur, bloom_intensity, bloom_spread, curvature,
                        vignette_intensity, brightness, contrast, rgb_offset):
        
        # Apply preset parameters if a non-custom preset is selected
        if preset_mode != "Custom":
            preset_params = self.get_preset_parameters(preset_mode)
            if preset_params:
                scanline_intensity = preset_params["scanline_intensity"]
                scanline_spacing = preset_params["scanline_spacing"]
                phosphor_blur = preset_params["phosphor_blur"]
                bloom_intensity = preset_params["bloom_intensity"]
                bloom_spread = preset_params["bloom_spread"]
                curvature = preset_params["curvature"]
                vignette_intensity = preset_params["vignette_intensity"]
                brightness = preset_params["brightness"]
                contrast = preset_params["contrast"]
                rgb_offset = preset_params["rgb_offset"]

        # Convert from torch tensor to numpy array
        batch_numpy = images.cpu().numpy()
        batch_size = batch_numpy.shape[0]
        
        # Process each image in the batch
        processed_batch = np.zeros_like(batch_numpy)
        for i in range(batch_size):
            # Get current image and ensure it's in float range [0, 1]
            image = batch_numpy[i].copy()
            
            # Apply effects in sequence
            image = self.apply_phosphor_blur(image, phosphor_blur)
            image = self.apply_bloom(image, bloom_intensity, bloom_spread)
            image = self.apply_scanlines(image, scanline_intensity, scanline_spacing)
            image = self.apply_curvature(image, curvature)
            image = self.apply_vignette(image, vignette_intensity)
            image = self.adjust_brightness_contrast(image, brightness, contrast)
            
            # Apply RGB offset last to prevent it from being blurred
            if preset_mode != "Black & White TV":
                image = self.apply_rgb_offset(image, rgb_offset)
            else:
                # Convert to grayscale for Black & White TV preset
                image = np.dot(image[..., :3], [0.2989, 0.5870, 0.1140])
                image = np.stack((image,) * 3, axis=-1)
            
            processed_batch[i] = np.clip(image, 0, 1)
        
        # Convert back to torch tensor
        return (torch.from_numpy(processed_batch).to(images.device),)

NODE_CLASS_MAPPINGS = {
    "CRT_Effect_v1": CRT_Effect_v1
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CRT_Effect_v1": "CRT Effect v1"
}