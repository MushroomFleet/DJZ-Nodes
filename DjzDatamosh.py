import torch
import numpy as np

class DJZDatamosh:
    def __init__(self):
        self.type = "DJZDatamosh"
        self.output_node = True
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "block_size": ("INT", {
                    "default": 16,
                    "min": 4,
                    "max": 64,
                    "step": 4
                }),
                "max_shift": ("INT", {
                    "default": 8,
                    "min": 1,
                    "max": 32,
                    "step": 1
                }),
                "shift_range": ("INT", {
                    "default": 2,
                    "min": 1,
                    "max": 4,
                    "step": 1,
                    "description": "Higher values = faster but less accurate"
                })
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "datamosh_glide"
    CATEGORY = "image/effects"

    def find_shifts_fast(self, prev_frame, curr_frame, block_size, max_shift, shift_range):
        """Fast version of shift finding"""
        # Convert to expected format and scale to byte range
        prev_frame = (prev_frame.permute(0, 3, 1, 2) * 255).byte()
        curr_frame = (curr_frame.permute(0, 3, 1, 2) * 255).byte()
        
        _, channels, height, width = prev_frame.shape
        h_blocks = height // block_size
        w_blocks = width // block_size
        
        # Initialize output shift tensor
        best_shifts = torch.zeros((h_blocks, w_blocks, 2), device=prev_frame.device)
        
        # Create step size for faster search
        step = shift_range
        shift_values = list(range(-max_shift, max_shift + 1, step))
        
        for h in range(h_blocks):
            for w in range(w_blocks):
                y = h * block_size
                x = w * block_size
                
                # Get current block dimensions
                block_height = min(block_size, height - y)
                block_width = min(block_size, width - x)
                
                # Extract current block
                curr_block = curr_frame[0, :, y:y+block_height, x:x+block_width]
                
                min_diff = float('inf')
                best_dx = 0
                best_dy = 0
                
                # Search for best match
                for dy in shift_values:
                    for dx in shift_values:
                        # Calculate wrapped coordinates
                        py = (y + dy) % height
                        px = (x + dx) % width
                        
                        # Get comparison block
                        prev_block = prev_frame[0, :, 
                                              py:py+block_height,
                                              px:px+block_width]
                        
                        if prev_block.shape == curr_block.shape:
                            diff = torch.abs(prev_block - curr_block).sum().item()
                            if diff < min_diff:
                                min_diff = diff
                                best_dx = dx
                                best_dy = dy
                
                best_shifts[h, w, 0] = best_dx
                best_shifts[h, w, 1] = best_dy
        
        return best_shifts

    def apply_shifts(self, frame, shifts, block_size):
        """Apply computed motion vectors"""
        # Convert to processing format
        frame = frame.permute(0, 3, 1, 2)
        
        # Get dimensions
        batch, channels, height, width = frame.shape
        h_blocks = height // block_size
        w_blocks = width // block_size
        
        # Create output tensor
        output = frame.clone()
        
        # Apply shifts block by block
        for h in range(h_blocks):
            for w in range(w_blocks):
                y_start = h * block_size
                x_start = w * block_size
                
                # Calculate block size (handle edge cases)
                block_height = min(block_size, height - y_start)
                block_width = min(block_size, width - x_start)
                
                # Get shift values
                dx = int(shifts[h, w, 0].item())
                dy = int(shifts[h, w, 1].item())
                
                # Calculate source coordinates with wrapping
                src_y = int((y_start + dy) % height)
                src_x = int((x_start + dx) % width)
                
                # Apply shift
                output[0, :, y_start:y_start+block_height, x_start:x_start+block_width] = \
                    frame[0, :, src_y:src_y+block_height, src_x:src_x+block_width]
        
        # Convert back to original format
        return output.permute(0, 2, 3, 1)

    def datamosh_glide(self, images, block_size, max_shift, shift_range):
        if len(images.shape) != 4 or images.shape[0] < 2:
            print("Warning: DJZDatamosh requires at least 2 input images")
            return (images,)
        
        output_frames = []
        batch_size = images.shape[0]
        
        print(f"Starting datamosh process with {batch_size} frames")
        print(f"Frame shape: {images.shape}")
        
        # Initialize with first frame
        output_frames.append(images[0])
        current_frame = images[0:1].clone()
        
        # Process remaining frames
        for i in range(1, batch_size):
            print(f"Processing frame {i}/{batch_size-1}")
            
            next_frame = images[i:i+1]
            shifts = self.find_shifts_fast(current_frame, next_frame, block_size, max_shift, shift_range)
            datamoshed = self.apply_shifts(current_frame, shifts, block_size)
            
            # Update and store
            output_frames.append(datamoshed[0])
            current_frame = datamoshed
            
            print(f"Frame {i} complete")
        
        # Combine frames
        result = torch.stack(output_frames)
        print(f"Processing complete. Output shape: {result.shape}")
        
        return (result,)

# Register the node with ComfyUI
NODE_CLASS_MAPPINGS = {
    "DJZDatamosh": DJZDatamosh
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DJZDatamosh": "DJZ Datamosh"
}