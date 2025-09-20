import numpy as np
import torch
import cv2
import math

class DJZ_ParallaxV1:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "background_image": ("IMAGE",),
                "image_1": ("IMAGE",),
                "mask_1": ("MASK",),
                "image_2": ("IMAGE",),
                "mask_2": ("MASK",),
                "fps": ("INT", {"default": 24, "min": 1, "max": 60}),
                "max_frames": ("INT", {"default": 60, "min": 1, "max": 1000}),
                "height": ("INT", {"default": 512, "min": 64, "max": 2048}),
                "width": ("INT", {"default": 512, "min": 64, "max": 2048}),
                "background_speed": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.1}),
                "background_direction": ("FLOAT", {"default": 0.0, "min": -360.0, "max": 360.0, "step": 1.0}),
                "image_1_speed": ("FLOAT", {"default": 2.0, "min": -10.0, "max": 10.0, "step": 0.1}),
                "image_1_direction": ("FLOAT", {"default": 0.0, "min": -360.0, "max": 360.0, "step": 1.0}),
                "image_2_speed": ("FLOAT", {"default": 3.0, "min": -10.0, "max": 10.0, "step": 0.1}),
                "image_2_direction": ("FLOAT", {"default": 0.0, "min": -360.0, "max": 360.0, "step": 1.0}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "create_parallax_animation"
    CATEGORY = "image/animation"

    def calculate_offset(self, frame_index, speed, direction):
        """
        Calculate x,y offset for a layer at given frame
        
        Args:
            frame_index: Current frame number
            speed: Movement speed in pixels per frame
            direction: Movement direction in degrees (0=right, 90=down, 180=left, 270=up)
        """
        # Convert direction to radians
        direction_rad = math.radians(direction)
        
        # Calculate offset components
        offset_x = speed * frame_index * math.cos(direction_rad)
        offset_y = speed * frame_index * math.sin(direction_rad)
        
        return int(offset_x), int(offset_y)

    def sample_layer(self, image, mask, offset_x, offset_y, target_height, target_width):
        """
        Sample a layer at given offset with wrapping/tiling behavior
        
        Args:
            image: numpy array of shape (H, W, 3)
            mask: numpy array of shape (H, W) 
            offset_x, offset_y: pixel offsets
            target_height, target_width: output dimensions
        """
        img_h, img_w = image.shape[:2]
        
        # Create output arrays
        sampled_image = np.zeros((target_height, target_width, 3), dtype=image.dtype)
        sampled_mask = np.zeros((target_height, target_width), dtype=mask.dtype)
        
        # Sample with tiling/wrapping
        for y in range(target_height):
            for x in range(target_width):
                # Calculate source coordinates with offset and wrapping
                src_x = (x + offset_x) % img_w
                src_y = (y + offset_y) % img_h
                
                sampled_image[y, x] = image[src_y, src_x]
                sampled_mask[y, x] = mask[src_y, src_x]
        
        return sampled_image, sampled_mask

    def composite_layers(self, background, layer1, mask1, layer2, mask2):
        """
        Composite layers using alpha blending
        
        Args:
            background: numpy array (H, W, 3)
            layer1: numpy array (H, W, 3)  
            mask1: numpy array (H, W)
            layer2: numpy array (H, W, 3)
            mask2: numpy array (H, W)
        """
        # Start with background
        result = background.copy()
        
        # Composite layer 1
        alpha1 = np.expand_dims(mask1, axis=-1)
        result = alpha1 * layer1 + (1 - alpha1) * result
        
        # Composite layer 2 on top
        alpha2 = np.expand_dims(mask2, axis=-1)
        result = alpha2 * layer2 + (1 - alpha2) * result
        
        return result

    def create_parallax_animation(self, background_image, image_1, mask_1, image_2, mask_2,
                                 fps, max_frames, height, width,
                                 background_speed, background_direction,
                                 image_1_speed, image_1_direction,
                                 image_2_speed, image_2_direction):
        """
        Create parallax scrolling animation
        """
        # Convert inputs to numpy arrays
        bg_np = background_image.cpu().numpy()
        img1_np = image_1.cpu().numpy()  
        mask1_np = mask_1.cpu().numpy()
        img2_np = image_2.cpu().numpy()
        mask2_np = mask_2.cpu().numpy()
        
        # Validate inputs
        if len(bg_np.shape) != 4 or bg_np.shape[-1] != 3:
            raise ValueError("Background image must be in BHWC format with 3 channels")
        if len(img1_np.shape) != 4 or img1_np.shape[-1] != 3:
            raise ValueError("Image 1 must be in BHWC format with 3 channels")
        if len(img2_np.shape) != 4 or img2_np.shape[-1] != 3:
            raise ValueError("Image 2 must be in BHWC format with 3 channels")
        
        # Take first frame from each input (assuming single images)
        bg_frame = bg_np[0]
        img1_frame = img1_np[0]
        mask1_frame = mask1_np[0] if len(mask1_np.shape) == 3 else mask1_np[0]
        img2_frame = img2_np[0] 
        mask2_frame = mask2_np[0] if len(mask2_np.shape) == 3 else mask2_np[0]
        
        # Create output batch
        output_frames = []
        
        for frame_idx in range(max_frames):
            # Calculate offsets for each layer
            bg_offset_x, bg_offset_y = self.calculate_offset(
                frame_idx, background_speed, background_direction)
            
            img1_offset_x, img1_offset_y = self.calculate_offset(
                frame_idx, image_1_speed, image_1_direction)
            
            img2_offset_x, img2_offset_y = self.calculate_offset(
                frame_idx, image_2_speed, image_2_direction)
            
            # Sample each layer at calculated offsets
            bg_sampled, _ = self.sample_layer(
                bg_frame, np.ones_like(bg_frame[:, :, 0]), 
                bg_offset_x, bg_offset_y, height, width)
            
            img1_sampled, mask1_sampled = self.sample_layer(
                img1_frame, mask1_frame,
                img1_offset_x, img1_offset_y, height, width)
            
            img2_sampled, mask2_sampled = self.sample_layer(
                img2_frame, mask2_frame,
                img2_offset_x, img2_offset_y, height, width)
            
            # Composite all layers
            composite_frame = self.composite_layers(
                bg_sampled, img1_sampled, mask1_sampled,
                img2_sampled, mask2_sampled)
            
            output_frames.append(composite_frame)
        
        # Convert to torch tensor
        output_batch = np.array(output_frames)
        output_tensor = torch.from_numpy(output_batch).to(background_image.device)
        
        return (output_tensor,)

NODE_CLASS_MAPPINGS = {
    "DJZ_ParallaxV1": DJZ_ParallaxV1
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DJZ_ParallaxV1": "DJZ Parallax V1"
}