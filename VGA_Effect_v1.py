import numpy as np
import torch
import cv2

class VGA_Effect_v1:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),  # Batch of images input
                "horizontal_resolution": ("INT", {
                    "default": 640,
                    "min": 320,
                    "max": 1024,
                    "step": 8,
                }),
                "vertical_resolution": ("INT", {
                    "default": 480,
                    "min": 240,
                    "max": 768,
                    "step": 8,
                }),
                "refresh_rate": ("INT", {
                    "default": 60,
                    "min": 30,
                    "max": 75,
                    "step": 1,
                }),
                "scan_line_intensity": ("FLOAT", {
                    "default": 0.15,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                }),
                "phosphor_persistence": ("FLOAT", {
                    "default": 0.2,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                }),
                "color_bleed": ("FLOAT", {
                    "default": 0.3,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                }),
                "signal_noise": ("FLOAT", {
                    "default": 0.05,
                    "min": 0.0,
                    "max": 0.5,
                    "step": 0.01,
                }),
                "horizontal_sync_jitter": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.0,
                    "max": 5.0,
                    "step": 0.1,
                }),
                "vertical_sync_jitter": ("FLOAT", {
                    "default": 0.2,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.1,
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_vga_effect"
    CATEGORY = "image/effects"

    def create_scanlines(self, height, width, intensity):
        # Create the intensity pattern and reshape it for proper broadcasting
        intensity_pattern = np.array([1.0, 1.0 - intensity])[:, np.newaxis]
        scanline_pattern = np.ones((2, width)) * intensity_pattern
        scanlines = np.tile(scanline_pattern, (height // 2 + 1, 1))[:height]
        return scanlines[:, :, np.newaxis]

    def apply_horizontal_jitter(self, image, amount):
        rows, cols = image.shape[:2]
        # Generate jitter offset for each row
        jitter = np.random.normal(0, amount, rows).astype(np.int32)
        # Create meshgrid for proper broadcasting
        row_indices, col_indices = np.meshgrid(np.arange(rows), np.arange(cols), indexing='ij')
        # Apply jitter to column indices
        jittered_cols = np.clip(col_indices + jitter[:, np.newaxis], 0, cols - 1)
        # Apply jitter using advanced indexing
        return image[row_indices, jittered_cols]

    def apply_vertical_jitter(self, image, amount):
        rows, cols = image.shape[:2]
        # Generate jitter offset for each column
        jitter = np.random.normal(0, amount, cols).astype(np.int32)
        # Create meshgrid for proper broadcasting
        row_indices, col_indices = np.meshgrid(np.arange(rows), np.arange(cols), indexing='ij')
        # Apply jitter to row indices
        jittered_rows = np.clip(row_indices + jitter[np.newaxis, :], 0, rows - 1)
        # Apply jitter using advanced indexing
        return image[jittered_rows, col_indices]

    def apply_color_bleed(self, image, amount):
        kernel_size = int(amount * 10) * 2 + 1
        color_channels = cv2.split(image)
        blurred_channels = []
        
        for i, channel in enumerate(color_channels):
            # Apply horizontal blur with different kernel sizes for each channel
            kernel = np.zeros((1, kernel_size))
            kernel[0, kernel_size//2:] = np.linspace(0, 1, kernel_size//2 + 1)
            kernel = kernel / kernel.sum()
            blurred = cv2.filter2D(channel, -1, kernel)
            blurred_channels.append(blurred)
            
        return cv2.merge(blurred_channels)

    def apply_signal_noise(self, image, intensity):
        noise = np.random.normal(0, intensity * 255, image.shape)
        noisy_image = np.clip(image + noise, 0, 255).astype(np.uint8)
        return noisy_image

    def apply_phosphor_persistence(self, image, amount):
        kernel_size = int(amount * 20) * 2 + 1
        kernel = np.zeros((kernel_size, 1))
        kernel[:kernel_size//2 + 1, 0] = np.linspace(1, 0, kernel_size//2 + 1)
        kernel = kernel / kernel.sum()
        return cv2.filter2D(image, -1, kernel)

    def resize_vga(self, image, h_res, v_res):
        # First downscale to VGA resolution
        downscaled = cv2.resize(image, (h_res, v_res), interpolation=cv2.INTER_LINEAR)
        # Then upscale back to original size with nearest neighbor to maintain pixelation
        return cv2.resize(downscaled, (image.shape[1], image.shape[0]), interpolation=cv2.INTER_NEAREST)

    def apply_vga_effect(self, images, horizontal_resolution, vertical_resolution, 
                        refresh_rate, scan_line_intensity, phosphor_persistence,
                        color_bleed, signal_noise, horizontal_sync_jitter,
                        vertical_sync_jitter):
        
        # Convert from torch tensor to numpy array
        batch_numpy = images.cpu().numpy()
        batch_size, height, width, channels = batch_numpy.shape
        
        # Process each image in the batch
        processed_batch = np.zeros_like(batch_numpy)
        for i in range(batch_size):
            # Convert to uint8 for processing
            frame = (batch_numpy[i] * 255).astype(np.uint8)
            
            # Apply VGA effects
            frame = self.resize_vga(frame, horizontal_resolution, vertical_resolution)
            frame = self.apply_color_bleed(frame, color_bleed)
            frame = self.apply_horizontal_jitter(frame, horizontal_sync_jitter)
            frame = self.apply_vertical_jitter(frame, vertical_sync_jitter)
            frame = self.apply_phosphor_persistence(frame, phosphor_persistence)
            frame = self.apply_signal_noise(frame, signal_noise)
            
            # Apply scanlines
            scanlines = self.create_scanlines(height, width, scan_line_intensity)
            frame = frame * scanlines
            
            # Normalize back to float32
            processed_batch[i] = np.clip(frame, 0, 255).astype(np.float32) / 255.0
        
        # Convert back to torch tensor
        return (torch.from_numpy(processed_batch).to(images.device),)

NODE_CLASS_MAPPINGS = {
    "VGA_Effect_v1": VGA_Effect_v1
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VGA_Effect_v1": "VGA Effect v1"
}
