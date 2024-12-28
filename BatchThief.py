import torch
import numpy as np

class BatchThief:
    def __init__(self):
        self.type = "BatchThief"
        self.output_node = True
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "start_frame": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 999,  # Arbitrary limit, can be adjusted
                    "step": 1
                }),
                "end_frame": ("INT", {
                    "default": 1,
                    "min": 0,
                    "max": 999,  # Arbitrary limit, can be adjusted
                    "step": 1
                })
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "steal_frames"
    CATEGORY = "image/batch"
    
    def steal_frames(self, images, start_frame, end_frame):
        # Check if we have a batch of images
        if len(images.shape) < 4 or images.shape[0] <= 1:
            print("Warning: BatchThief node requires a batch of multiple images")
            return (images,)
            
        # Get batch size
        batch_size = images.shape[0]
        
        # Validate and adjust frame indices
        start_frame = min(max(0, start_frame), batch_size - 1)
        end_frame = min(max(start_frame, end_frame), batch_size)
        
        # Extract the specified range of frames
        stolen_frames = images[start_frame:end_frame]
        
        # If the range is empty (start_frame >= end_frame), return an empty batch
        if stolen_frames.shape[0] == 0:
            print("Warning: Selected frame range is empty")
            # Return a single empty frame to maintain tensor structure
            return (images[:1],)
            
        return (stolen_frames,)

# This is required for ComfyUI to recognize and load the node
NODE_CLASS_MAPPINGS = {
    "BatchThief": BatchThief
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BatchThief": "Batch Thief"
}