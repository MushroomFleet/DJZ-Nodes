import torch
import numpy as np

class BatchRangeInsert:
    def __init__(self):
        self.type = "BatchRangeInsert"
        self.output_node = True
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "target_sequence": ("IMAGE",),  # The main sequence to modify
                "insert_frames": ("IMAGE",),    # The frames to insert
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
    FUNCTION = "insert_range"
    CATEGORY = "image/batch"
    
    def insert_range(self, target_sequence, insert_frames, start_frame, end_frame):
        # Check if we have batches of images
        if len(target_sequence.shape) < 4 or target_sequence.shape[0] <= 1:
            print("Warning: BatchRangeInsert node requires a batch of multiple images for target sequence")
            return (target_sequence,)
            
        if len(insert_frames.shape) < 4:
            print("Warning: BatchRangeInsert node requires a batch of images for insert frames")
            return (target_sequence,)
            
        # Get batch sizes and frame dimensions
        target_size = target_sequence.shape[0]
        insert_size = insert_frames.shape[0]
        frame_height = target_sequence.shape[1]
        frame_width = target_sequence.shape[2]
        channels = target_sequence.shape[3]
        
        # Validate and adjust frame indices
        start_frame = min(max(0, start_frame), target_size)
        end_frame = min(max(start_frame, end_frame), target_size)
        
        # Calculate range size
        range_size = end_frame - start_frame
        
        # Calculate new sequence length
        # Original length - range being replaced + number of frames being inserted
        new_size = target_size - range_size + insert_size
        
        # Create a new tensor for the expanded sequence
        result_sequence = torch.zeros((new_size, frame_height, frame_width, channels), 
                                   dtype=target_sequence.dtype,
                                   device=target_sequence.device)
        
        # Copy frames before the insertion point
        if start_frame > 0:
            result_sequence[:start_frame] = target_sequence[:start_frame]
            
        # Insert the new frames
        result_sequence[start_frame:start_frame + insert_size] = insert_frames
        
        # Copy remaining frames after the insertion
        if end_frame < target_size:
            result_sequence[start_frame + insert_size:] = target_sequence[end_frame:]
            
        print(f"Inserted {insert_size} frames at position {start_frame}, new sequence length: {new_size}")
            
        return (result_sequence,)

# This is required for ComfyUI to recognize and load the node
NODE_CLASS_MAPPINGS = {
    "BatchRangeInsert": BatchRangeInsert
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BatchRangeInsert": "Batch Range Insert"
}