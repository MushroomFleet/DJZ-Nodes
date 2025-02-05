import numpy as np
import torch
import math

class VideoTemperatureV1:
    def __init__(self):
        self.TEMP_PRESETS = {
            "none": lambda t: (1.0, 1.0, 1.0),
            "tungsten": lambda t: (1.1 + 0.05 * math.sin(t * 0.1), 0.9, 0.8),
            "daylight": lambda t: (0.85, 0.95 + 0.05 * math.sin(t * 0.1), 1.1),
            "aging_print": lambda t: (1.0 + 0.1 * math.sin(t * 0.05), 
                                    0.9 + 0.05 * math.cos(t * 0.1), 
                                    0.8 + 0.15 * math.sin(t * 0.15)),
            "custom": None  # Handled separately
        }

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "temp_preset": (list(cls().TEMP_PRESETS.keys()),),
                "custom_r": ("STRING", {"default": "1.0"}),
                "custom_g": ("STRING", {"default": "1.0"}),
                "custom_b": ("STRING", {"default": "1.0"}),
                "intensity": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.05}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_temperature"
    CATEGORY = "postprocessing/video"

    def _parse_expression(self, expr, t):
        """Safely evaluate a simple math expression with 't' as variable"""
        # Replace common math functions with their values
        expr = expr.replace('sin', f'math.sin')
        expr = expr.replace('cos', f'math.cos')
        expr = expr.replace('t', str(t))
        try:
            return float(eval(expr))
        except:
            return 1.0  # Fallback to neutral value if expression is invalid

    def _apply_temperature_to_frame(self, image, r_mult, g_mult, b_mult):
        """Apply RGB multipliers to a single frame"""
        # Ensure the multipliers are tensors of the right shape
        r_mult = torch.tensor(r_mult, device=image.device)
        g_mult = torch.tensor(g_mult, device=image.device)
        b_mult = torch.tensor(b_mult, device=image.device)
        
        # Apply the multipliers to each channel
        result = image.clone()
        result[:, 0, :, :] *= r_mult
        result[:, 1, :, :] *= g_mult
        result[:, 2, :, :] *= b_mult
        
        # Clamp values to valid range
        return torch.clamp(result, 0.0, 1.0)

    def apply_temperature(self, images, temp_preset, custom_r, custom_g, custom_b, intensity):
        result = []
        batch_size = len(images)

        for i in range(batch_size):
            # Calculate time parameter (normalized to batch position)
            t = (i / max(1, batch_size - 1)) * 2 * math.pi

            # Get RGB multipliers based on preset or custom expressions
            if temp_preset == "custom":
                r_mult = self._parse_expression(custom_r, t)
                g_mult = self._parse_expression(custom_g, t)
                b_mult = self._parse_expression(custom_b, t)
            else:
                r_mult, g_mult, b_mult = self.TEMP_PRESETS[temp_preset](t)

            # Interpolate between no effect (1.0) and full effect based on intensity
            r_mult = 1.0 + (r_mult - 1.0) * intensity
            g_mult = 1.0 + (g_mult - 1.0) * intensity
            b_mult = 1.0 + (b_mult - 1.0) * intensity

            # Process the current frame
            frame = images[i:i+1]  # Keep batch dimension
            processed_frame = self._apply_temperature_to_frame(frame, r_mult, g_mult, b_mult)
            result.append(processed_frame)

        # Stack all processed frames back into a batch
        return (torch.cat(result, dim=0),)

NODE_CLASS_MAPPINGS = {
    "VideoTemperatureV1": VideoTemperatureV1
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VideoTemperatureV1": "Video Temperature Effect"
}