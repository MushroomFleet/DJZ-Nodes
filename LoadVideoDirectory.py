import os
import glob
import random
import cv2
import torch
import numpy as np

ALLOWED_VIDEO_EXT = ('.mp4', '.avi', '.mov', '.mkv')

class LoadVideoDirectory:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mode": (["single_video", "incremental_video", "random"],),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "index": ("INT", {"default": 0, "min": 0, "max": 150000, "step": 1}),
                "skip_frames": ("INT", {"default": 0, "min": 0, "max": 999999, "step": 1}),
                "max_frames": ("INT", {"default": 0, "min": 0, "max": 999999, "step": 1}),
                "label": ("STRING", {"default": 'Video Batch 001', "multiline": False}),
                "path": ("STRING", {"default": '', "multiline": False}),
                "pattern": ("STRING", {"default": '*', "multiline": False}),
            },
        }

    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("frames", "filename_text")
    FUNCTION = "load_video_directory"

    CATEGORY = "image/video"

    def load_video_directory(self, path, pattern='*', index=0, skip_frames=0, max_frames=0, mode="single_video", seed=0, label='Video Batch 001'):
        if not os.path.exists(path):
            raise ValueError(f"Path does not exist: {path}")
            
        vl = self.VideoDirectoryLoader(path, pattern)
        if mode == 'single_video':
            frames_tensor, filename = vl.get_video_frames_by_id(index, skip_frames, max_frames)
            if frames_tensor is None:
                raise ValueError(f"No valid video frames found for index {index}")
        elif mode == 'incremental_video':
            frames_tensor, filename = vl.get_next_video_frames(index, skip_frames, max_frames)
            if frames_tensor is None:
                raise ValueError("No valid video frames found")
        else:  # random mode
            random.seed(seed)
            newindex = int(random.random() * len(vl.video_paths))
            frames_tensor, filename = vl.get_video_frames_by_id(newindex, skip_frames, max_frames)
            if frames_tensor is None:
                raise ValueError("No valid video frames found")

        return (frames_tensor, filename)

    class VideoDirectoryLoader:
        def __init__(self, directory_path, pattern):
            self.video_paths = []
            self.load_videos(directory_path, pattern)
            self.video_paths.sort()
            self.index = 0

        def load_videos(self, directory_path, pattern):
            for file_name in glob.glob(os.path.join(glob.escape(directory_path), pattern), recursive=True):
                if file_name.lower().endswith(ALLOWED_VIDEO_EXT):
                    abs_file_path = os.path.abspath(file_name)
                    self.video_paths.append(abs_file_path)

        def get_video_frames_by_id(self, video_id, skip_frames, max_frames):
            if video_id < 0 or video_id >= len(self.video_paths):
                return None, None
                
            video_path = self.video_paths[video_id]
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                return None, None
                
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # Handle skip_frames
            start_frame = min(skip_frames, total_frames - 1) if skip_frames > 0 else 0
            cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
            
            # Handle max_frames
            remaining_frames = total_frames - start_frame
            frames_to_read = remaining_frames if max_frames == 0 else min(remaining_frames, max_frames)
            
            # Pre-allocate tensor to store all frames
            frames_list = []
            
            for _ in range(frames_to_read):
                ret, frame = cap.read()
                if not ret:
                    break
                    
                # Convert BGR to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Convert to float32 and normalize to 0-1
                frame_float = frame_rgb.astype(np.float32) / 255.0
                # Convert to tensor
                frame_tensor = torch.from_numpy(frame_float)
                frames_list.append(frame_tensor)
            
            cap.release()
            
            if not frames_list:
                return None, None
                
            # Stack all frames into a single tensor [batch, height, width, channels]
            frames_tensor = torch.stack(frames_list, dim=0)
            
            return (frames_tensor, os.path.basename(video_path))

        def get_next_video_frames(self, index, skip_frames, max_frames):
            if index >= len(self.video_paths):
                index = 0
            return self.get_video_frames_by_id(index, skip_frames, max_frames)

# This is required for ComfyUI to recognize and load the node
NODE_CLASS_MAPPINGS = {
    "LoadVideoDirectory": LoadVideoDirectory
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadVideoDirectory": "Load Video Directory"
}