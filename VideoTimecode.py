"""
@author: VideoTimecode
A ComfyUI node that adds timecode overlays to image sequences
"""

import numpy as np
import torch
import cv2
from PIL import Image, ImageDraw, ImageFont
import os
from datetime import timedelta

class VideoTimecode:
    """A ComfyUI node that adds timecode overlays to image sequences"""
    
    @classmethod
    def INPUT_TYPES(s):
        # Get list of TTF fonts from the /TTF/ directory
        ttf_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "TTF")
        font_list = ["default"]
        if os.path.exists(ttf_path):
            font_list.extend([f for f in os.listdir(ttf_path) if f.lower().endswith('.ttf')])
        
        return {
            "required": {
                "images": ("IMAGE",),  # Batch of images input
                "fps": ("FLOAT", {
                    "default": 30.0,
                    "min": 1.0,
                    "max": 120.0,
                    "step": 0.1
                }),
                "start_time": ("STRING", {
                    "default": "00:00:00:00",
                    "multiline": False
                }),
                "font": (font_list,),
                "font_size": ("INT", {
                    "default": 32,
                    "min": 8,
                    "max": 256
                }),
                "position": (["top", "bottom"], {
                    "default": "bottom"
                }),
                "text_color": (["white", "black", "red", "green", "blue", "yellow"], {
                    "default": "white"
                }),
                "background_opacity": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.1
                }),
                "reverse_count": ("BOOLEAN", {
                    "default": False
                }),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "add_timecode"
    CATEGORY = "image/overlay"

    # Color presets in RGB format
    COLOR_PRESETS = {
        "white": (255, 255, 255),
        "black": (0, 0, 0),
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        "yellow": (255, 255, 0)
    }

    def load_font(self, font_name, font_size):
        """Load font from TTF folder or use default with proper scaling"""
        if font_name == "default":
            try:
                # Get the default font path
                default_font_path = ImageFont.load_default().path
                if default_font_path:
                    return ImageFont.truetype(default_font_path, font_size)
                else:
                    # Fallback to system fonts
                    system_fonts = [
                        "arial.ttf",
                        "Arial.ttf",
                        "DejaVuSans.ttf",
                        "/System/Library/Fonts/SFNS.ttf",
                        "C:\\Windows\\Fonts\\arial.ttf",
                    ]
                    for font_path in system_fonts:
                        try:
                            return ImageFont.truetype(font_path, font_size)
                        except:
                            continue
                    return ImageFont.load_default()
            except Exception as e:
                print(f"Error loading default font: {str(e)}")
                return ImageFont.load_default()
        
        # Handle TTF fonts from the TTF folder
        ttf_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "TTF", font_name)
        try:
            return ImageFont.truetype(ttf_path, font_size)
        except Exception as e:
            print(f"Error loading font {font_name}: {str(e)}")
            try:
                return ImageFont.truetype("arial.ttf", font_size)
            except:
                print("Warning: Could not load fallback font, using default")
                return ImageFont.load_default()

    def add_timecode_to_frame(self, frame, current_time, fps, font, font_size, position, 
                            text_color, background_opacity):
        """Add timecode overlay to a single frame"""
        # Convert to PIL Image for text handling
        frame_pil = Image.fromarray((frame * 255).astype(np.uint8))
        
        # Create text overlay
        overlay = Image.new('RGBA', frame_pil.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Calculate timecode
        total_frames = int((current_time % 1) * fps)
        time_obj = timedelta(seconds=int(current_time))
        timecode = f"{str(time_obj)}:{total_frames:02d}"
        
        # Get font and calculate text size
        font_obj = self.load_font(font, font_size)
        text_bbox = draw.textbbox((0, 0), timecode, font=font_obj)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        # Calculate position
        if position == "top":
            text_y = 20
        else:  # bottom
            text_y = frame_pil.height - text_height - 20
        text_x = (frame_pil.width - text_width) // 2
        
        # Draw background rectangle
        bg_pad = 10
        bg_color = (0, 0, 0, int(255 * background_opacity))
        draw.rectangle(
            [text_x - bg_pad, text_y - bg_pad,
             text_x + text_width + bg_pad, text_y + text_height + bg_pad],
            fill=bg_color
        )
        
        # Draw text
        color = self.COLOR_PRESETS[text_color]
        draw.text((text_x, text_y), timecode, font=font_obj, fill=(*color, 255))
        
        # Composite the overlay with the original frame
        frame_pil = Image.alpha_composite(frame_pil.convert('RGBA'), overlay)
        
        # Convert back to numpy array
        return np.array(frame_pil.convert('RGB')).astype(np.float32) / 255.0

    def add_timecode(self, images, fps, start_time, font, font_size, position,
                    text_color, background_opacity, reverse_count):
        """Main processing function for the node"""
        batch_size = images.shape[0]
        processed_tensors = []
        
        # Parse start time
        hours, minutes, seconds, frames = map(int, start_time.split(':'))
        start_seconds = hours * 3600 + minutes * 60 + seconds + frames / fps
        
        for i in range(batch_size):
            # Calculate current timecode
            if reverse_count:
                total_seconds = batch_size / fps
                current_time = start_seconds - (i / fps)
                if current_time < 0:
                    current_time = 0
            else:
                current_time = start_seconds + (i / fps)
            
            # Process frame
            frame = images[i].cpu().numpy()
            processed_frame = self.add_timecode_to_frame(
                frame, current_time, fps, font, font_size,
                position, text_color, background_opacity
            )
            
            processed_tensors.append(torch.from_numpy(processed_frame))
        
        # Stack tensors back into batch
        result = torch.stack(processed_tensors)
        return (result,)

# Node registration for ComfyUI
NODE_CLASS_MAPPINGS = {
    "VideoTimecode": VideoTimecode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VideoTimecode": "Video Timecode"
}