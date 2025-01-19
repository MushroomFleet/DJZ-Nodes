import numpy as np
import torch
import cv2
from PIL import Image

class VideoRingPainter:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),  # Batch of images input
                "mask": ("MASK",),     # Input mask to be processed
                "stroke_width": ("INT", {
                    "default": 20,
                    "min": 0,
                    "max": 999,
                    "step": 1
                }),
                "stroke_blur": ("INT", {
                    "default": 6,
                    "min": 0,
                    "max": 100,
                    "step": 1
                }),
                "highlight_color": ("STRING", {
                    "default": "#FF0000",
                    "multiline": False
                }),
                "background_color": ("STRING", {
                    "default": "#000000",
                    "multiline": False
                }),
                "highlight_opacity": ("FLOAT", {
                    "default": 0.8,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.1
                }),
            },
        }

    RETURN_TYPES = ("IMAGE", "MASK",)
    RETURN_NAMES = ("preview", "ring_mask",)
    FUNCTION = "process_video_ring"
    CATEGORY = "image/effects"

    def expand_mask(self, mask, expansion, blur):
        """Expand or contract a mask with optional blur"""
        if expansion > 0:
            kernel = np.ones((3, 3), np.uint8)
            mask = cv2.dilate(mask, kernel, iterations=expansion)
        elif expansion < 0:
            kernel = np.ones((3, 3), np.uint8)
            mask = cv2.erode(mask, kernel, iterations=abs(expansion))
        
        if blur > 0:
            mask = cv2.GaussianBlur(mask, (0, 0), blur)
        
        return mask

    def create_ring_mask(self, mask, stroke_width, blur):
        """Create a ring mask from input mask using stroke width"""
        # Convert mask to numpy if it's a tensor
        if isinstance(mask, torch.Tensor):
            mask = mask.cpu().numpy()
        
        if mask.max() <= 1.0:
            mask = (mask * 255).astype(np.uint8)
            
        grow_offset = int(stroke_width / 2)
        inner_stroke = -grow_offset
        outer_stroke = stroke_width - grow_offset
        
        # Create inner and outer masks
        inner_mask = self.expand_mask(mask, inner_stroke, blur)
        outer_mask = self.expand_mask(mask, outer_stroke, blur)
        
        # Create ring by subtracting inner from outer
        ring_mask = np.clip(outer_mask - inner_mask, 0, 255)
        return ring_mask / 255.0

    def hex_to_rgb(self, color_input):
        """Convert color input to RGB values. Handles both hex codes and float RGB values."""
        # If input is a string starting with #, treat as hex
        if isinstance(color_input, str) and color_input.startswith('#'):
            color = color_input.lstrip('#')
            return tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        
        # Otherwise treat as float RGB values
        try:
            # Split the input string by commas if it's a string
            if isinstance(color_input, str):
                rgb_values = [float(x.strip()) for x in color_input.split(',')]
            else:
                rgb_values = [float(color_input)]
            
            # Convert float values (0-1) to RGB (0-255)
            return tuple(int(v * 255) for v in rgb_values[:3])
        except Exception as e:
            print(f"Error parsing color input: {color_input}")
            # Return black as fallback
            return (0, 0, 0)

    def colorize_mask(self, mask, highlight_color, background_color, opacity):
        """Colorize the mask using specified colors"""
        # Convert hex colors to RGB
        highlight_rgb = self.hex_to_rgb(highlight_color)
        background_rgb = self.hex_to_rgb(background_color)
        
        # Create colored image
        h, w = mask.shape
        colored = np.zeros((h, w, 3), dtype=np.float32)
        
        # Apply background color
        for i in range(3):
            colored[:, :, i] = background_rgb[i] / 255.0
        
        # Apply highlight color with mask
        mask_3d = np.stack([mask * opacity] * 3, axis=-1)
        highlight_color_norm = np.array(highlight_rgb) / 255.0
        
        colored = colored * (1 - mask_3d) + highlight_color_norm * mask_3d
        return colored

    def process_video_ring(self, images, mask, stroke_width, stroke_blur, 
                          highlight_color, background_color, highlight_opacity):
        # Convert inputs to appropriate formats
        batch_size = images.shape[0]
        if mask.dim() == 2:
            mask = mask.unsqueeze(0)
        
        # Process each frame
        ring_masks = []
        previews = []
        
        for i in range(batch_size):
            # Create ring mask
            current_mask = mask[min(i, mask.shape[0]-1)]
            ring_mask = self.create_ring_mask(
                current_mask,
                stroke_width,
                stroke_blur
            )
            
            # Colorize the mask for preview
            colored_preview = self.colorize_mask(
                ring_mask,
                highlight_color,
                background_color,
                highlight_opacity
            )
            
            ring_masks.append(torch.from_numpy(ring_mask).float())
            previews.append(torch.from_numpy(colored_preview).float())
        
        # Stack results
        ring_masks = torch.stack(ring_masks)
        previews = torch.stack(previews)
        
        return (previews.to(images.device), ring_masks.to(images.device))

NODE_CLASS_MAPPINGS = {
    "VideoRingPainter": VideoRingPainter
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VideoRingPainter": "Video Ring Painter"
}
