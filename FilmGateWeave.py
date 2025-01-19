import numpy as np
import torch
import cv2
import random
import math

class FilmGateWeave:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),  # Batch of images input
                "weave_preset": (["none", "subtle", "moderate", "heavy", "custom"], {
                    "default": "subtle"
                }),
                "custom_expression": ("STRING", {
                    "default": "sin(t * 0.1) * 5",
                    "multiline": False
                }),
                "amplitude_x": ("FLOAT", {
                    "default": 3.0,
                    "min": 0.0,
                    "max": 20.0,
                    "step": 0.1
                }),
                "amplitude_y": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 20.0,
                    "step": 0.1
                }),
                "frequency": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 5.0,
                    "step": 0.1
                }),
                "phase_shift": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 2*math.pi,
                    "step": 0.1
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_film_gate_weave"
    CATEGORY = "image/effects"

    def evaluate_expression(self, expression, t):
        """Safely evaluate mathematical expressions for custom weave patterns"""
        # Create a safe dict with math functions
        safe_dict = {
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'pi': math.pi,
            't': t
        }
        try:
            # Replace common math functions with their math module equivalents
            expression = expression.replace('math.', '')
            return eval(expression, {"__builtins__": {}}, safe_dict)
        except:
            return 0.0

    def get_preset_parameters(self, preset):
        """Define presets for common weave patterns"""
        presets = {
            "none": {
                "amplitude_x": 0.0,
                "amplitude_y": 0.0,
                "frequency": 1.0,
                "phase_shift": 0.0,
                "expression": "0"
            },
            "subtle": {
                "amplitude_x": 2.0,
                "amplitude_y": 0.5,
                "frequency": 0.8,
                "phase_shift": 0.2,
                "expression": "sin(t * 0.8) * 2"
            },
            "moderate": {
                "amplitude_x": 4.0,
                "amplitude_y": 1.0,
                "frequency": 1.2,
                "phase_shift": 0.4,
                "expression": "sin(t * 1.2) * 4 + cos(t * 0.6) * 2"
            },
            "heavy": {
                "amplitude_x": 8.0,
                "amplitude_y": 2.0,
                "frequency": 1.5,
                "phase_shift": 0.6,
                "expression": "sin(t * 1.5) * 8 + cos(t * 0.75) * 4"
            }
        }
        return presets.get(preset, None)

    def apply_weave(self, image, frame_idx, total_frames, params):
        """Apply the weave effect to a single frame"""
        rows, cols = image.shape[:2]
        
        # Create mesh grid for transformation
        y, x = np.mgrid[0:rows, 0:cols]
        
        # Calculate time parameter (normalized between 0 and 2π)
        t = (frame_idx / max(1, total_frames-1)) * 2 * math.pi * params["frequency"] + params["phase_shift"]
        
        if params.get("expression"):
            # Use custom expression if provided
            offset_x = self.evaluate_expression(params["expression"], t)
            offset_y = self.evaluate_expression(params["expression"], t + math.pi/2)  # Phase shifted for y
        else:
            # Use standard sinusoidal movement
            offset_x = math.sin(t) * params["amplitude_x"]
            offset_y = math.cos(t) * params["amplitude_y"]
        
        # Apply the offsets
        x_mapped = np.clip(x + offset_x, 0, cols-1).astype(np.float32)
        y_mapped = np.clip(y + offset_y, 0, rows-1).astype(np.float32)
        
        # Remap the image
        return cv2.remap(image, x_mapped, y_mapped, cv2.INTER_LINEAR)

    def apply_film_gate_weave(self, images, weave_preset, custom_expression, 
                            amplitude_x, amplitude_y, frequency, phase_shift):
        # Convert from torch tensor to numpy array
        batch_numpy = images.cpu().numpy()
        batch_size, height, width, channels = batch_numpy.shape
        
        # Get parameters based on preset or use custom values
        if weave_preset != "custom":
            preset_params = self.get_preset_parameters(weave_preset)
            if preset_params:
                amplitude_x = preset_params["amplitude_x"]
                amplitude_y = preset_params["amplitude_y"]
                frequency = preset_params["frequency"]
                phase_shift = preset_params["phase_shift"]
                custom_expression = preset_params["expression"]
        
        params = {
            "amplitude_x": amplitude_x,
            "amplitude_y": amplitude_y,
            "frequency": frequency,
            "phase_shift": phase_shift,
            "expression": custom_expression if weave_preset == "custom" else None
        }
        
        # Process each frame in the batch
        processed_batch = np.zeros_like(batch_numpy)
        for i in range(batch_size):
            # Convert to appropriate format for processing
            frame = (batch_numpy[i] * 255).astype(np.uint8)
            
            # Apply the weave effect
            processed = self.apply_weave(frame, i, batch_size, params)
            
            # Normalize back to float32
            processed_batch[i] = processed.astype(np.float32) / 255.0
        
        # Convert back to torch tensor
        return (torch.from_numpy(processed_batch).to(images.device),)

NODE_CLASS_MAPPINGS = {
    "FilmGateWeave": FilmGateWeave
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FilmGateWeave": "Film Gate Weave"
}