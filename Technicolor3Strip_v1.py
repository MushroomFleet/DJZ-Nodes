import numpy as np
import torch
import cv2

class Technicolor3Strip_v1:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),  # Batch of images input
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
                "cross_process_amount": ("FLOAT", {
                    "default": 0.1,
                    "min": 0.0,
                    "max": 0.5,
                    "step": 0.05,
                }),
                "saturation_boost": ("FLOAT", {
                    "default": 1.2,
                    "min": 0.5,
                    "max": 2.0,
                    "step": 0.1,
                }),
                "contrast_boost": ("FLOAT", {
                    "default": 1.1,
                    "min": 0.5,
                    "max": 2.0,
                    "step": 0.1,
                }),
                "shadow_preservation": ("FLOAT", {
                    "default": 0.8,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.1,
                }),
                "highlight_protection": ("FLOAT", {
                    "default": 0.9,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.1,
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_technicolor_effect"
    CATEGORY = "image/effects"

    def adjust_shadows_highlights(self, image, shadow_preservation, highlight_protection):
        # Convert to LAB color space for luminance adjustment
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l_channel = lab[:, :, 0]
        
        # Apply shadow preservation
        shadows_mask = l_channel < 127
        l_channel[shadows_mask] = (l_channel[shadows_mask] * shadow_preservation + 
                                 l_channel[shadows_mask] * (1 - shadow_preservation))
        
        # Apply highlight protection
        highlights_mask = l_channel >= 127
        l_channel[highlights_mask] = (l_channel[highlights_mask] * highlight_protection + 
                                    255 * (1 - highlight_protection))
        
        lab[:, :, 0] = l_channel
        return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    def enhance_contrast(self, image, amount):
        # Create a contrast lookup table
        lookUpTable = np.empty((1, 256), np.uint8)
        for i in range(256):
            lookUpTable[0, i] = np.clip(pow(i / 255.0, 1.0 / amount) * 255.0, 0, 255)
        return cv2.LUT(image, lookUpTable)

    def process_frame(self, image, params):
        # Split into BGR channels
        b, g, r = cv2.split(image)
        
        # Enhance each channel separately
        r = cv2.addWeighted(r, params["red_strength"], r, 0, 0)
        g = cv2.addWeighted(g, params["green_strength"], g, 0, 0)
        b = cv2.addWeighted(b, params["blue_strength"], b, 0, 0)
        
        # Apply cross-processing between channels
        cross = params["cross_process_amount"]
        r = cv2.addWeighted(r, 1.0 - cross, g, cross, 0)
        g = cv2.addWeighted(g, 1.0 - cross, b, cross, 0)
        b = cv2.addWeighted(b, 1.0 - cross, r, cross, 0)
        
        # Merge channels
        technicolor = cv2.merge([b, g, r])
        
        # Adjust contrast
        technicolor = self.enhance_contrast(technicolor, params["contrast_boost"])
        
        # Convert to HSV for saturation adjustment
        hsv = cv2.cvtColor(technicolor, cv2.COLOR_BGR2HSV)
        hsv[:, :, 1] = cv2.multiply(hsv[:, :, 1], params["saturation_boost"])
        technicolor = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        
        # Apply shadow and highlight adjustments
        technicolor = self.adjust_shadows_highlights(
            technicolor,
            params["shadow_preservation"],
            params["highlight_protection"]
        )
        
        return technicolor

    def apply_technicolor_effect(self, images, red_strength, green_strength, blue_strength,
                               cross_process_amount, saturation_boost, contrast_boost,
                               shadow_preservation, highlight_protection):
        
        # Convert from torch tensor to numpy array
        batch_numpy = images.cpu().numpy()
        batch_size, height, width, channels = batch_numpy.shape
        
        # Prepare parameters
        params = {
            "red_strength": red_strength,
            "green_strength": green_strength,
            "blue_strength": blue_strength,
            "cross_process_amount": cross_process_amount,
            "saturation_boost": saturation_boost,
            "contrast_boost": contrast_boost,
            "shadow_preservation": shadow_preservation,
            "highlight_protection": highlight_protection,
        }
        
        # Process each image in the batch
        processed_batch = np.zeros_like(batch_numpy)
        for i in range(batch_size):
            # Convert to BGR for processing
            frame = (batch_numpy[i] * 255).astype(np.uint8)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            
            # Apply Technicolor effect
            frame = self.process_frame(frame, params)
            
            # Convert back to RGB and normalize
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            processed_batch[i] = frame.astype(np.float32) / 255.0
        
        # Convert back to torch tensor
        return (torch.from_numpy(processed_batch).to(images.device),)

NODE_CLASS_MAPPINGS = {
    "Technicolor3Strip_v1": Technicolor3Strip_v1
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Technicolor3Strip_v1": "Technicolor 3-Strip v1"
}