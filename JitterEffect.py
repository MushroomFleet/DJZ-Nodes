import torch
import numpy as np
import cv2
from typing import Tuple

class JitterEffect:
    """ComfyUI node for applying jitter/shake effects to image sequences"""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),  # Batch of images input
                "x_amplitude": ("INT", {
                    "default": 3,
                    "min": 0,
                    "max": 50,
                    "step": 1,
                    "display": "slider"
                }),
                "y_amplitude": ("INT", {
                    "default": 3,
                    "min": 0,
                    "max": 50,
                    "step": 1,
                    "display": "slider"
                }),
                "rotation_angle": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 5.0,
                    "step": 0.1,
                    "display": "slider"
                }),
                "frame_coherence": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "display": "slider"
                }),
                "border_mode": (["CONSTANT", "REPLICATE", "REFLECT"], {
                    "default": "REPLICATE"
                }),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 2147483647
                })
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_jitter_effect"
    CATEGORY = "image/effects"

    def apply_jitter(self, image: np.ndarray, dx: float, dy: float, 
                    angle: float, border_mode: str) -> np.ndarray:
        """Apply frame jitter with translation and rotation"""
        height, width = image.shape[:2]
        
        # Create rotation matrix around center
        center = (width / 2, height / 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        
        # Add translation to matrix
        M[0, 2] += dx
        M[1, 2] += dy
        
        # Convert border mode string to cv2 constant
        border_modes = {
            "CONSTANT": cv2.BORDER_CONSTANT,
            "REPLICATE": cv2.BORDER_REPLICATE,
            "REFLECT": cv2.BORDER_REFLECT
        }
        cv2_border_mode = border_modes[border_mode]
        
        # Apply transformation
        if len(image.shape) == 3:
            result = np.zeros_like(image)
            for c in range(image.shape[2]):
                result[:,:,c] = cv2.warpAffine(
                    image[:,:,c], 
                    M, 
                    (width, height),
                    borderMode=cv2_border_mode
                )
        else:
            result = cv2.warpAffine(
                image, 
                M, 
                (width, height),
                borderMode=cv2_border_mode
            )
            
        return result

    def apply_jitter_effect(
        self,
        images: torch.Tensor,
        x_amplitude: int,
        y_amplitude: int,
        rotation_angle: float,
        frame_coherence: float,
        border_mode: str,
        seed: int
    ) -> Tuple[torch.Tensor]:
        """
        Apply jitter effect to a batch of images with frame coherence
        """
        # Convert from torch tensor to numpy array
        batch_numpy = images.cpu().numpy()
        
        # Initialize RNG
        rng = np.random.RandomState(seed)
        
        # Initialize previous offsets for frame coherence
        prev_dx = 0
        prev_dy = 0
        prev_angle = 0
        
        # Process each image in the batch
        processed_batch = np.zeros_like(batch_numpy)
        for i in range(len(batch_numpy)):
            image = batch_numpy[i]
            
            # Generate new random values
            new_dx = rng.randint(-x_amplitude, x_amplitude + 1)
            new_dy = rng.randint(-y_amplitude, y_amplitude + 1)
            new_angle = rng.uniform(-rotation_angle, rotation_angle)
            
            # Blend with previous values for frame coherence
            dx = prev_dx * frame_coherence + new_dx * (1 - frame_coherence)
            dy = prev_dy * frame_coherence + new_dy * (1 - frame_coherence)
            angle = prev_angle * frame_coherence + new_angle * (1 - frame_coherence)
            
            # Store current values as previous for next frame
            prev_dx = dx
            prev_dy = dy
            prev_angle = angle
            
            # Apply jitter effect
            processed_batch[i] = self.apply_jitter(
                image, dx, dy, angle, border_mode
            )
        
        # Convert back to torch tensor
        return (torch.from_numpy(processed_batch).to(images.device),)

NODE_CLASS_MAPPINGS = {
    "JitterEffect": JitterEffect
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "JitterEffect": "Jitter Effect"
}
