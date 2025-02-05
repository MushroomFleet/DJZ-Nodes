import numpy as np
import torch
import cv2

class MotionBlending:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),  # Batch of images input
                "mode": (["Motion Blur", "Frame Blending"],),
                "style": (["Simulated Shutter", "Temporal Blend"],),
                "intensity": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.05
                }),
                "angle": ("FLOAT", {
                    "default": 0.0,
                    "min": -180.0,
                    "max": 180.0,
                    "step": 1.0
                }),
                "kernel_size": ("INT", {
                    "default": 15,
                    "min": 3,
                    "max": 99,
                    "step": 2
                }),
                "frames_to_blend": ("INT", {
                    "default": 2,
                    "min": 2,
                    "max": 10,
                    "step": 1
                }),
                "decay_factor": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.05
                })
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_motion_effect"
    CATEGORY = "image/effects"

    def create_motion_kernel(self, kernel_size, angle, intensity):
        """Create a motion blur kernel based on angle and intensity."""
        kernel = np.zeros((kernel_size, kernel_size))
        center = kernel_size // 2
        
        # Convert angle to radians
        angle_rad = np.deg2rad(angle)
        
        # Calculate direction vector
        dx = np.cos(angle_rad)
        dy = np.sin(angle_rad)
        
        # Create the motion blur kernel
        for i in range(kernel_size):
            offset = i - center
            x = center + dx * offset * intensity
            y = center + dy * offset * intensity
            
            # Ensure coordinates are within bounds
            if 0 <= int(y) < kernel_size and 0 <= int(x) < kernel_size:
                kernel[int(y), int(x)] = 1
        
        # Normalize the kernel
        return kernel / np.sum(kernel)

    def apply_shutter_simulation(self, image, kernel_size, angle, intensity):
        """Apply motion blur using simulated shutter effect."""
        # Create motion blur kernel
        kernel = self.create_motion_kernel(kernel_size, angle, intensity)
        
        # Apply the kernel
        blurred = cv2.filter2D(image, -1, kernel)
        return blurred

    def apply_temporal_blend(self, image, frames_to_blend, decay_factor):
        """Apply temporal blending effect."""
        height, width = image.shape[:2]
        result = np.zeros_like(image, dtype=np.float32)
        
        # Create multiple offset versions of the image
        for i in range(frames_to_blend):
            offset = int(i * width / (frames_to_blend * 4))
            temp_image = np.roll(image, offset, axis=1)
            weight = decay_factor ** i
            result += temp_image * weight
        
        # Normalize the result
        result /= sum(decay_factor ** i for i in range(frames_to_blend))
        return np.clip(result, 0, 255).astype(np.uint8)

    def apply_motion_effect(self, images, mode, style, intensity, angle, 
                          kernel_size, frames_to_blend, decay_factor):
        # Convert from torch tensor to numpy array
        batch_numpy = images.cpu().numpy()
        batch_size, height, width, channels = batch_numpy.shape
        
        # Process each image in the batch
        processed_batch = np.zeros_like(batch_numpy)
        for i in range(batch_size):
            # Convert to uint8 for processing
            frame = (batch_numpy[i] * 255).astype(np.uint8)
            
            if mode == "Motion Blur":
                if style == "Simulated Shutter":
                    processed = self.apply_shutter_simulation(
                        frame, kernel_size, angle, intensity
                    )
                else:  # Temporal Blend
                    processed = self.apply_temporal_blend(
                        frame, frames_to_blend, decay_factor
                    )
            else:  # Frame Blending
                if style == "Simulated Shutter":
                    # Combine both effects for frame blending
                    motion_blur = self.apply_shutter_simulation(
                        frame, kernel_size, angle, intensity
                    )
                    processed = self.apply_temporal_blend(
                        motion_blur, frames_to_blend, decay_factor
                    )
                else:  # Temporal Blend
                    processed = self.apply_temporal_blend(
                        frame, frames_to_blend, decay_factor * 2
                    )
            
            # Normalize back to 0-1 range
            processed_batch[i] = processed.astype(np.float32) / 255.0
        
        # Convert back to torch tensor
        return (torch.from_numpy(processed_batch).to(images.device),)

NODE_CLASS_MAPPINGS = {
    "MotionBlending": MotionBlending
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MotionBlending": "Motion Blending"
}