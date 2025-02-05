import numpy as np
import torch
import cv2

class VideoTrails:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),  # Batch of images input
                "persistence": ("FLOAT", {
                    "default": 0.85,
                    "min": 0.1,
                    "max": 0.99,
                    "step": 0.01,
                    "display": "number"
                }),
                "fade_speed": ("FLOAT", {
                    "default": 0.15,
                    "min": 0.01,
                    "max": 0.5,
                    "step": 0.01,
                    "display": "number"
                }),
                "intensity": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 2.0,
                    "step": 0.1,
                    "display": "number"
                }),
                "motion_threshold": ("FLOAT", {
                    "default": 0.05,
                    "min": 0.01,
                    "max": 0.2,
                    "step": 0.01,
                    "display": "number"
                }),
                "blur_strength": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.1,
                    "display": "number"
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_trails"
    CATEGORY = "image/effects"

    def detect_motion(self, current, previous, threshold):
        """Detect motion between frames using optical flow"""
        # Convert frames to grayscale
        curr_gray = cv2.cvtColor((current * 255).astype(np.uint8), cv2.COLOR_RGB2GRAY)
        prev_gray = cv2.cvtColor((previous * 255).astype(np.uint8), cv2.COLOR_RGB2GRAY)
        
        # Calculate optical flow
        flow = cv2.calcOpticalFlowFarneback(
            prev_gray, curr_gray, 
            None, 0.5, 3, 15, 3, 5, 1.2, 0
        )
        
        # Calculate magnitude of flow
        magnitude = np.sqrt(flow[..., 0]**2 + flow[..., 1]**2)
        
        # Normalize and threshold
        magnitude = magnitude / magnitude.max()
        motion_mask = (magnitude > threshold).astype(np.float32)
        
        # Expand to 3 channels
        return np.stack([motion_mask] * 3, axis=-1)

    def apply_motion_blur(self, image, strength):
        """Apply directional motion blur"""
        if strength <= 0:
            return image
            
        kernel_size = int(strength * 20) | 1  # Ensure odd number
        kernel = np.zeros((kernel_size, kernel_size))
        mid = kernel_size // 2
        kernel[mid, :] = np.ones(kernel_size)  # Horizontal blur
        kernel = kernel / kernel.sum()
        
        blurred = cv2.filter2D((image * 255).astype(np.uint8), -1, kernel)
        return blurred.astype(np.float32) / 255.0

    def apply_trails(self, images, persistence, fade_speed, intensity, motion_threshold, blur_strength):
        """Apply video trails effect with accumulation and proper motion following"""
        print("\nStarting Enhanced Video Trails effect processing...")
        
        # Convert from torch tensor to numpy array
        batch_numpy = images.cpu().numpy()
        batch_size = batch_numpy.shape[0]
        
        # Initialize output batch and accumulation buffer
        processed_batch = np.zeros_like(batch_numpy)
        accumulation_buffer = np.zeros_like(batch_numpy[0])
        
        print(f"Processing {batch_size} frames with persistence {persistence}")
        
        for i in range(batch_size):
            print(f"Processing frame {i+1}/{batch_size}")
            
            current_frame = batch_numpy[i].copy()
            
            # Apply motion blur if enabled
            if blur_strength > 0:
                current_frame = self.apply_motion_blur(current_frame, blur_strength)
            
            # For frames after the first one, detect motion and update accumulation
            if i > 0:
                # Detect motion between current and previous frame
                motion_mask = self.detect_motion(
                    current_frame,
                    batch_numpy[i-1],
                    motion_threshold
                )
                
                # Update accumulation buffer based on motion
                accumulation_buffer = np.where(
                    motion_mask > 0,
                    # Where motion is detected, blend current frame with accumulated trails
                    current_frame * intensity + accumulation_buffer * persistence,
                    # Where no motion, gradually fade existing trails
                    accumulation_buffer * (1 - fade_speed)
                )
            else:
                # For first frame, initialize accumulation buffer
                accumulation_buffer = current_frame.copy()
            
            # Ensure values stay in valid range
            accumulation_buffer = np.clip(accumulation_buffer, 0, 1)
            
            # Store result
            processed_batch[i] = accumulation_buffer
        
        print("Enhanced Video Trails processing complete!")
        return (torch.from_numpy(processed_batch).to(images.device),)

# Node class mappings for ComfyUI
NODE_CLASS_MAPPINGS = {
    "VideoTrails": VideoTrails
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VideoTrails": "Video Trails Effect"
}