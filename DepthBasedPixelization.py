import numpy as np
import torch
import cv2

class DepthBasedPixelization:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),  # Batch of images input
                "depth_maps": ("IMAGE",),  # Batch of depth maps
                "min_block_size": ("INT", {
                    "default": 4,
                    "min": 1,
                    "max": 32,
                    "step": 1,
                }),
                "max_block_size": ("INT", {
                    "default": 32,
                    "min": 1,
                    "max": 64,
                    "step": 1,
                }),
                "depth_influence": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 2.0,
                    "step": 0.1,
                }),
                "invert_depth": ("BOOLEAN", {
                    "default": True,
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_depth_pixelization"
    CATEGORY = "image/effects"

    def normalize_depth_map(self, depth_map):
        """
        Normalize depth map to range [0, 1].
        """
        depth_min = torch.min(depth_map)
        depth_max = torch.max(depth_map)
        if depth_max - depth_min == 0:
            return torch.zeros_like(depth_map)
        return (depth_map - depth_min) / (depth_max - depth_min)

    def preprocess_depth_map(self, depth_map, target_shape):
        """
        Preprocess depth map to match target shape.
        """
        # Convert to grayscale if needed
        if depth_map.shape[-1] > 1:
            depth_map = torch.mean(depth_map, dim=-1, keepdim=True)
        
        # Ensure correct dimensions
        if depth_map.shape[1:3] != target_shape:
            # Resize depth map using interpolation
            depth_np = depth_map.cpu().numpy()
            resized_depth = np.zeros((depth_map.shape[0], target_shape[0], target_shape[1], 1))
            
            for i in range(depth_map.shape[0]):
                resized_depth[i, ..., 0] = cv2.resize(
                    depth_np[i, ..., 0],
                    (target_shape[1], target_shape[0]),
                    interpolation=cv2.INTER_LINEAR
                )
            
            depth_map = torch.from_numpy(resized_depth).to(depth_map.device)
        
        return depth_map

    def get_block_size_map(self, depth_map, min_block_size, max_block_size, invert_depth, depth_influence):
        """
        Convert normalized depth values to block sizes.
        """
        # Normalize depth map
        norm_depth = self.normalize_depth_map(depth_map)
        
        if invert_depth:
            norm_depth = 1 - norm_depth

        # Apply depth influence
        norm_depth = torch.pow(norm_depth, depth_influence)
        
        # Scale to block size range
        size_range = max_block_size - min_block_size
        block_sizes = (norm_depth * size_range + min_block_size).int()
        
        return block_sizes

    def pixelize_block(self, image, x, y, block_size):
        """
        Pixelize a single block in the image.
        """
        # Ensure block size is valid
        block_size = max(1, int(block_size))
        
        # Get block region with bounds checking
        y_end = min(y + block_size, image.shape[0])
        x_end = min(x + block_size, image.shape[1])
        
        if y_end <= y or x_end <= x:
            return
        
        block = image[y:y_end, x:x_end]
        
        # Calculate mean color for the block
        mean_color = torch.mean(block, dim=(0, 1))
        
        # Fill block with mean color
        image[y:y_end, x:x_end] = mean_color

    def process_single_image(self, image, depth_map, min_block_size, max_block_size, invert_depth, depth_influence):
        """
        Process a single image-depth pair.
        """
        # Get block sizes from depth map
        block_sizes = self.get_block_size_map(
            depth_map,
            min_block_size,
            max_block_size,
            invert_depth,
            depth_influence
        )
        
        # Create output image
        result = image.clone()
        height, width = image.shape[:2]
        
        # Process each block
        for y in range(0, height, min_block_size):
            for x in range(0, width, min_block_size):
                # Get block size for this position
                block_size = min(
                    int(block_sizes[y, x].item()),
                    height - y,
                    width - x
                )
                self.pixelize_block(result, x, y, block_size)
        
        return result

    def apply_depth_pixelization(self, images, depth_maps, min_block_size, max_block_size, depth_influence, invert_depth):
        """
        Apply depth-based pixelization to a batch of images.
        """
        # Print debug information
        print(f"Image shape: {images.shape}")
        print(f"Depth map shape: {depth_maps.shape}")
        
        # Preprocess depth maps to match image dimensions
        target_shape = images.shape[1:3]  # (H, W)
        depth_maps = self.preprocess_depth_map(depth_maps, target_shape)
        
        print(f"Preprocessed depth map shape: {depth_maps.shape}")
        
        # Process batch
        batch_size = images.shape[0]
        processed_batch = torch.zeros_like(images)
        
        for i in range(batch_size):
            # Process each image in the batch
            processed_batch[i] = self.process_single_image(
                images[i],
                depth_maps[i, ..., 0],  # Use first channel of depth map
                min_block_size,
                max_block_size,
                invert_depth,
                depth_influence
            )
        
        return (processed_batch,)

NODE_CLASS_MAPPINGS = {
    "DepthBasedPixelization": DepthBasedPixelization
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DepthBasedPixelization": "Depth-Based Pixelization"
}