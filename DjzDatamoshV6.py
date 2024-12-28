import torch
import numpy as np
from PIL import Image
from scipy import ndimage

class DjzDatamoshV6:
    def __init__(self):
        self.type = "DjzDatamoshV6"
        self.output_node = True
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "threshold": ("FLOAT", {
                    "default": 128.0,
                    "min": 0.0,
                    "max": 255.0,
                    "step": 1.0
                }),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "pixel_sort"
    CATEGORY = "image/effects"

    def get_luma_values(self, image_data):
        """Calculate luma values for the image using standard coefficients"""
        # Convert to numpy for calculations
        if isinstance(image_data, torch.Tensor):
            image_data = image_data.cpu().numpy()
        
        # RGB to Luma conversion coefficients
        coefficients = np.array([0.2126, 0.7152, 0.0722])
        
        # Calculate luma values (assuming last dimension is RGB)
        luma = np.dot(image_data[..., :3], coefficients)
        return luma

    def get_sobel_coordinates(self, image_data, threshold):
        """Calculate Sobel edge detection coordinates"""
        # Get luma values for edge detection
        luma = self.get_luma_values(image_data)
        
        # Apply Sobel operators
        dx = ndimage.sobel(luma, 0)  # horizontal derivative
        dy = ndimage.sobel(luma, 1)  # vertical derivative
        
        # Calculate magnitude
        magnitude = np.hypot(dx, dy)
        
        # Normalize
        magnitude *= 255.0 / np.max(magnitude)
        
        # Create boolean mask based on threshold
        return magnitude > threshold

    def get_segments(self, sobel_coordinates):
        """Get segments for sorting based on Sobel edges"""
        height, width = sobel_coordinates.shape
        segments = []
        
        for i in range(height):
            current_segment = []
            for j in range(width):
                if not current_segment:
                    current_segment.append((i, j))
                    continue
                    
                # If we hit an edge or column changes, start new segment
                if (sobel_coordinates[i, j] != sobel_coordinates[current_segment[0][0], current_segment[0][1]]):
                    segments.append(current_segment)
                    current_segment = []
                
                current_segment.append((i, j))
                
            if current_segment:
                segments.append(current_segment)
                
        return segments

    def sort_segments(self, image_data, luma, segments):
        """Sort image segments based on luma values"""
        sorted_data = image_data.copy()
        
        for segment in segments:
            if not segment:
                continue
                
            # Get coordinates for current segment
            i_coords, j_coords = zip(*segment)
            
            # Get luma values for segment
            segment_luma = luma[i_coords[0], j_coords]
            
            # Sort segment based on luma values
            sorted_indices = np.argsort(segment_luma)
            
            # Apply sorting to all channels
            for idx, sort_idx in enumerate(sorted_indices):
                sorted_data[i_coords[0], j_coords[idx]] = image_data[i_coords[0], j_coords[sort_idx]]
        
        return sorted_data

    def pixel_sort(self, images, threshold):
        """Main pixel sorting function"""
        print(f"Starting DjzDatamoshV6 pixel sorting")
        print(f"Input batch shape: {images.shape}")
        
        if len(images.shape) != 4:
            print("Warning: DjzDatamoshV6 requires batch of images in BHWC format")
            return (images,)
            
        try:
            # Convert to numpy for processing
            images_np = images.cpu().numpy()
            batch_sorted = []
            
            # Process each image in batch
            for idx in range(len(images_np)):
                image = images_np[idx]
                
                # Get edge detection mask
                sobel_coords = self.get_sobel_coordinates(image, threshold)
                
                # Calculate luma values for sorting
                luma = self.get_luma_values(image)
                
                # Get segments for sorting
                segments = self.get_segments(sobel_coords)
                
                # Sort segments
                sorted_image = self.sort_segments(image, luma, segments)
                
                batch_sorted.append(sorted_image)
            
            # Convert back to torch tensor
            result = torch.from_numpy(np.stack(batch_sorted))
            
            print(f"Processing complete. Output shape: {result.shape}")
            return (result,)
            
        except Exception as e:
            print(f"Error during processing: {str(e)}")
            return (images,)

# Register the node with ComfyUI
NODE_CLASS_MAPPINGS = {
    "DjzDatamoshV6": DjzDatamoshV6
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DjzDatamoshV6": "Djz Datamosh V6 (Pixel Sorting)"
}