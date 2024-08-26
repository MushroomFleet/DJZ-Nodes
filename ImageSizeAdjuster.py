import math

class ImageSizeAdjuster:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "model_type": (["SD", "SDXL", "Cascade"],),
                "downscale_factor": ("INT", {
                    "default": 16,
                    "min": 1,
                    "max": 128,
                    "step": 1,
                    "display": "number"
                })
            }
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("adjusted_width", "adjusted_height")
    FUNCTION = "adjust_size"
    CATEGORY = "DJZ-Nodes"

    def adjust_size(self, image, model_type, downscale_factor):
        # Define the total pixel counts for SD, SDXL, and Cascade
        total_pixels = {
            'SD': 512 * 512,
            'SDXL': 1024 * 1024,
            'Cascade': 2048 * 2048
        }

        # Get the dimensions of the input image
        _, height, width, _ = image.shape

        # Calculate the current aspect ratio
        aspect_ratio = width / height

        # Get the target total pixels based on the model type
        target_pixels = total_pixels[model_type]

        # Calculate new dimensions that maintain the aspect ratio and are close to the target pixel count
        new_width = math.sqrt(target_pixels * aspect_ratio)
        new_height = new_width / aspect_ratio

        # Adjust dimensions to be divisible by the downscale factor
        adjusted_width = math.ceil(new_width / downscale_factor) * downscale_factor
        adjusted_height = math.ceil(new_height / downscale_factor) * downscale_factor

        return (int(adjusted_width), int(adjusted_height))

NODE_CLASS_MAPPINGS = {
    "ImageSizeAdjuster": ImageSizeAdjuster
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageSizeAdjuster": "Image Size Adjuster"
}