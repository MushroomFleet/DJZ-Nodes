import math

class ImageSizeAdjusterV3:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "model_type": (["SD", "SDXL", "Cascade", "Mochi1"],),
                "downscale_factor": ("INT", {
                    "default": 8,  # Changed default to 8 to better suit video
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
        # Define model-specific parameters for standard models
        total_pixels = {
            'SD': 512 * 512,
            'SDXL': 1024 * 1024,
            'Cascade': 2048 * 2048,
        }
        
        # Model-specific constraints for Mochi1
        mochi_constraints = {
            'landscape': {
                'width': 848,
                'height': 480,
                'aspect': 848/480  # 16:9
            },
            'portrait': {
                'width': 480,
                'height': 848,
                'aspect': 480/848  # 9:16
            },
            'threshold': 1.0  # Aspect ratio threshold for switching between landscape and portrait
        }

        _, original_height, original_width, _ = image.shape
        aspect_ratio = original_width / original_height

        # Handle Mochi1 model type differently
        if model_type == 'Mochi1':
            # Determine orientation based on aspect ratio
            is_landscape = aspect_ratio >= mochi_constraints['threshold']
            orientation = 'landscape' if is_landscape else 'portrait'
            constraints = mochi_constraints[orientation]
            
            # Set maximum dimensions based on orientation
            max_width = min(max_width, constraints['width'])
            max_height = min(max_height, constraints['height'])
            
            # Calculate target dimensions while maintaining Mochi1's aspect ratio
            if is_landscape:
                # For landscape, fit to width and calculate height
                new_width = constraints['width']
                new_height = int(new_width / constraints['aspect'])
            else:
                # For portrait, fit to height and calculate width
                new_height = constraints['height']
                new_width = int(new_height * constraints['aspect'])
            
            # Removed forced downscale_factor override
            
        else:
            # Handle standard models
            target_pixels = total_pixels[model_type] * (scaling_factor ** 2)
            new_width, new_height = self._calculate_initial_dimensions(target_pixels, aspect_ratio, force_square)

        if model_type != 'Mochi1':  # Only apply these adjustments for non-Mochi1 models
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
    "ImageSizeAdjusterV3": ImageSizeAdjusterV3
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageSizeAdjusterV3": "Image Size Adjuster V3"
}