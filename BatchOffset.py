import torch
import numpy as np

class BatchOffset:
    def __init__(self):
        self.type = "BatchOffset"
        self.output_node = True
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "offset": ("INT", {
                    "default": -1,
                    "min": -100,  # Arbitrary limit, can be adjusted
                    "max": 100,   # Arbitrary limit, can be adjusted
                    "step": 1
                })
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "offset_batch"
    CATEGORY = "image/batch"
    
    def offset_batch(self, images, offset):
        # Check if we have a batch of images
        if len(images.shape) < 4 or images.shape[0] <= 1:
            print("Warning: BatchOffset node requires a batch of multiple images")
            return (images,)
            
        # Calculate the effective offset (handling negative numbers)
        batch_size = images.shape[0]
        effective_offset = offset % batch_size
        
        # Perform the offset operation
        # For offset -1, this will move each image one position forward
        # and wrap the first image to the end
        shifted_images = torch.roll(images, shifts=effective_offset, dims=0)
        
        return (shifted_images,)

# This is required for ComfyUI to recognize and load the node
NODE_CLASS_MAPPINGS = {
    "BatchOffset": BatchOffset
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BatchOffset": "Batch Offset"
}