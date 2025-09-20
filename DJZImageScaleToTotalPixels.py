import math
import comfy.utils

class DJZImageScaleToTotalPixels:
    upscale_methods = ["nearest-exact", "bilinear", "area", "bicubic", "lanczos"]
    crop_methods = ["disabled", "center"]

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "upscale_method": (s.upscale_methods,),
                "megapixels": ("FLOAT", {
                    "default": 1.0, 
                    "min": 0.01, 
                    "max": 16.0, 
                    "step": 0.01
                }),
                "downscale_factor": ("INT", {
                    "default": 64,
                    "min": 1,
                    "max": 512,
                    "step": 1
                }),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "upscale"
    CATEGORY = "image/upscaling"

    def upscale(self, image, upscale_method, megapixels, downscale_factor):
        samples = image.movedim(-1, 1)
        total = int(megapixels * 1024 * 1024)

        # Calculate initial scale factor
        scale_by = math.sqrt(total / (samples.shape[3] * samples.shape[2]))
        
        # Calculate target dimensions
        target_width = samples.shape[3] * scale_by
        target_height = samples.shape[2] * scale_by
        
        # Round to nearest multiple of downscale_factor to ensure divisibility
        width = round(target_width / downscale_factor) * downscale_factor
        height = round(target_height / downscale_factor) * downscale_factor
        
        # Ensure minimum dimensions (at least 1 * downscale_factor)
        width = max(width, downscale_factor)
        height = max(height, downscale_factor)

        s = comfy.utils.common_upscale(samples, width, height, upscale_method, "disabled")
        s = s.movedim(1, -1)
        return (s,)

NODE_CLASS_MAPPINGS = {
    "DJZImageScaleToTotalPixels": DJZImageScaleToTotalPixels,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DJZImageScaleToTotalPixels": "DJZ Scale to Total Pixels",
}