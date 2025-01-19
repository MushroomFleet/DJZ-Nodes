import numpy as np
import torch
import cv2
import random
import math

class VideoVignettingV1:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),  # Batch of images input
                "vignette_type": (["Mechanical", "Chemical", "Both", "None"],),
                "mechanical_intensity": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.05,
                }),
                "mechanical_feather": ("FLOAT", {
                    "default": 0.3,
                    "min": 0.1,
                    "max": 1.0,
                    "step": 0.05,
                }),
                "chemical_intensity": ("FLOAT", {
                    "default": 0.4,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.05,
                }),
                "chemical_irregularity": ("FLOAT", {
                    "default": 0.2,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.05,
                }),
                "temporal_variance": (["None", "Sine", "Random", "Pulse", "Custom"],),
                "custom_expression": ("STRING", {
                    "default": "sin(t * 0.1) * 0.2",
                    "multiline": False
                }),
                "variance_speed": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 5.0,
                    "step": 0.1,
                }),
                "variance_amplitude": ("FLOAT", {
                    "default": 0.2,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.05,
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_vignette_effect"
    CATEGORY = "image/effects"

    def create_mechanical_vignette(self, height, width, intensity, feather):
        # Create a radial gradient from the center
        y, x = np.ogrid[-height/2:height/2, -width/2:width/2]
        radius = np.sqrt(x*x + y*y)
        
        # Normalize radius to [0, 1] range
        max_radius = np.sqrt((height/2)**2 + (width/2)**2)
        normalized_radius = radius / max_radius
        
        # Create vignette mask
        vignette = 1 - normalized_radius * intensity
        # Apply feathering using sigmoid function
        vignette = 1 / (1 + np.exp((normalized_radius - feather) / (feather * 0.2)))
        
        return np.clip(vignette, 0, 1)

    def create_chemical_vignette(self, height, width, intensity, irregularity):
        # Create base radial gradient
        y, x = np.ogrid[-height/2:height/2, -width/2:width/2]
        radius = np.sqrt(x*x + y*y)
        
        # Add Perlin-like noise for irregular edges
        noise = np.zeros((height, width))
        scale = 50  # Scale of the noise
        for i in range(4):  # Multiple octaves of noise
            freq = 2**i
            amp = irregularity * 0.5**i
            # Generate and resize noise before adding
            current_noise = np.random.rand(
                int(height/scale*freq), 
                int(width/scale*freq)
            )
            current_noise = cv2.resize(current_noise, (width, height))
            noise += amp * current_noise
        
        # Normalize noise to [0, 1]
        noise = (noise - noise.min()) / (noise.max() - noise.min())
        
        # Combine base vignette with noise
        max_radius = np.sqrt((height/2)**2 + (width/2)**2)
        vignette = 1 - (radius / max_radius + noise * irregularity) * intensity
        
        return np.clip(vignette, 0, 1)

    def evaluate_temporal_variance(self, t, variance_type, custom_expr, speed, amplitude):
        if variance_type == "None":
            return 1.0
        elif variance_type == "Sine":
            return 1.0 + np.sin(t * speed) * amplitude
        elif variance_type == "Random":
            return 1.0 + (random.random() * 2 - 1) * amplitude
        elif variance_type == "Pulse":
            return 1.0 + amplitude * (1 if np.sin(t * speed) > 0 else 0)
        elif variance_type == "Custom":
            try:
                # Create safe math environment
                safe_dict = {
                    "sin": math.sin,
                    "cos": math.cos,
                    "tan": math.tan,
                    "exp": math.exp,
                    "log": math.log,
                    "pi": math.pi,
                    "t": t
                }
                # Evaluate custom expression
                result = eval(custom_expr, {"__builtins__": {}}, safe_dict)
                return 1.0 + float(result)
            except:
                print(f"Error evaluating custom expression: {custom_expr}")
                return 1.0

    def apply_vignette_effect(
        self, images, vignette_type, mechanical_intensity, mechanical_feather,
        chemical_intensity, chemical_irregularity, temporal_variance,
        custom_expression, variance_speed, variance_amplitude
    ):
        # Convert from torch tensor to numpy array
        batch_numpy = images.cpu().numpy()
        batch_size, height, width, channels = batch_numpy.shape
        
        # Process each image in the batch
        processed_batch = np.zeros_like(batch_numpy)
        for i in range(batch_size):
            # Get temporal variance factor
            t = i * variance_speed
            variance = self.evaluate_temporal_variance(
                t, temporal_variance, custom_expression,
                variance_speed, variance_amplitude
            )
            
            # Initialize combined vignette mask
            combined_mask = np.ones((height, width))
            
            if vignette_type in ["Mechanical", "Both"]:
                mech_mask = self.create_mechanical_vignette(
                    height, width,
                    mechanical_intensity * variance,
                    mechanical_feather
                )
                combined_mask *= mech_mask
            
            if vignette_type in ["Chemical", "Both"]:
                chem_mask = self.create_chemical_vignette(
                    height, width,
                    chemical_intensity * variance,
                    chemical_irregularity
                )
                combined_mask *= chem_mask
            
            # Expand mask to match image channels
            combined_mask = np.expand_dims(combined_mask, axis=2)
            combined_mask = np.repeat(combined_mask, channels, axis=2)
            
            # Apply vignette effect
            processed_batch[i] = batch_numpy[i] * combined_mask
        
        # Convert back to torch tensor
        return (torch.from_numpy(processed_batch).to(images.device),)

NODE_CLASS_MAPPINGS = {
    "VideoVignettingV1": VideoVignettingV1
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VideoVignettingV1": "Video Vignetting v1"
}
