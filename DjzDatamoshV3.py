import torch
import numpy as np
import subprocess
import os
import tempfile
from PIL import Image
import io

class DjzDatamoshV3:
    def __init__(self):
        self.type = "DjzDatamoshV3"
        self.output_node = True
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "mode": (["iframe_removal", "delta_repeat"],),
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
                }),
                "delta_frames": ("INT", {
                    "default": 5,
                    "min": 1,
                    "max": 30,
                    "step": 1
                })
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "datamosh"
    CATEGORY = "image/effects"

    def batch_to_initial_avi(self, images, temp_dir):
        """Convert image batch to initial AVI format"""
        # First save frames as PNG
        frame_pattern = os.path.join(temp_dir, 'frame_%04d.png')
        for i in range(len(images)):
            img_np = (images[i].cpu().numpy() * 255).astype(np.uint8)
            Image.fromarray(img_np).save(frame_pattern % i)
            
        # Convert to AVI using exact ffmpeg command from mosh.py
        input_avi = os.path.join(temp_dir, 'input.avi')
        subprocess.call(
            f'ffmpeg -loglevel error -y -i "{frame_pattern}" '
            f'-crf 0 -pix_fmt yuv420p -bf 0 -b 10000k -r 30 "{input_avi}"',
            shell=True
        )
        
        # Clean up PNGs
        for i in range(len(images)):
            os.remove(frame_pattern % i)
            
        return input_avi

    def apply_datamosh(self, input_avi, output_avi, mode, start_frame, end_frame, delta_frames):
        """Apply datamoshing effect following mosh.py logic exactly"""
        # Read input AVI
        with open(input_avi, 'rb') as in_file:
            in_file_bytes = in_file.read()

        # Split into frames exactly as mosh.py does
        frame_start = bytes.fromhex('30306463')
        frames = in_file_bytes.split(frame_start)
        
        # Open output file
        with open(output_avi, 'wb') as out_file:
            # Write header as mosh.py does
            out_file.write(frames[0])
            frames = frames[1:]  # Remove header from frames
            
            # Frame type markers
            iframe = bytes.fromhex('0001B0')
            pframe = bytes.fromhex('0001B6')
            
            # Count actual video frames
            n_video_frames = len([frame for frame in frames if frame[5:8] == iframe or frame[5:8] == pframe])
            if end_frame < 0:
                end_frame = n_video_frames
                
            print(f"Total frames: {len(frames)}")
            print(f"Video frames: {n_video_frames}")
            
            # Write frames based on mode
            if mode == "iframe_removal":
                frames_written = 0
                for index, frame in enumerate(frames):
                    if index < start_frame or end_frame < index or frame[5:8] != iframe:
                        out_file.write(frame_start + frame)
                        frames_written += 1
                print(f"Frames written: {frames_written}")
                
            else:  # delta_repeat mode
                # Check if we have enough frames
                if delta_frames > end_frame - start_frame:
                    print('Not enough frames to repeat')
                    return

                repeat_frames = []
                repeat_index = 0
                frames_written = 0
                
                for index, frame in enumerate(frames):
                    # Handle non-video frames as mosh.py does
                    if (frame[5:8] != iframe and frame[5:8] != pframe) or not start_frame <= index < end_frame:
                        out_file.write(frame_start + frame)
                        frames_written += 1
                        continue

                    if len(repeat_frames) < delta_frames and frame[5:8] != iframe:
                        # Collect initial frames to repeat
                        repeat_frames.append(frame)
                        out_file.write(frame_start + frame)
                        frames_written += 1
                    elif len(repeat_frames) == delta_frames:
                        out_file.write(frame_start + repeat_frames[repeat_index])
                        repeat_index = (repeat_index + 1) % delta_frames
                        frames_written += 1
                    else:
                        # Handle i-frames as mosh.py does
                        out_file.write(frame_start + frame)
                        frames_written += 1
                        
                print(f"Frames written: {frames_written}")

    def final_conversion(self, output_avi, temp_dir):
        """Convert moshed AVI back to frames"""
        # First convert to MP4 using exact ffmpeg command from mosh.py
        output_mp4 = os.path.join(temp_dir, 'output.mp4')
        subprocess.call(
            f'ffmpeg -loglevel error -y -i "{output_avi}" '
            f'-crf 18 -pix_fmt yuv420p -vcodec libx264 -acodec aac -b 10000k -r 30 "{output_mp4}"',
            shell=True
        )
        
        # Extract frames
        frames_pattern = os.path.join(temp_dir, 'moshed_%04d.png')
        subprocess.call(
            f'ffmpeg -y -i "{output_mp4}" "{frames_pattern}"',
            shell=True
        )
        
        # Load frames back into tensors
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

    def datamosh(self, images, mode, start_frame, end_frame, delta_frames):
        print(f"Starting DjzDatamoshV3 in {mode} mode")
        print(f"Input batch shape: {images.shape}")
        
        if len(images.shape) != 4 or images.shape[0] < 2:
            print("Warning: DjzDatamoshV3 requires at least 2 input images")
            return (images,)

        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                # Convert to initial AVI
                input_avi = self.batch_to_initial_avi(images, temp_dir)
                output_avi = os.path.join(temp_dir, 'output.avi')
                
                # Apply datamoshing
                self.apply_datamosh(
                    input_avi=input_avi,
                    output_avi=output_avi,
                    mode=mode,
                    start_frame=start_frame,
                    end_frame=end_frame,
                    delta_frames=delta_frames
                )
                
                # Convert back to frames
                result = self.final_conversion(output_avi, temp_dir)
                
                if result is None:
                    print("Error: Failed to process video")
                    return (images,)
                    
                print(f"Processing complete. Output shape: {result.shape}")
                return (result,)
                
            except Exception as e:
                print(f"Error during processing: {str(e)}")
                return (images,)

# Register the node with ComfyUI
NODE_CLASS_MAPPINGS = {
    "DjzDatamoshV3": DjzDatamoshV3
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DjzDatamoshV3": "Djz Datamosh V3"
}