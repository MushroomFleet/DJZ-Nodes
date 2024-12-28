import torch
import numpy as np
import os
import tempfile
from PIL import Image
import subprocess

class DjzDatamoshV5:
    def __init__(self):
        self.type = "DjzDatamoshV5"
        self.output_node = True
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "reverse_sort": ("BOOLEAN", {
                    "default": True,
                    "label": "Reverse Sort"
                }),
                "start_frame": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 999,
                    "step": 1
                }),
                "end_frame": ("INT", {
                    "default": -1,
                    "min": -1,
                    "max": 999,
                    "step": 1
                })
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "datamosh"
    CATEGORY = "image/effects"

    def extract_frame_sizes(self, images, temp_dir):
        """Save frames and get their sizes"""
        frame_sizes = []
        frame_paths = []
        
        for i in range(len(images)):
            frame_path = os.path.join(temp_dir, f'frame_{i:04d}.png')
            img_np = (images[i].cpu().numpy() * 255).astype(np.uint8)
            Image.fromarray(img_np).save(frame_path)
            
            # Get file size
            frame_sizes.append((os.path.getsize(frame_path), i))
            frame_paths.append(frame_path)
            
        return frame_sizes, frame_paths

    def create_sorted_video(self, frame_sizes, frame_paths, temp_dir, reverse_sort, start_frame, end_frame):
        """Create video with frames sorted by size"""
        try:
            if end_frame < 0:
                end_frame = len(frame_sizes)
            
            # Split frames into sections
            pre_frames = list(range(start_frame))
            sort_frames = list(range(start_frame, min(end_frame, len(frame_sizes))))
            post_frames = list(range(end_frame, len(frame_sizes)))
            
            # Sort middle section by frame size
            sorted_section = sorted(
                [(size, idx) for size, idx in frame_sizes if idx in sort_frames],
                reverse=reverse_sort
            )
            sorted_indices = [idx for _, idx in sorted_section]
            
            # Combine all sections
            final_order = pre_frames + sorted_indices + post_frames
            
            # Create new frame sequence
            sorted_frames_dir = os.path.join(temp_dir, 'sorted_frames')
            os.makedirs(sorted_frames_dir, exist_ok=True)
            
            for new_idx, old_idx in enumerate(final_order):
                src_path = frame_paths[old_idx]
                dst_path = os.path.join(sorted_frames_dir, f'frame_{new_idx:04d}.png')
                os.link(src_path, dst_path)  # Hard link to avoid copying
            
            # Convert to video
            output_path = os.path.join(temp_dir, 'output.mp4')
            frames_pattern = os.path.join(sorted_frames_dir, 'frame_%04d.png')
            subprocess.call(
                f'ffmpeg -loglevel error -y -i "{frames_pattern}" '
                f'-crf 18 -pix_fmt yuv420p -vcodec libx264 -acodec aac -b 10000k -r 30 "{output_path}"',
                shell=True
            )
            
            return output_path
            
        except Exception as e:
            print(f"Error in frame sorting: {str(e)}")
            return None

    def load_sorted_frames(self, video_path, temp_dir):
        """Load sorted frames back into tensors"""
        frames_pattern = os.path.join(temp_dir, 'final_%04d.png')
        subprocess.call(
            f'ffmpeg -y -i "{video_path}" "{frames_pattern}"',
            shell=True
        )
        
        frames = []
        frame_idx = 1  # ffmpeg starts at 1
        while True:
            frame_path = frames_pattern % frame_idx
            if not os.path.exists(frame_path):
                break
                
            img = Image.open(frame_path)
            frame_np = np.array(img).astype(np.float32) / 255.0
            frames.append(torch.from_numpy(frame_np))
            
            os.remove(frame_path)
            frame_idx += 1
            
        return torch.stack(frames) if frames else None

    def datamosh(self, images, reverse_sort, start_frame, end_frame):
        print(f"Starting DjzDatamoshV5 with reverse_sort={reverse_sort}")
        print(f"Input batch shape: {images.shape}")
        
        if len(images.shape) != 4 or images.shape[0] < 2:
            print("Warning: DjzDatamoshV5 requires at least 2 input images")
            return (images,)

        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                # Extract frame sizes and save frames
                frame_sizes, frame_paths = self.extract_frame_sizes(images, temp_dir)
                
                # Create sorted video
                output_path = self.create_sorted_video(
                    frame_sizes=frame_sizes,
                    frame_paths=frame_paths,
                    temp_dir=temp_dir,
                    reverse_sort=reverse_sort,
                    start_frame=start_frame,
                    end_frame=end_frame
                )
                
                if output_path is None:
                    print("Error: Failed to create sorted video")
                    return (images,)
                
                # Load sorted frames
                result = self.load_sorted_frames(output_path, temp_dir)
                
                if result is None:
                    print("Error: Failed to load sorted frames")
                    return (images,)
                    
                print(f"Processing complete. Output shape: {result.shape}")
                return (result,)
                
            except Exception as e:
                print(f"Error during processing: {str(e)}")
                return (images,)

# Register the node with ComfyUI
NODE_CLASS_MAPPINGS = {
    "DjzDatamoshV5": DjzDatamoshV5
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DjzDatamoshV5": "Djz Datamosh V5 (Size Range)"
}