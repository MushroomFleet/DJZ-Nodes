import numpy as np
import torch
import cv2

class BatchAlphaComposite:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "bottom_images": ("IMAGE",),  # Bottom layer batch (RGB)
                "top_images": ("IMAGE",),     # Top layer batch (RGBA)
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_alpha_composite"
    CATEGORY = "image/processing"

    def process_frame(self, bottom_frame, top_frame):
        """
        Process a single frame pair using alpha compositing
        
        Args:
            bottom_frame: numpy array of shape (H, W, 3) in range [0, 1]
            top_frame: numpy array of shape (H, W, 4) in range [0, 1]
        """
        # Extract alpha channel from top frame
        alpha = top_frame[:, :, 3]
        
        # Expand alpha to match RGB channels
        alpha = np.expand_dims(alpha, axis=-1)
        
        # Extract RGB channels from top frame
        top_rgb = top_frame[:, :, :3]
        
        # Perform alpha compositing
        result = (alpha * top_rgb + (1 - alpha) * bottom_frame)
        
        return result

    def apply_alpha_composite(self, bottom_images, top_images):
        """
        Apply alpha compositing to batches of images
        
        Args:
            bottom_images: torch tensor of shape (B, H, W, 3) in range [0, 1]
            top_images: torch tensor of shape (B, H, W, 4) in range [0, 1]
        """
        # Convert from torch tensor to numpy array
        bottom_numpy = bottom_images.cpu().numpy()
        top_numpy = top_images.cpu().numpy()
        
        # Get batch dimensions
        batch_size = bottom_numpy.shape[0]
        
        # Validate input shapes
        if len(bottom_numpy.shape) != 4 or bottom_numpy.shape[-1] != 3:
            raise ValueError("Bottom layer must be in BHWC format with 3 channels")
        if len(top_numpy.shape) != 4 or top_numpy.shape[-1] != 4:
            raise ValueError("Top layer must be in BHWC format with 4 channels")
        
        # Process each image in the batch
        processed_batch = np.zeros_like(bottom_numpy)
        for i in range(batch_size):
            processed_batch[i] = self.process_frame(
                bottom_numpy[i],
                top_numpy[i]
            )
        
        # Convert back to torch tensor
        return (torch.from_numpy(processed_batch).to(bottom_images.device),)

NODE_CLASS_MAPPINGS = {
    "BatchAlphaComposite": BatchAlphaComposite
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BatchAlphaComposite": "Batch Alpha Composite"
}