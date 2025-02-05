"""
@author: RetroVideoText
A ComfyUI node that adds retro-style text overlays to images
"""

import numpy as np
import torch
from PIL import Image, ImageDraw, ImageFont
import os

class RetroVideoText:
    """A ComfyUI node that adds retro-style text effects to images"""
    
    @classmethod
    def INPUT_TYPES(s):
        # Get list of TTF fonts from the /TTF/ directory
        ttf_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "TTF")
        font_list = ["default"]
        if os.path.exists(ttf_path):
            font_list.extend([f for f in os.listdir(ttf_path) if f.lower().endswith('.ttf')])
        
        return {
            "required": {
                "images": ("IMAGE",),  # ComfyUI image tensor
                "text": ("STRING", {"default": "SYSTEM LOADING..."}),
                "font": (font_list,),
                "position": (["top", "center", "bottom"], {"default": "bottom"}),
                "font_size": ("INT", {"default": 32, "min": 8, "max": 256}),
                "text_color": (["green", "amber", "white", "cyan", "magenta"], {"default": "green"}),
                "glow_radius": ("INT", {"default": 3, "min": 0, "max": 20}),
                "glow_intensity": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.1}),
                "scanline_spacing": ("INT", {"default": 3, "min": 1, "max": 20}),
                "scanline_alpha": ("FLOAT", {"default": 0.3, "min": 0.0, "max": 1.0, "step": 0.1}),
                "chromatic_aberration": ("INT", {"default": 2, "min": 0, "max": 10}),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "add_retro_text"
    CATEGORY = "image/text"

    # Color presets in RGB format
    COLOR_PRESETS = {
        "green": (0, 255, 0),
        "amber": (255, 191, 0),
        "white": (255, 255, 255),
        "cyan": (0, 255, 255),
        "magenta": (255, 0, 255)
    }

    def load_font(self, font_name, font_size):
        """Load font from TTF folder or use default with proper scaling"""
        if font_name == "default":
            # For default font, we need to create a TTF from the default font data
            try:
                # Get the default font path
                default_font_path = ImageFont.load_default().path
                if default_font_path:
                    # If we have a path, load it as TrueType with desired size
                    return ImageFont.truetype(default_font_path, font_size)
                else:
                    # Fallback to a basic system font
                    system_fonts = [
                        "arial.ttf", 
                        "Arial.ttf",
                        "DejaVuSans.ttf",  # Common on Linux
                        "/System/Library/Fonts/SFNS.ttf",  # MacOS
                        "C:\\Windows\\Fonts\\arial.ttf",  # Windows
                    ]
                    for font_path in system_fonts:
                        try:
                            return ImageFont.truetype(font_path, font_size)
                        except:
                            continue
                    # If all else fails, use load_default
                    print("Warning: Could not load scalable font, text size may be limited")
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
            # Fallback to trying to load a system font
            try:
                return ImageFont.truetype("arial.ttf", font_size)
            except:
                print("Warning: Could not load fallback font, using default")
                return ImageFont.load_default()

    def add_scanlines(self, image, spacing, alpha):
        """Add CRT scanline effect to the image"""
        width, height = image.size
        scan_lines = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(scan_lines)
        
        for y in range(0, height, spacing):
            draw.line([(0, y), (width, y)], fill=(0, 0, 0, int(255 * alpha)))
            
        return Image.alpha_composite(image.convert('RGBA'), scan_lines)

    def add_text_effects(self, image, text, font_name, position, font_size, color_name,
                        glow_radius, glow_intensity, chromatic_aberration):
        """Add text with retro effects to the image"""
        # Convert to RGBA for compositing
        image = image.convert('RGBA')
        text_layer = Image.new('RGBA', image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(text_layer)
        
        # Load font with specified size
        font = self.load_font(font_name, font_size)
        
        # Get text size for positioning
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        # Calculate text position
        if position == 'bottom':
            text_position = ((image.width - text_width) // 2,
                           image.height - text_height - 20)
        elif position == 'top':
            text_position = ((image.width - text_width) // 2, 20)
        else:  # center
            text_position = ((image.width - text_width) // 2,
                           (image.height - text_height) // 2)
        
        color = self.COLOR_PRESETS[color_name]
        
        # Add glow effect
        glow_alpha = int(255 * glow_intensity)
        for offset_x in range(-glow_radius, glow_radius + 1):
            for offset_y in range(-glow_radius, glow_radius + 1):
                if offset_x == 0 and offset_y == 0:
                    continue
                pos = (text_position[0] + offset_x, text_position[1] + offset_y)
                draw.text(pos, text, font=font, fill=(*color, glow_alpha))
        
        # Add chromatic aberration
        if chromatic_aberration > 0:
            # Red channel offset
            draw.text((text_position[0] + chromatic_aberration, text_position[1]),
                     text, font=font, fill=(255, 0, 0, 200))
            # Blue channel offset
            draw.text((text_position[0] - chromatic_aberration, text_position[1]),
                     text, font=font, fill=(0, 0, 255, 200))
        
        # Main text
        draw.text(text_position, text, font=font, fill=(*color, 255))
        
        return Image.alpha_composite(image, text_layer)

    def add_retro_text(self, images, text, font, position, font_size, text_color,
                      glow_radius, glow_intensity, scanline_spacing, 
                      scanline_alpha, chromatic_aberration):
        """Main processing function for the node"""
        # Convert from tensor format (B,H,W,C) to PIL Image
        batch_size, height, width, channels = images.shape
        processed_tensors = []

        for b in range(batch_size):
            # Convert tensor to PIL Image
            image_np = (images[b].cpu().numpy() * 255).astype(np.uint8)
            image = Image.fromarray(image_np)
            
            # Apply text effects
            image = self.add_text_effects(
                image, text, font, position, font_size, text_color,
                glow_radius, glow_intensity, chromatic_aberration
            )
            
            # Add scanlines
            if scanline_spacing > 0 and scanline_alpha > 0:
                image = self.add_scanlines(image, scanline_spacing, scanline_alpha)
            
            # Convert back to tensor format
            image_np = np.array(image.convert('RGB')).astype(np.float32) / 255.0
            processed_tensors.append(torch.from_numpy(image_np))

        # Stack tensors back into batch
        result = torch.stack(processed_tensors)
        return (result,)

# Node registration for ComfyUI
NODE_CLASS_MAPPINGS = {
    "RetroVideoText": RetroVideoText
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RetroVideoText": "Retro Video Text"
}