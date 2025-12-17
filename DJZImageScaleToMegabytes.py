import math
import comfy.utils
import torch

class DJZImageScaleToMegabytes:
    upscale_methods = ["nearest-exact", "bilinear", "area", "bicubic", "lanczos"]

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "upscale_method": (s.upscale_methods,),
                "total_megabytes": ("FLOAT", {
                    "default": 4.99, 
                    "min": 0.01, 
                    "max": 100.0, 
                    "step": 0.01,
                    "display": "number"
                }),
                "divisible_by": ("INT", {
                    "default": 64,
                    "min": 1,
                    "max": 512,
                    "step": 1
                }),
                "batch": ("BOOLEAN", {
                    "default": False
                }),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "scale_to_megabytes"
    CATEGORY = "image/upscaling"

    def estimate_png_size(self, width, height, channels=3):
        """
        Estimate PNG file size in bytes with safety margin.
        PNG compression is highly variable, so we use conservative estimates:
        - Base compression factor: 0.8 (assume 20% compression)
        - Safety margin: 0.85 (to stay under limit)
        - Combined: 0.68 of uncompressed size
        This ensures output files stay safely under the specified target.
        """
        uncompressed_size = width * height * channels
        # Conservative estimate with safety margin to prevent exceeding target
        estimated_size = uncompressed_size * 0.8 * 0.85  # = 0.68
        return estimated_size

    def calculate_target_dimensions(self, current_width, current_height, target_bytes, channels=3):
        """
        Calculate target dimensions to achieve approximately target_bytes file size.
        """
        # Current estimated size
        current_estimated_size = self.estimate_png_size(current_width, current_height, channels)
        
        # Calculate scale factor based on the ratio of target to current size
        # Since file size scales with area (width * height), we take the square root
        scale_factor = math.sqrt(target_bytes / current_estimated_size)
        
        return scale_factor

    def scale_to_megabytes(self, image, upscale_method, total_megabytes, divisible_by, batch):
        samples = image.movedim(-1, 1)
        
        # Convert megabytes to bytes
        target_bytes = total_megabytes * 1024 * 1024
        
        # Get image dimensions
        batch_size = samples.shape[0]
        channels = samples.shape[1]
        current_height = samples.shape[2]
        current_width = samples.shape[3]
        
        # Determine target bytes per image
        if batch:
            # Divide target bytes across all images in batch
            # Apply additional 0.82 safety factor for batch mode to prevent overshoot
            bytes_per_image = (target_bytes / batch_size) * 0.82
        else:
            # Each image should be approximately the target size
            bytes_per_image = target_bytes
        
        # Calculate scale factor
        scale_factor = self.calculate_target_dimensions(
            current_width, 
            current_height, 
            bytes_per_image, 
            channels
        )
        
        # Calculate target dimensions
        target_width = current_width * scale_factor
        target_height = current_height * scale_factor
        
        # Round to nearest multiple of divisible_by
        width = round(target_width / divisible_by) * divisible_by
        height = round(target_height / divisible_by) * divisible_by
        
        # Ensure minimum dimensions (at least 1 * divisible_by)
        width = max(width, divisible_by)
        height = max(height, divisible_by)
        
        # Convert to integers
        width = int(width)
        height = int(height)
        
        # Perform the scaling
        s = comfy.utils.common_upscale(samples, width, height, upscale_method, "disabled")
        s = s.movedim(1, -1)
        
        return (s,)

NODE_CLASS_MAPPINGS = {
    "DJZImageScaleToMegabytes": DJZImageScaleToMegabytes,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DJZImageScaleToMegabytes": "DJZ Scale to Megabytes",
}
