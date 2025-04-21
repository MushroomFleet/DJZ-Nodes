"""
@author: VideoText
A ComfyUI node that adds customizable text overlays to images
"""

import numpy as np
import torch
from PIL import Image, ImageDraw, ImageFont
import os
import re

class VideoText:
    """A ComfyUI node that adds customizable text overlays to images"""
    
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
                "text": ("STRING", {"default": "VIDEO TEXT"}),
                "font": (font_list,),
                "position": (["top-left", "top-center", "top-right", 
                              "center-left", "center", "center-right", 
                              "bottom-left", "bottom-center", "bottom-right"], 
                              {"default": "bottom-center"}),
                "x_offset": ("INT", {"default": 0, "min": -1000, "max": 1000}),
                "y_offset": ("INT", {"default": 0, "min": -1000, "max": 1000}),
                "padding": ("INT", {"default": 20, "min": 0, "max": 500}),
                "font_size": ("INT", {"default": 32, "min": 8, "max": 256}),
                "line_spacing": ("INT", {"default": 0, "min": -20, "max": 100}),
                "letter_spacing": ("INT", {"default": 0, "min": -10, "max": 50}),
                "text_color": ("STRING", {"default": "#00FF00"}),  # HEX color code
                "glow_radius": ("INT", {"default": 3, "min": 0, "max": 20}),
                "glow_intensity": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.1}),
                "outline_width": ("INT", {"default": 0, "min": 0, "max": 10}),
                "outline_color": ("STRING", {"default": "#000000"}),  # HEX color code
                "chromatic_aberration": ("INT", {"default": 2, "min": 0, "max": 10}),
                "text_alignment": (["left", "center", "right"], {"default": "center"}),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "add_text"
    CATEGORY = "image/text"

    def hex_to_rgb(self, hex_color):
        """Convert hex color code to RGB tuple"""
        # Remove '#' if present
        hex_color = hex_color.lstrip('#')
        
        # Check if valid hex code
        if not re.match(r'^[0-9A-Fa-f]{6}$', hex_color):
            print(f"Warning: Invalid hex color '{hex_color}', defaulting to white")
            return (255, 255, 255)
            
        # Convert to RGB
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

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

    def add_text_with_effects(self, image, text, font_name, position, 
                            x_offset, y_offset, padding, font_size, 
                            text_color_hex, glow_radius, glow_intensity, 
                            outline_width, outline_color_hex, chromatic_aberration,
                            text_alignment, line_spacing, letter_spacing):
        """Add text with effects to the image"""
        # Convert to RGBA for compositing
        image = image.convert('RGBA')
        text_layer = Image.new('RGBA', image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(text_layer)
        
        # Convert hex colors to RGB
        text_color = self.hex_to_rgb(text_color_hex)
        outline_color = self.hex_to_rgb(outline_color_hex)
        
        # Load font with specified size
        font = self.load_font(font_name, font_size)
        
        # Split text into lines
        lines = text.split('\n')
        
        # Apply letter spacing if needed
        if letter_spacing != 0:
            spaced_lines = []
            for line in lines:
                if letter_spacing > 0:
                    spaced_line = " ".join(line)
                    # Adjust the spacing by inserting spaces
                    for _ in range(letter_spacing - 1):
                        spaced_line = " ".join(list(spaced_line))
                    spaced_lines.append(spaced_line)
                else:
                    # Negative spacing - we need to render each character separately
                    # This is handled during drawing
                    spaced_lines.append(line)
            lines = spaced_lines
        
        # Calculate total text height including line spacing
        total_height = 0
        line_heights = []
        line_widths = []
        
        for line in lines:
            text_bbox = draw.textbbox((0, 0), line, font=font)
            line_width = text_bbox[2] - text_bbox[0]
            line_height = text_bbox[3] - text_bbox[1]
            line_heights.append(line_height)
            line_widths.append(line_width)
            total_height += line_height
        
        # Add line spacing to total height
        if len(lines) > 1:
            total_height += line_spacing * (len(lines) - 1)
        
        # Calculate max width
        max_width = max(line_widths) if line_widths else 0
        
        # Parse position and calculate base coordinates
        position_parts = position.split('-')
        vertical = position_parts[0] if len(position_parts) > 0 else "center"
        horizontal = position_parts[1] if len(position_parts) > 1 else "center"
        
        # Calculate base position
        if horizontal == 'left':
            base_x = padding
        elif horizontal == 'center':
            base_x = (image.width - max_width) // 2
        else:  # right
            base_x = image.width - max_width - padding
            
        if vertical == 'top':
            base_y = padding
        elif vertical == 'center':
            base_y = (image.height - total_height) // 2
        else:  # bottom
            base_y = image.height - total_height - padding
        
        # Apply offset
        base_x += x_offset
        base_y += y_offset
        
        # Current y position for drawing
        current_y = base_y
        
        # Draw each line
        for i, line in enumerate(lines):
            # Calculate x position based on alignment
            if text_alignment == 'left':
                text_x = base_x
            elif text_alignment == 'center':
                text_x = base_x + (max_width - line_widths[i]) // 2
            else:  # right
                text_x = base_x + max_width - line_widths[i]
                
            text_position = (text_x, current_y)
            
            # Add outline if specified
            if outline_width > 0:
                for dx in range(-outline_width, outline_width + 1):
                    for dy in range(-outline_width, outline_width + 1):
                        # Skip if dx and dy are both 0 (that would be the main text)
                        if dx == 0 and dy == 0:
                            continue
                        # Calculate size of outline (thicker at corners, thinner at edges)
                        dist = max(abs(dx), abs(dy))
                        if dist > outline_width:
                            continue
                        outline_alpha = int(255 * (1 - (dist / (outline_width + 1))))
                        outline_pos = (text_position[0] + dx, text_position[1] + dy)
                        draw.text(outline_pos, line, font=font, fill=(*outline_color, outline_alpha))
            
            # Add glow effect
            if glow_radius > 0 and glow_intensity > 0:
                glow_alpha = int(255 * glow_intensity)
                for offset_x in range(-glow_radius, glow_radius + 1):
                    for offset_y in range(-glow_radius, glow_radius + 1):
                        if offset_x == 0 and offset_y == 0:
                            continue
                        # Calculate distance for glow falloff
                        distance = (offset_x**2 + offset_y**2) ** 0.5
                        if distance > glow_radius:
                            continue
                        # Glow intensity decreases with distance
                        intensity = 1 - (distance / glow_radius)
                        alpha = int(glow_alpha * intensity)
                        pos = (text_position[0] + offset_x, text_position[1] + offset_y)
                        draw.text(pos, line, font=font, fill=(*text_color, alpha))
            
            # Add chromatic aberration
            if chromatic_aberration > 0:
                # Red channel offset
                draw.text((text_position[0] + chromatic_aberration, text_position[1]),
                        line, font=font, fill=(255, 0, 0, 200))
                # Blue channel offset
                draw.text((text_position[0] - chromatic_aberration, text_position[1]),
                        line, font=font, fill=(0, 0, 255, 200))
            
            # Main text
            draw.text(text_position, line, font=font, fill=(*text_color, 255))
            
            # Update y position for next line
            current_y += line_heights[i] + line_spacing
        
        return Image.alpha_composite(image, text_layer)

    def add_text(self, images, text, font, position, x_offset, y_offset, padding,
                font_size, line_spacing, letter_spacing, text_color, glow_radius, 
                glow_intensity, outline_width, outline_color, chromatic_aberration,
                text_alignment):
        """Main processing function for the node"""
        # Convert from tensor format (B,H,W,C) to PIL Image
        batch_size, height, width, channels = images.shape
        processed_tensors = []

        for b in range(batch_size):
            # Convert tensor to PIL Image
            image_np = (images[b].cpu().numpy() * 255).astype(np.uint8)
            image = Image.fromarray(image_np)
            
            # Apply text effects
            image = self.add_text_with_effects(
                image, text, font, position, x_offset, y_offset, padding, 
                font_size, text_color, glow_radius, glow_intensity, 
                outline_width, outline_color, chromatic_aberration,
                text_alignment, line_spacing, letter_spacing
            )
            
            # Convert back to tensor format
            image_np = np.array(image.convert('RGB')).astype(np.float32) / 255.0
            processed_tensors.append(torch.from_numpy(image_np))

        # Stack tensors back into batch
        result = torch.stack(processed_tensors)
        return (result,)

# Node registration for ComfyUI
NODE_CLASS_MAPPINGS = {
    "VideoText": VideoText
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VideoText": "Video Text"
}