import torch
import numpy as np

class BatchRangeSwap:
    def __init__(self):
        self.type = "BatchRangeSwap"
        self.output_node = True
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "target_sequence": ("IMAGE",),  # The main sequence to modify
                "swap_frames": ("IMAGE",),      # The frames to swap in
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
    FUNCTION = "swap_range"
    CATEGORY = "image/batch"
    
    def swap_range(self, target_sequence, swap_frames, start_frame, end_frame):
        # Check if we have batches of images
        if len(target_sequence.shape) < 4 or target_sequence.shape[0] <= 1:
            print("Warning: BatchRangeSwap node requires a batch of multiple images for target sequence")
            return (target_sequence,)
            
        if len(swap_frames.shape) < 4:
            print("Warning: BatchRangeSwap node requires a batch of images for swap frames")
            return (target_sequence,)
            
        # Get batch sizes
        target_size = target_sequence.shape[0]
        swap_size = swap_frames.shape[0]
        
        # Validate and adjust frame indices
        start_frame = min(max(0, start_frame), target_size - 1)
        end_frame = min(max(start_frame, end_frame), target_size)
        
        # Calculate range size
        range_size = end_frame - start_frame
        
        # Create a copy of the target sequence to modify
        result_sequence = target_sequence.clone()
        
        # If the range is empty, return original sequence
        if range_size == 0:
            print("Warning: Selected frame range is empty")
            return (result_sequence,)
            
        # Calculate how many frames we can actually swap
        # Limited by both range size and available swap frames
        frames_to_swap = min(range_size, swap_size)
        
        # Perform the swap
        result_sequence[start_frame:start_frame + frames_to_swap] = swap_frames[:frames_to_swap]
        
        # Print warning if we couldn't swap all frames in range due to insufficient swap frames
        if frames_to_swap < range_size:
            print(f"Warning: Only {frames_to_swap} frames were swapped (insufficient swap frames for entire range)")
            
        return (result_sequence,)

# This is required for ComfyUI to recognize and load the node
NODE_CLASS_MAPPINGS = {
    "BatchRangeSwap": BatchRangeSwap
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BatchRangeSwap": "Batch Range Swap"
}