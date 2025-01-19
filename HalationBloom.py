import numpy as np
import torch
import cv2

class HalationBloom:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),  # Batch of images input
                "effect_mode": (["Halation", "Bloom", "Both"],),
                "intensity": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 5.0,
                    "step": 0.1
                }),
                "threshold": ("FLOAT", {
                    "default": 0.6,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.05
                }),
                "radius": ("INT", {
                    "default": 15,
                    "min": 1,
                    "max": 100,
                    "step": 1
                }),
                "chromatic_aberration": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.1
                }),
                "temporal_variation": ("FLOAT", {
                    "default": 0.2,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.05
                }),
                "red_offset": ("FLOAT", {
                    "default": 1.2,
                    "min": 0.5,
                    "max": 2.0,
                    "step": 0.1
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_effect"
    CATEGORY = "image/effects"

    def create_temporal_variation(self, base_value, variation_amount, frame_index, total_frames):
        """Create smooth temporal variation using sine waves"""
        if total_frames <= 1:
            return base_value
        
        phase = (frame_index / total_frames) * 2 * np.pi
        variation = np.sin(phase) * variation_amount
        return base_value + variation

    def apply_halation(self, image, intensity, radius, threshold, red_offset):
        """Apply halation effect with color bleeding"""
        # Convert to float32 for processing
        img_float = image.astype(np.float32) / 255.0
        
        # Create luminance mask for bright areas
        luminance = cv2.cvtColor(img_float, cv2.COLOR_RGB2LAB)[:,:,0]
        bright_mask = np.clip(luminance - threshold, 0, 1)
        
        # Create separate color channel glows
        red_glow = cv2.GaussianBlur(img_float[:,:,0], (0,0), radius * red_offset)
        green_glow = cv2.GaussianBlur(img_float[:,:,1], (0,0), radius * 0.9)
        blue_glow = cv2.GaussianBlur(img_float[:,:,2], (0,0), radius * 0.8)
        
        # Combine channels with mask
        halation = np.stack([red_glow, green_glow, blue_glow], axis=-1)
        halation = halation * np.expand_dims(bright_mask, -1) * intensity
        
        # Blend with original image
        result = np.clip(img_float + halation, 0, 1)
        return (result * 255).astype(np.uint8)

    def apply_bloom(self, image, intensity, radius, threshold):
        """Apply uniform bloom effect"""
        # Convert to float32
        img_float = image.astype(np.float32) / 255.0
        
        # Create and blur bright areas
        bright_areas = np.where(img_float > threshold, img_float, 0)
        bloom = cv2.GaussianBlur(bright_areas, (0,0), radius)
        
        # Blend with original image
        result = np.clip(img_float + (bloom * intensity), 0, 1)
        return (result * 255).astype(np.uint8)

    def apply_chromatic_aberration(self, image, amount):
        """Apply chromatic aberration effect"""
        height, width = image.shape[:2]
        
        # Calculate displacement maps
        x_displacement = int(width * amount * 0.02)
        y_displacement = int(height * amount * 0.01)
        
        # Split channels and apply displacement
        b, g, r = cv2.split(image)
        
        # Shift red channel
        matrix_r = np.float32([[1, 0, x_displacement], [0, 1, y_displacement]])
        r = cv2.warpAffine(r, matrix_r, (width, height))
        
        # Shift blue channel opposite
        matrix_b = np.float32([[1, 0, -x_displacement], [0, 1, -y_displacement]])
        b = cv2.warpAffine(b, matrix_b, (width, height))
        
        return cv2.merge([b, g, r])

    def apply_effect(self, images, effect_mode, intensity, threshold, radius, 
                    chromatic_aberration, temporal_variation, red_offset):
        # Convert from torch tensor to numpy array
        batch_numpy = images.cpu().numpy()
        batch_size = batch_numpy.shape[0]
        processed_batch = np.zeros_like(batch_numpy)
        
        for i in range(batch_size):
            # Apply temporal variation to parameters
            frame_intensity = self.create_temporal_variation(
                intensity, temporal_variation, i, batch_size)
            
            # Convert to uint8 for processing
            frame = (batch_numpy[i] * 255).astype(np.uint8)
            
            if effect_mode in ["Halation", "Both"]:
                frame = self.apply_halation(
                    frame, frame_intensity, radius, threshold, red_offset)
            
            if effect_mode in ["Bloom", "Both"]:
                frame = self.apply_bloom(
                    frame, frame_intensity * 0.5, radius, threshold)
            
            if chromatic_aberration > 0:
                frame = self.apply_chromatic_aberration(frame, chromatic_aberration)
            
            # Normalize back to float32
            processed_batch[i] = frame.astype(np.float32) / 255.0
        
        # Convert back to torch tensor
        return (torch.from_numpy(processed_batch).to(images.device),)

NODE_CLASS_MAPPINGS = {
    "HalationBloom": HalationBloom
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "HalationBloom": "Halation & Bloom Effect"
}