import numpy as np
import torch
import cv2
from concurrent.futures import ThreadPoolExecutor

class KeyframeBasedUpscalerV1:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),  # Batch of images input
                "scale_factor": ("FLOAT", {
                    "default": 2.0,
                    "min": 1.0,
                    "max": 4.0,
                    "step": 0.5,
                }),
                "keyframe_threshold": ("FLOAT", {
                    "default": 30.0,
                    "min": 0.0,
                    "max": 100.0,
                    "step": 1.0,
                    "description": "Threshold for keyframe detection"
                }),
                "temporal_window": ("INT", {
                    "default": 5,
                    "min": 1,
                    "max": 15,
                    "step": 1,
                    "description": "Number of frames to consider for temporal analysis"
                }),
                "quality_preservation": ("FLOAT", {
                    "default": 0.8,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.1,
                    "description": "Balance between speed and quality"
                }),
                "motion_sensitivity": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.1,
                    "description": "Sensitivity to motion for keyframe detection"
                }),
                "interpolation_method": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 2,
                    "step": 1,
                    "description": "0: Linear, 1: Cubic, 2: Lanczos"
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_keyframe_upscaling"
    CATEGORY = "image/upscaling"

    def get_frame_signature(self, frame):
        """Calculate frame signature using multiple features for robust comparison"""
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        
        # Calculate features at multiple scales
        signatures = []
        for scale in [32, 64]:
            # Downscale for different granularities
            downscaled = cv2.resize(gray, (scale, scale))
            
            # Edge detection for structural information
            edges = cv2.Sobel(downscaled, cv2.CV_64F, 1, 1)
            
            # Normalize and add to signatures
            signatures.append(cv2.normalize(downscaled, None, 0, 1, cv2.NORM_MINMAX))
            signatures.append(cv2.normalize(edges, None, 0, 1, cv2.NORM_MINMAX))
        
        return np.concatenate([sig.flatten() for sig in signatures])

    def calculate_frame_difference(self, frame1, frame2, sensitivity):
        """Calculate difference between frames using multiple metrics"""
        # Get frame signatures
        signature1 = self.get_frame_signature(frame1)
        signature2 = self.get_frame_signature(frame2)
        
        # Calculate structural difference
        structural_diff = np.mean((signature1 - signature2) ** 2)
        
        # Calculate motion using optical flow with different parameters based on sensitivity
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_RGB2GRAY)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_RGB2GRAY)
        
        if sensitivity > 0:
            # Adjust optical flow parameters based on sensitivity
            pyr_scale = 0.5
            levels = int(3 + sensitivity * 2)  # More levels for higher sensitivity
            winsize = int(10 + sensitivity * 10)  # Larger window for higher sensitivity
            iterations = int(2 + sensitivity * 3)
            
            flow = cv2.calcOpticalFlowFarneback(
                gray1, gray2, None, pyr_scale, levels, winsize,
                iterations, 5, 1.2, 0
            )
            
            # Calculate motion metrics
            magnitude = np.sqrt(flow[..., 0]**2 + flow[..., 1]**2)
            motion_diff = np.mean(magnitude) * sensitivity
            
            # Combine structural and motion differences
            return (structural_diff * (1 - sensitivity) + motion_diff * sensitivity) * 100
        
        return structural_diff * 100

    def high_quality_upscale(self, frame, scale_factor, interpolation_method):
        """High quality upscaling for keyframes"""
        methods = [cv2.INTER_LINEAR, cv2.INTER_CUBIC, cv2.INTER_LANCZOS4]
        h, w = frame.shape[:2]
        return cv2.resize(frame, 
                         (int(w * scale_factor), int(h * scale_factor)),
                         interpolation=methods[interpolation_method])

    def fast_upscale(self, frame, scale_factor):
        """Fast upscaling for non-keyframes"""
        h, w = frame.shape[:2]
        return cv2.resize(frame, 
                         (int(w * scale_factor), int(h * scale_factor)),
                         interpolation=cv2.INTER_LINEAR)

    def temporal_blend(self, frames, weights, quality_preservation):
        """Blend multiple frames using temporal weights with quality preservation"""
        result = np.zeros_like(frames[0], dtype=np.float32)
        
        # Apply gaussian weights based on temporal distance and quality preservation
        sigma = 1.0 / (quality_preservation + 0.1)  # Adjust blur based on quality
        weights = np.array(weights)
        weights = np.exp(-np.arange(len(weights))**2 / (2 * sigma**2))
        weights = weights / weights.sum()  # Normalize
        
        # Blend frames
        for frame, weight in zip(frames, weights):
            result += frame.astype(np.float32) * weight
        
        # Apply sharpening based on quality preservation
        if quality_preservation > 0.5:
            kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]]) * quality_preservation
            result = cv2.filter2D(result, -1, kernel)
            
        return np.clip(result, 0, 255).astype(np.uint8)

    def apply_keyframe_upscaling(
        self, images, scale_factor, keyframe_threshold,
        temporal_window, quality_preservation, motion_sensitivity,
        interpolation_method
    ):
        # Convert from torch tensor to numpy array
        batch_numpy = images.cpu().numpy()
        batch_size, height, width, channels = batch_numpy.shape
        
        # Convert to 0-255 range for processing
        batch_numpy = (batch_numpy * 255).astype(np.uint8)
        
        # Initialize output array
        new_height = int(height * scale_factor)
        new_width = int(width * scale_factor)
        processed_batch = np.zeros((batch_size, new_height, new_width, channels),
                                 dtype=np.float32)
        
        # Identify keyframes using sliding window approach
        keyframes = [0]  # First frame is always a keyframe
        window_size = min(temporal_window, batch_size)
        
        for i in range(1, batch_size):
            # Calculate differences within temporal window
            start_idx = max(0, i - window_size)
            window_frames = batch_numpy[start_idx:i+1]
            
            # Calculate differences with previous frames in window
            diffs = []
            for j in range(len(window_frames)-1):
                diff = self.calculate_frame_difference(
                    window_frames[j], window_frames[-1], motion_sensitivity
                )
                diffs.append(diff)
            
            # Use mean difference for more stable detection
            mean_diff = np.mean(diffs) if diffs else 0
            if mean_diff > keyframe_threshold or i - keyframes[-1] >= temporal_window:
                keyframes.append(i)
        
        if keyframes[-1] != batch_size - 1:
            keyframes.append(batch_size - 1)  # Ensure last frame is a keyframe
        
        # Process frames using parallel processing for efficiency
        def process_frame(i):
            if i in keyframes:
                # High quality processing for keyframes
                return self.high_quality_upscale(
                    batch_numpy[i], scale_factor, interpolation_method
                )
            else:
                # Find relevant keyframes within temporal window
                prev_keys = [k for k in keyframes if k <= i][-temporal_window:]
                next_keys = [k for k in keyframes if k > i][:temporal_window]
                
                # Gather frames and calculate weights
                frames = []
                weights = []
                
                for k in prev_keys:
                    dist = i - k
                    if dist <= temporal_window:
                        frames.append(batch_numpy[k])
                        weights.append(1.0 / (dist + 1))
                        
                for k in next_keys:
                    dist = k - i
                    if dist <= temporal_window:
                        frames.append(batch_numpy[k])
                        weights.append(1.0 / (dist + 1))
                
                # Normalize weights
                weights = np.array(weights)
                weights = weights / weights.sum()
                
                # Blend frames and upscale
                blended = self.temporal_blend(frames, weights, quality_preservation)
                return self.fast_upscale(blended, scale_factor)
        
        # Process frames in parallel
        with ThreadPoolExecutor() as executor:
            results = list(executor.map(process_frame, range(batch_size)))
            for i, result in enumerate(results):
                processed_batch[i] = result
        
        # Convert back to 0-1 range and torch tensor
        processed_batch = processed_batch.astype(np.float32) / 255.0
        return (torch.from_numpy(processed_batch).to(images.device),)

NODE_CLASS_MAPPINGS = {
    "KeyframeBasedUpscalerV1": KeyframeBasedUpscalerV1
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "KeyframeBasedUpscalerV1": "Keyframe Based Upscaler v1"
}
