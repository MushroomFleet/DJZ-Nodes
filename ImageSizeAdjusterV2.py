import math

class ImageSizeAdjusterV2:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "model_type": (["SD", "SDXL", "1440p", "WAN22", "Cascade", "4K", "8K", "16K"],),
                "downscale_factor": ("INT", {
                    "default": 64,
                    "min": 1,
                    "max": 128,
                    "step": 1,
                    "display": "number"
                }),
                "rounding_method": (["up", "down", "nearest"],),
                "preserve_original": (["none", "width", "height"],),
                "force_square": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "scaling_factor": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 10.0,
                    "step": 0.1,
                    "display": "number"
                }),
                "max_width": ("INT", {
                    "default": 2048,
                    "min": 64,
                    "max": 8192,
                    "step": 64,
                    "display": "number"
                }),
                "max_height": ("INT", {
                    "default": 2048,
                    "min": 64,
                    "max": 8192,
                    "step": 64,
                    "display": "number"
                }),
            }
        }

    RETURN_TYPES = ("INT", "INT", "FLOAT", "INT", "INT")
    RETURN_NAMES = ("adjusted_width", "adjusted_height", "applied_scale", "original_width", "original_height")
    FUNCTION = "adjust_size"
    CATEGORY = "DJZ-Nodes"

    def adjust_size(self, image, model_type, downscale_factor, rounding_method, preserve_original, force_square, scaling_factor=1.0, max_width=2048, max_height=2048):
        total_pixels = {
            'SD': 512 * 512,
            'SDXL': 1024 * 1024,
            '1440p': 1440 * 1440,
            'WAN22': 1536 * 1536,
            'Cascade': 2048 * 2048,
            '4K': 2880 * 2880,
            '8K': 5760 * 5760,
            '16K': 11520 * 11520
        }

        _, original_height, original_width, _ = image.shape
        aspect_ratio = original_width / original_height
        target_pixels = total_pixels[model_type] * (scaling_factor ** 2)

        new_width, new_height = self._calculate_initial_dimensions(target_pixels, aspect_ratio, force_square)
        new_width, new_height = self._preserve_original_dimension(new_width, new_height, original_width, original_height, preserve_original, downscale_factor, aspect_ratio)
        adjusted_width, adjusted_height = self._apply_rounding_method(new_width, new_height, downscale_factor, rounding_method)
        adjusted_width, adjusted_height = self._apply_size_limits(adjusted_width, adjusted_height, max_width, max_height, downscale_factor)

        applied_scale = math.sqrt((adjusted_width * adjusted_height) / (original_width * original_height))

        return int(adjusted_width), int(adjusted_height), float(applied_scale), original_width, original_height

    def _calculate_initial_dimensions(self, target_pixels, aspect_ratio, force_square):
        if force_square:
            new_size = int(math.sqrt(target_pixels))
            return new_size, new_size
        else:
            new_width = math.sqrt(target_pixels * aspect_ratio)
            new_height = new_width / aspect_ratio
            return new_width, new_height

    def _preserve_original_dimension(self, new_width, new_height, original_width, original_height, preserve_original, downscale_factor, aspect_ratio):
        if preserve_original == "width" and original_width % downscale_factor == 0:
            new_width = original_width
            new_height = new_width / aspect_ratio
        elif preserve_original == "height" and original_height % downscale_factor == 0:
            new_height = original_height
            new_width = new_height * aspect_ratio
        return new_width, new_height

    def _apply_rounding_method(self, width, height, downscale_factor, rounding_method):
        rounding_functions = {
            "up": math.ceil,
            "down": math.floor,
            "nearest": round
        }
        rounding_func = rounding_functions[rounding_method]
        
        adjusted_width = rounding_func(width / downscale_factor) * downscale_factor
        adjusted_height = rounding_func(height / downscale_factor) * downscale_factor
        return adjusted_width, adjusted_height

    def _apply_size_limits(self, width, height, max_width, max_height, downscale_factor):
        width = min(max(width, downscale_factor), max_width)
        height = min(max(height, downscale_factor), max_height)
        return width, height

NODE_CLASS_MAPPINGS = {
    "ImageSizeAdjusterV2": ImageSizeAdjusterV2
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageSizeAdjusterV2": "Image Size Adjuster V2"
}
