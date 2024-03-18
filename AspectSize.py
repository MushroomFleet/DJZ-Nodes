import math

class AspectSize:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model_type": (["SD","SDXL","Cascade"],),
                "aspect_ratio_width": ("INT",{
                    "default": 1,
                    "step":1,
                    "display": "number"
                }),
                "aspect_ratio_height": ("INT",{
                    "default": 1,
                    "step":1,
                    "display": "number"
                })
            }
        }

    RETURN_TYPES = ("INT","INT")
    RETURN_NAMES = ("Width", "Height")

    FUNCTION = "run"

    CATEGORY = "DJZ-Nodes"

    def run(self, model_type, aspect_ratio_width, aspect_ratio_height,  downscale_factor=16):
        # Define the total pixel counts for SD and SDXL
        total_pixels = {
            'SD': 512 * 512,
            'SDXL': 1024 * 1024,
            'Cascade': 2048 * 2048
        }
    
        # Calculate the number of total pixels based on model type
        pixels = total_pixels.get(model_type, 0)
    
        # Calculate the aspect ratio decimal
        aspect_ratio_decimal = aspect_ratio_width / aspect_ratio_height
    
        # Calculate width and height
        width = math.sqrt(pixels * aspect_ratio_decimal)
        height = pixels / width
    
        # Adjust the width and height to be divisible by the downscale_factor
        width = math.ceil(width / downscale_factor) * downscale_factor
        height = math.ceil(height / downscale_factor) * downscale_factor
    
        # Return the width and height as a tuple of integers
        return (int(width), int(height))

NODE_CLASS_MAPPINGS = {
    "AspectSize": AspectSize
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AspectSize": "AspectSize"
}