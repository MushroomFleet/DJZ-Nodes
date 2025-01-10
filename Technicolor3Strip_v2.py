import numpy as np
import torch
import cv2
from PIL import Image, ImageEnhance, ImageOps, ImageFilter

class Technicolor3Strip_v2:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),  # Batch of images input
                # Color Channel Controls
                "red_strength": ("FLOAT", {
                    "default": 1.5,
                    "min": 0.1,
                    "max": 3.0,
                    "step": 0.1,
                }),
                "green_strength": ("FLOAT", {
                    "default": 1.3,
                    "min": 0.1,
                    "max": 3.0,
                    "step": 0.1,
                }),
                "blue_strength": ("FLOAT", {
                    "default": 1.2,
                    "min": 0.1,
                    "max": 3.0,
                    "step": 0.1,
                }),
                # Cross-processing
                "cross_process_amount": ("FLOAT", {
                    "default": 0.1,
                    "min": 0.0,
                    "max": 0.5,
                    "step": 0.05,
                }),
                # Enhanced Color Controls
                "color_saturation": ("FLOAT", {
                    "default": 1.4,
                    "min": 0.0,
                    "max": 3.0,
                    "step": 0.1,
                }),
                "color_temperature": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.5,
                    "max": 2.0,
                    "step": 0.1,
                }),
                "color_vibrance": ("FLOAT", {
                    "default": 1.2,
                    "min": 0.5,
                    "max": 2.0,
                    "step": 0.1,
                }),
                # Contrast and Tone Controls
                "contrast": ("FLOAT", {
                    "default": 1.2,
                    "min": 0.5,
                    "max": 2.0,
                    "step": 0.1,
                }),
                "brightness": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.5,
                    "max": 1.5,
                    "step": 0.1,
                }),
                "shadow_tone": ("FLOAT", {
                    "default": 0.9,
                    "min": 0.5,
                    "max": 1.5,
                    "step": 0.1,
                }),
                "highlight_tone": ("FLOAT", {
                    "default": 0.95,
                    "min": 0.5,
                    "max": 1.5,
                    "step": 0.1,
                }),
                # Film Characteristics
                "grain_amount": ("FLOAT", {
                    "default": 0.1,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.05,
                }),
                "sharpness": ("FLOAT", {
                    "default": 1.1,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.1,
                }),
                "halation": ("FLOAT", {
                    "default": 0.2,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.1,
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_technicolor_effect"
    CATEGORY = "image/effects"

    def adjust_color_temperature(self, image, temperature):
        # Adjust RGB channels to simulate color temperature
        r, g, b = image.split()
        if temperature > 1:  # Warmer
            r = ImageEnhance.Brightness(r).enhance(temperature)
            b = ImageEnhance.Brightness(b).enhance(2 - temperature)
        else:  # Cooler
            r = ImageEnhance.Brightness(r).enhance(temperature)
            b = ImageEnhance.Brightness(b).enhance(1 + (1 - temperature))
        return Image.merge('RGB', (r, g, b))

    def apply_halation(self, image, amount):
        # Create a blurred version for halation effect
        blur = image.filter(ImageFilter.GaussianBlur(radius=10))
        blur = ImageEnhance.Brightness(blur).enhance(1 + amount)
        return Image.blend(image, blur, amount)

    def add_grain(self, image, amount):
        if amount == 0:
            return image
        
        # Create grain pattern
        grain = np.random.normal(0, amount * 50, image.size[::-1])
        grain = Image.fromarray(np.uint8(grain + 128))
        grain = grain.convert('L')
        
        # Apply grain to each channel
        r, g, b = image.split()
        r = Image.blend(r, grain, amount * 0.1)
        g = Image.blend(g, grain, amount * 0.1)
        b = Image.blend(b, grain, amount * 0.1)
        
        return Image.merge('RGB', (r, g, b))

    def adjust_vibrance(self, image, vibrance):
        # Convert to HSV for vibrance adjustment
        hsv = image.convert('HSV')
        h, s, v = hsv.split()
        
        # Enhance saturation based on current saturation levels
        s_array = np.array(s)
        s_array = s_array * (1 + (vibrance - 1) * (1 - s_array / 255))
        s = Image.fromarray(np.uint8(np.clip(s_array, 0, 255)))
        
        return Image.merge('HSV', (h, s, v)).convert('RGB')

    def process_frame(self, image, params):
        # Convert numpy array to PIL Image
        pil_image = Image.fromarray(image)
        
        # Split and enhance individual channels
        r, g, b = pil_image.split()
        r = ImageEnhance.Brightness(r).enhance(params["red_strength"])
        g = ImageEnhance.Brightness(g).enhance(params["green_strength"])
        b = ImageEnhance.Brightness(b).enhance(params["blue_strength"])
        
        # Cross-processing
        cross = params["cross_process_amount"]
        if cross > 0:
            r = Image.blend(r, g, cross)
            g = Image.blend(g, b, cross)
            b = Image.blend(b, r, cross)
        
        # Merge channels
        image = Image.merge('RGB', (r, g, b))
        
        # Apply enhanced color adjustments
        image = ImageEnhance.Color(image).enhance(params["color_saturation"])
        image = self.adjust_color_temperature(image, params["color_temperature"])
        image = self.adjust_vibrance(image, params["color_vibrance"])
        
        # Apply contrast and tone adjustments
        image = ImageEnhance.Contrast(image).enhance(params["contrast"])
        image = ImageEnhance.Brightness(image).enhance(params["brightness"])
        
        # Shadow and highlight adjustments
        shadow_image = ImageOps.autocontrast(image, cutoff=(params["shadow_tone"] * 100, 0))
        highlight_image = ImageOps.autocontrast(image, cutoff=(0, (1 - params["highlight_tone"]) * 100))
        image = Image.blend(image, shadow_image, 0.5)
        image = Image.blend(image, highlight_image, 0.5)
        
        # Apply film characteristics
        image = ImageEnhance.Sharpness(image).enhance(params["sharpness"])
        image = self.apply_halation(image, params["halation"])
        image = self.add_grain(image, params["grain_amount"])
        
        # Convert back to numpy array
        return np.array(image)

    def apply_technicolor_effect(self, images, red_strength, green_strength, blue_strength,
                               cross_process_amount, color_saturation, color_temperature,
                               color_vibrance, contrast, brightness, shadow_tone,
                               highlight_tone, grain_amount, sharpness, halation):
        
        # Convert from torch tensor to numpy array
        batch_numpy = images.cpu().numpy()
        batch_size, height, width, channels = batch_numpy.shape
        
        # Prepare parameters
        params = {
            "red_strength": red_strength,
            "green_strength": green_strength,
            "blue_strength": blue_strength,
            "cross_process_amount": cross_process_amount,
            "color_saturation": color_saturation,
            "color_temperature": color_temperature,
            "color_vibrance": color_vibrance,
            "contrast": contrast,
            "brightness": brightness,
            "shadow_tone": shadow_tone,
            "highlight_tone": highlight_tone,
            "grain_amount": grain_amount,
            "sharpness": sharpness,
            "halation": halation,
        }
        
        # Process each image in the batch
        processed_batch = np.zeros_like(batch_numpy)
        for i in range(batch_size):
            # Convert to RGB uint8 for PIL
            frame = (batch_numpy[i] * 255).astype(np.uint8)
            
            # Apply Technicolor effect
            frame = self.process_frame(frame, params)
            
            # Normalize back to float32
            processed_batch[i] = frame.astype(np.float32) / 255.0
        
        # Convert back to torch tensor
        return (torch.from_numpy(processed_batch).to(images.device),)

NODE_CLASS_MAPPINGS = {
    "Technicolor3Strip_v2": Technicolor3Strip_v2
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Technicolor3Strip_v2": "Technicolor 3-Strip v2"
}