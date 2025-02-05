import numpy as np
import torch
import cv2
import random

class VHS_Effect_v1:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),  # Batch of images input
                "luma_compression_rate": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 10.0,
                    "step": 0.1,
                }),
                "luma_noise_sigma": ("FLOAT", {
                    "default": 30.0,
                    "min": 0.0,
                    "max": 100.0,
                    "step": 1.0,
                }),
                "luma_noise_mean": ("FLOAT", {
                    "default": 0.0,
                    "min": -50.0,
                    "max": 50.0,
                    "step": 1.0,
                }),
                "chroma_compression_rate": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 10.0,
                    "step": 0.1,
                }),
                "chroma_noise_intensity": ("FLOAT", {
                    "default": 10.0,
                    "min": 0.0,
                    "max": 50.0,
                    "step": 1.0,
                }),
                "vertical_blur": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 21,
                    "step": 2,
                }),
                "horizontal_blur": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 21,
                    "step": 2,
                }),
                "border_size": ("FLOAT", {
                    "default": 1.7,
                    "min": 0.0,
                    "max": 10.0,
                    "step": 0.1,
                }),
                "generations": ("INT", {
                    "default": 3,
                    "min": 1,
                    "max": 10,
                    "step": 1,
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_vhs_effect"
    CATEGORY = "image/effects"

    def add_noise(self, image, mean=0, sigma=30):
        height, width, channels = image.shape
        gaussian_noise = np.random.normal(mean, sigma, (height, width, channels))
        noisy_image = np.clip(image + gaussian_noise, 0, 255).astype(np.uint8)
        return noisy_image

    def add_chroma_noise(self, image, intensity=10):
        height, width = image.shape[:2]
        noise_red = np.random.randint(-intensity, intensity, (height, width), dtype=np.int16)
        noise_green = np.random.randint(-intensity, intensity, (height, width), dtype=np.int16)
        noise_blue = np.random.randint(-intensity, intensity, (height, width), dtype=np.int16)
        
        image = image.copy()
        image[:, :, 0] = np.clip(image[:, :, 0] + noise_blue, 0, 255)
        image[:, :, 1] = np.clip(image[:, :, 1] + noise_green, 0, 255)
        image[:, :, 2] = np.clip(image[:, :, 2] + noise_red, 0, 255)
        return np.uint8(image)

    def cut_black_line_border(self, image, border_size):
        h, w, _ = image.shape
        line_width = int(w * (border_size / 100))
        image[:, -1 * line_width:] = 0
        return image

    def compress_luma(self, image, compression_rate, noise_mean, noise_sigma, border_size):
        height, width = image.shape[:2]
        compressed = cv2.resize(image, 
                              (int(width / compression_rate), height),
                              interpolation=cv2.INTER_LANCZOS4)
        noisy = self.add_noise(compressed, noise_mean, noise_sigma)
        restored = cv2.resize(noisy, (width, height),
                            interpolation=cv2.INTER_LANCZOS4)
        return self.cut_black_line_border(restored, border_size)

    def compress_chroma(self, image, compression_rate, noise_intensity, border_size):
        height, width = image.shape[:2]
        compressed = cv2.resize(image,
                              (int(width / compression_rate), height),
                              interpolation=cv2.INTER_LANCZOS4)
        noisy = self.add_chroma_noise(compressed, noise_intensity)
        restored = cv2.resize(noisy, (width, height),
                            interpolation=cv2.INTER_LANCZOS4)
        return self.cut_black_line_border(restored, border_size)

    def apply_waves(self, img, intensity=1.0):
        rows, cols = img.shape[:2]
        i, j = np.indices((rows, cols))
        waves = np.random.uniform(0.000, 1.110) * intensity
        offset_x = (waves * np.sin(250 * 2 * np.pi * i / (2 * cols))).astype(int)
        offset_j = np.clip(j + offset_x, 0, cols - 1)
        return img[i, offset_j]

    def apply_switch_noise(self, img):
        rows, cols = img.shape[:2]
        i, j = np.indices((rows, cols))
        waves = np.random.uniform(1.900, 1.910)
        offset_x = (waves * np.sin(np.cos(250) * 2 * np.pi * i / (2 * cols))).astype(int)
        offset_j = np.clip(j + (offset_x * np.random.randint(20, 30)), 0, cols - 1)
        return img[i, offset_j]

    def sharpen_image(self, image, kernel_size=(5, 5), sigma=100, alpha=1.5, beta=-0.5):
        blurred = cv2.GaussianBlur(image, kernel_size, sigma)
        sharpened = cv2.addWeighted(image, alpha, blurred, beta, 0)
        return np.clip(sharpened, 0, 255).astype(np.uint8)

    def process_frame(self, image, params):
        # Convert to YCrCb color space
        image_ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
        
        # Apply effects to luminance and chrominance separately
        luma_compressed = self.compress_luma(
            image_ycrcb, 
            params["luma_compression_rate"],
            params["luma_noise_mean"],
            params["luma_noise_sigma"],
            params["border_size"]
        )
        
        chroma_compressed = self.compress_chroma(
            image_ycrcb,
            params["chroma_compression_rate"],
            params["chroma_noise_intensity"],
            params["border_size"]
        )
        
        # Apply wave effects
        chroma_compressed = self.apply_waves(chroma_compressed)
        chroma_compressed = self.apply_waves(chroma_compressed)
        
        # Merge processed layers
        chrominance_layer = chroma_compressed[:, :, 1:3]
        merged_ycrcb = cv2.merge([luma_compressed[:, :, 0], chrominance_layer])
        
        # Convert back to BGR
        result = cv2.cvtColor(merged_ycrcb, cv2.COLOR_YCrCb2BGR)
        
        # Apply final effects
        result = cv2.blur(result, (params["horizontal_blur"], params["vertical_blur"]))
        result = self.sharpen_image(result)
        
        return result

    def apply_vhs_effect(self, images, luma_compression_rate, luma_noise_sigma, 
                        luma_noise_mean, chroma_compression_rate, chroma_noise_intensity,
                        vertical_blur, horizontal_blur, border_size, generations):
        
        # Convert from torch tensor to numpy array
        batch_numpy = images.cpu().numpy()
        batch_size, height, width, channels = batch_numpy.shape
        
        # Prepare parameters
        params = {
            "luma_compression_rate": luma_compression_rate,
            "luma_noise_sigma": luma_noise_sigma * generations,
            "luma_noise_mean": luma_noise_mean * generations,
            "chroma_compression_rate": chroma_compression_rate,
            "chroma_noise_intensity": chroma_noise_intensity * generations,
            "vertical_blur": vertical_blur if vertical_blur % 2 == 1 else vertical_blur + 1,
            "horizontal_blur": horizontal_blur if horizontal_blur % 2 == 1 else horizontal_blur + 1,
            "border_size": border_size,
        }
        
        # Process each image in the batch
        processed_batch = np.zeros_like(batch_numpy)
        for i in range(batch_size):
            # Convert to BGR for processing
            frame = (batch_numpy[i] * 255).astype(np.uint8)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            
            # Apply VHS effects
            frame = self.apply_switch_noise(frame)
            frame = self.process_frame(frame, params)
            frame = self.apply_waves(frame)
            frame = self.apply_waves(frame, 1.1)
            
            # Convert back to RGB and normalize
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            processed_batch[i] = frame.astype(np.float32) / 255.0
        
        # Convert back to torch tensor
        return (torch.from_numpy(processed_batch).to(images.device),)

NODE_CLASS_MAPPINGS = {
    "VHS_Effect_v1": VHS_Effect_v1
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VHS_Effect_v1": "VHS Effect v1"
}