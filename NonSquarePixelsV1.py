import numpy as np
import torch
import cv2 # type: ignore

class NonSquarePixelsV1:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),  # Batch of images input
                "preset": (["CUSTOM", "PAL (4:3)", "PAL WIDESCREEN (16:9)", "NTSC (4:3)", "NTSC WIDESCREEN (16:9)"], {
                    "default": "CUSTOM"
                }),
                "custom_pixel_aspect_ratio": ("FLOAT", {
                    "default": 1.0667,  # PAL 4:3 default
                    "min": 0.5,
                    "max": 2.0,
                    "step": 0.0001,
                }),
                "preserve_original_size": (["enable", "disable"], {
                    "default": "enable"
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_non_square_pixels"
    CATEGORY = "image/effects"

    def get_pixel_aspect_ratio(self, preset, custom_ratio):
        # Base ratios
        pal_4_3 = 1.0667    # 59/55
        ntsc_4_3 = 0.9091   # 10/11
        widescreen_multiplier = 4/3  # 16:9 is 4/3 times wider than 4:3
        
        preset_ratios = {
            "PAL (4:3)": pal_4_3,
            "PAL WIDESCREEN (16:9)": pal_4_3 * widescreen_multiplier,  # ≈ 1.4223
            "NTSC (4:3)": ntsc_4_3,
            "NTSC WIDESCREEN (16:9)": ntsc_4_3 * widescreen_multiplier  # ≈ 1.2121
        }
        return preset_ratios.get(preset, custom_ratio)

    def apply_non_square_pixels(self, images, preset, custom_pixel_aspect_ratio, preserve_original_size):
        # Convert from torch tensor to numpy array
        batch_numpy = images.cpu().numpy()
        batch_size, height, width, channels = batch_numpy.shape
        
        # Get the pixel aspect ratio based on preset or custom value
        pixel_aspect_ratio = self.get_pixel_aspect_ratio(preset, custom_pixel_aspect_ratio)
        
        # Calculate new dimensions
        new_width = int(width * pixel_aspect_ratio)
        
        # Initialize processed batch with correct dimensions
        if preserve_original_size == "enable":
            processed_batch = np.zeros_like(batch_numpy)
            final_width = width
        else:
            processed_batch = np.zeros((batch_size, height, new_width, channels), dtype=batch_numpy.dtype)
            final_width = new_width
            
        # Process each image in the batch
        for i in range(batch_size):
            # Convert to BGR for processing
            frame = (batch_numpy[i] * 255).astype(np.uint8)
            
            # Apply pixel aspect ratio transformation
            processed = cv2.resize(frame, (new_width, height), interpolation=cv2.INTER_LINEAR)
            
            # Optionally resize back to original dimensions
            if preserve_original_size == "enable":
                processed = cv2.resize(processed, (width, height), interpolation=cv2.INTER_LINEAR)
            
            # Normalize back to 0-1 range
            processed_batch[i] = processed.astype(np.float32) / 255.0
        
        # Convert back to torch tensor
        return (torch.from_numpy(processed_batch).to(images.device),)

NODE_CLASS_MAPPINGS = {
    "NonSquarePixelsV1": NonSquarePixelsV1
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "NonSquarePixelsV1": "Non-Square Pixels v1"
}
