import os
import glob
import random
import cv2
import torch
import numpy as np

ALLOWED_VIDEO_EXT = ('.mp4', '.avi', '.mov', '.mkv')

class LoadVideoBatchFrame:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mode": (["single_video", "incremental_video", "random"],),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "index": ("INT", {"default": 0, "min": 0, "max": 150000, "step": 1}),
                "frame": ("INT", {"default": 0, "min": 0, "max": 999999, "step": 1}),
                "label": ("STRING", {"default": 'Video Batch 001', "multiline": False}),
                "path": ("STRING", {"default": '', "multiline": False}),
                "pattern": ("STRING", {"default": '*', "multiline": False}),
            },
        }

    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("frame", "filename_text")
    FUNCTION = "load_batch_videos"

    CATEGORY = "image/video"

    def load_batch_videos(self, path, pattern='*', index=0, frame=0, mode="single_video", seed=0, label='Video Batch 001'):
        if not os.path.exists(path):
            raise ValueError(f"Path does not exist: {path}")
            
        fl = self.BatchVideoLoader(path, pattern)
        
        if mode == 'single_video':
            frame_tensor, filename = fl.get_video_frame_by_id(index, frame)
            if frame_tensor is None:
                raise ValueError(f"No valid video frame found for index {index} and frame {frame}")
        elif mode == 'incremental_video':
            frame_tensor, filename = fl.get_next_video_frame(index, frame)
            if frame_tensor is None:
                raise ValueError("No valid video frame found")
        else:
            random.seed(seed)
            newindex = int(random.random() * len(fl.video_paths))
            frame_tensor, filename = fl.get_video_frame_by_id(newindex, frame)
            if frame_tensor is None:
                raise ValueError("No valid video frame found")

        return (frame_tensor, filename)

    class BatchVideoLoader:
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

        def get_video_frame_by_id(self, video_id, frame_number):
            if video_id < 0 or video_id >= len(self.video_paths):
                return None, None
                
            video_path = self.video_paths[video_id]
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                return None, None
                
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            if frame_number >= total_frames:
                frame_number = total_frames - 1
                
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            
            ret, frame = cap.read()
            cap.release()
            
            if not ret:
                return None, None
                
            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Convert to float32 and normalize to 0-1
            frame_float = frame_rgb.astype(np.float32) / 255.0
            # Convert to tensor and rearrange dimensions to [batch, height, width, channels]
            frame_tensor = torch.from_numpy(frame_float)[None,]
            
            return (frame_tensor, os.path.basename(video_path))

        def get_next_video_frame(self, index, frame_number):
            if index >= len(self.video_paths):
                index = 0
            return self.get_video_frame_by_id(index, frame_number)