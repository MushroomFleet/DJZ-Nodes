import numpy as np
import torch
import cv2
import os
from PIL import Image

class BorderCompositeAlpha:
    @classmethod
    def INPUT_TYPES(s):
        # List all PNG files in the /borders/ folder
        border_files = s.list_border_files()
        return {
            "required": {
                "bottom_images": ("IMAGE",),  # Bottom layer batch (RGB)
                "border_image": (border_files,),  # Dropdown with border image filenames
            },
        }
    
    @classmethod
    def list_border_files(s):
        # List all PNG files in the /borders/ folder
        border_dir = os.path.join(os.path.dirname(__file__), "borders")
        if not os.path.exists(border_dir):
            return ["no_borders_found.png"]
        
        border_files = [f for f in os.listdir(border_dir) if f.lower().endswith('.png')]
        if not border_files:
            return ["no_borders_found.png"]
        
        return border_files

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

    def load_border_image(self, border_filename, target_height, target_width):
        """
        Load a border image from the /borders/ folder and resize if needed
        
        Args:
            border_filename: Name of the border image file
            target_height: Height to resize to
            target_width: Width to resize to
        """
        border_path = os.path.join(os.path.dirname(__file__), "borders", border_filename)
        
        # Load the image using PIL (which handles alpha channel properly)
        try:
            border_img = Image.open(border_path).convert('RGBA')
            
            # Resize if dimensions don't match
            if border_img.height != target_height or border_img.width != target_width:
                border_img = border_img.resize((target_width, target_height), Image.LANCZOS)
            
            # Convert to numpy array and normalize to [0, 1]
            border_array = np.array(border_img).astype(np.float32) / 255.0
            
            return border_array
        except Exception as e:
            print(f"Error loading border image: {e}")
            # Return a transparent image as fallback
            return np.zeros((target_height, target_width, 4), dtype=np.float32)

    def apply_alpha_composite(self, bottom_images, border_image):
        """
        Apply border overlay to batch of images using alpha compositing
        
        Args:
            bottom_images: torch tensor of shape (B, H, W, 3) in range [0, 1]
            border_image: filename of the border image to use
        """
        # Convert from torch tensor to numpy array
        bottom_numpy = bottom_images.cpu().numpy()
        
        # Get batch dimensions
        batch_size, height, width, _ = bottom_numpy.shape
        
        # Validate input shapes
        if len(bottom_numpy.shape) != 4 or bottom_numpy.shape[-1] != 3:
            raise ValueError("Bottom layer must be in BHWC format with 3 channels")
        
        # Load the selected border image
        border_numpy = self.load_border_image(border_image, height, width)
        
        # Create a batch of border images (repeat the same border for all images)
        top_numpy = np.repeat(border_numpy[np.newaxis, :, :, :], batch_size, axis=0)
        
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
    "BorderCompositeAlpha": BorderCompositeAlpha
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BorderCompositeAlpha": "Border Composite Alpha"
}
