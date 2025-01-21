import numpy as np
import torch
import cv2

class VideoTrailsV2:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),  # Batch of images input
                "trail_strength": ("FLOAT", {
                    "default": 0.85,
                    "min": 0.1,
                    "max": 0.99,
                    "step": 0.01,
                    "display": "number"
                }),
                "decay_rate": ("FLOAT", {
                    "default": 0.15,
                    "min": 0.01,
                    "max": 0.5,
                    "step": 0.01,
                    "display": "number"
                }),
                "color_bleed": ("FLOAT", {
                    "default": 0.3,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.05,
                    "display": "number"
                }),
                "blur_amount": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.1,
                    "display": "number"
                }),
                "threshold": ("FLOAT", {
                    "default": 0.1,
                    "min": 0.01,
                    "max": 0.5,
                    "step": 0.01,
                    "display": "number"
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_trails_v2"
    CATEGORY = "image/effects"

    def detect_motion_v2(self, current, previous, threshold):
        """
        Detect motion using frame differencing with per-channel processing
        for more authentic color bleeding effects
        """
        # Convert to uint8 for CV2 operations
        curr_frame = (current * 255).astype(np.uint8)
        prev_frame = (previous * 255).astype(np.uint8)
        
        # Calculate difference for each channel separately
        diff_r = cv2.absdiff(curr_frame[..., 0], prev_frame[..., 0])
        diff_g = cv2.absdiff(curr_frame[..., 1], prev_frame[..., 1])
        diff_b = cv2.absdiff(curr_frame[..., 2], prev_frame[..., 2])
        
        # Apply threshold to each channel
        thresh = int(threshold * 255)
        mask_r = (diff_r > thresh).astype(np.float32)
        mask_g = (diff_g > thresh).astype(np.float32)
        mask_b = (diff_b > thresh).astype(np.float32)
        
        return np.stack([mask_r, mask_g, mask_b], axis=-1)

    def apply_gaussian_blur(self, image, strength):
        """Apply Gaussian blur with adjustable strength"""
        if strength <= 0:
            return image
            
        kernel_size = max(3, int(strength * 10) | 1)  # Ensure odd number
        sigma = strength * 2
        
        blurred = cv2.GaussianBlur(
            (image * 255).astype(np.uint8),
            (kernel_size, kernel_size),
            sigma
        )
        return blurred.astype(np.float32) / 255.0

    def apply_color_bleed(self, image, amount):
        """Apply color bleeding effect by slightly offsetting color channels"""
        if amount <= 0:
            return image
            
        offset = int(amount * 4)
        if offset == 0:
            return image
            
        height, width = image.shape[:2]
        result = np.zeros_like(image)
        
        # Offset red channel slightly right
        result[..., 0] = np.roll(image[..., 0], offset, axis=1)
        # Keep green channel centered
        result[..., 1] = image[..., 1]
        # Offset blue channel slightly left
        result[..., 2] = np.roll(image[..., 2], -offset, axis=1)
        
        # Handle edges
        result[:, :offset, 0] = image[:, :offset, 0]
        result[:, -offset:, 2] = image[:, -offset:, 2]
        
        return result

    def apply_trails_v2(self, images, trail_strength, decay_rate, color_bleed, blur_amount, threshold):
        """
        Apply enhanced video trails effect with exponential decay and color bleeding
        """
        print("\nStarting VideoTrailsV2 effect processing...")
        
        # Convert from torch tensor to numpy array
        batch_numpy = images.cpu().numpy()
        batch_size = batch_numpy.shape[0]
        
        # Initialize output batch and trail buffers (separate for each channel)
        processed_batch = np.zeros_like(batch_numpy)
        trail_buffer = np.zeros_like(batch_numpy[0])
        
        print(f"Processing {batch_size} frames...")
        
        for i in range(batch_size):
            current_frame = batch_numpy[i].copy()
            
            # Apply initial gaussian blur if enabled
            if blur_amount > 0:
                current_frame = self.apply_gaussian_blur(current_frame, blur_amount)
            
            # For frames after the first one, process trails
            if i > 0:
                # Detect motion between frames
                motion_mask = self.detect_motion_v2(
                    current_frame,
                    batch_numpy[i-1],
                    threshold
                )
                
                # Apply exponential decay to existing trails
                trail_buffer *= np.exp(-decay_rate)
                
                # Update trail buffer based on motion
                trail_buffer = np.where(
                    motion_mask > 0,
                    # Where motion is detected, add new trails
                    current_frame + trail_buffer * trail_strength,
                    # Where no motion, just keep decaying trails
                    trail_buffer
                )
                
                # Apply color bleeding effect
                if color_bleed > 0:
                    trail_buffer = self.apply_color_bleed(trail_buffer, color_bleed)
            else:
                # For first frame, initialize trail buffer
                trail_buffer = current_frame.copy()
            
            # Ensure values stay in valid range
            trail_buffer = np.clip(trail_buffer, 0, 1)
            
            # Store result
            processed_batch[i] = trail_buffer
        
        print("VideoTrailsV2 processing complete!")
        return (torch.from_numpy(processed_batch).to(images.device),)

# Node class mappings for ComfyUI
NODE_CLASS_MAPPINGS = {
    "VideoTrailsV2": VideoTrailsV2
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VideoTrailsV2": "Video Trails Effect V2"
}
