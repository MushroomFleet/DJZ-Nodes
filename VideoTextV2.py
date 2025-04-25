"""
@author: VideoTextV2
A ComfyUI node that adds customizable text overlays to images with rotation and vertical text support
"""

import numpy as np
import torch
from PIL import Image, ImageDraw, ImageFont
import os
import re
import math

class VideoTextV2:
    """A ComfyUI node that adds customizable text overlays to images with rotation and vertical text support"""
    
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
                "text_rotation": ("INT", {"default": 0, "min": -180, "max": 180}),
                "vertical_text": (["disabled", "enabled"], {"default": "disabled"}),
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
                            text_alignment, line_spacing, letter_spacing,
                            text_rotation, vertical_text):
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
        
        # Apply letter spacing if needed and handle vertical text
        is_vertical = vertical_text == "enabled"
        
        if is_vertical:
            # For vertical text, we'll handle each character separately
            processed_lines = []
            for line in lines:
                # For vertical text, we keep the original characters
                processed_lines.append(line)
            lines = processed_lines
        elif letter_spacing != 0:
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
        
        # Calculate text dimensions differently based on vertical or horizontal orientation
        if is_vertical:
            # For vertical text, we need to calculate dimensions differently
            total_height = 0
            max_width = 0
            line_heights = []
            line_widths = []
            
            for line in lines:
                line_height = 0
                line_width = 0
                
                # Calculate height as sum of character heights plus spacing
                for char in line:
                    char_bbox = draw.textbbox((0, 0), char, font=font)
                    char_width = char_bbox[2] - char_bbox[0]
                    char_height = char_bbox[3] - char_bbox[1]
                    line_width = max(line_width, char_width)
                    line_height += char_height + letter_spacing
                
                # Adjust for last letter spacing
                if line and letter_spacing > 0:
                    line_height -= letter_spacing
                
                line_heights.append(line_height)
                line_widths.append(line_width)
                total_height = max(total_height, line_height)
                max_width += line_width + line_spacing
            
            # Adjust for last line spacing
            if lines and line_spacing > 0:
                max_width -= line_spacing
        else:
            # Original horizontal text calculations
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
        vertical_pos = position_parts[0] if len(position_parts) > 0 else "center"
        horizontal_pos = position_parts[1] if len(position_parts) > 1 else "center"
        
        # Calculate base position
        if horizontal_pos == 'left':
            base_x = padding
        elif horizontal_pos == 'center':
            base_x = (image.width - max_width) // 2
        else:  # right
            base_x = image.width - max_width - padding
            
        if vertical_pos == 'top':
            base_y = padding
        elif vertical_pos == 'center':
            base_y = (image.height - total_height) // 2
        else:  # bottom
            base_y = image.height - total_height - padding
        
        # Apply offset
        base_x += x_offset
        base_y += y_offset
        
        # Create a separate text layer for rotation
        if text_rotation != 0:
            # We need to create a temporary layer that's big enough for the rotated text
            # The diagonal of the text rectangle is a safe size to accommodate any rotation
            diagonal = int(math.sqrt(max_width**2 + total_height**2)) + 100  # Add padding
            temp_layer = Image.new('RGBA', (diagonal * 2, diagonal * 2), (0, 0, 0, 0))
            temp_draw = ImageDraw.Draw(temp_layer)
            
            # Center position for the temporary layer
            temp_center_x = diagonal
            temp_center_y = diagonal
            
            # Adjust base positions to center the text on the temp layer
            temp_base_x = temp_center_x - max_width // 2
            temp_base_y = temp_center_y - total_height // 2
        else:
            # For non-rotated text, use the original layer and positions
            temp_layer = text_layer
            temp_draw = draw
            temp_base_x = base_x
            temp_base_y = base_y
        
        # Current y position for drawing
        current_y = temp_base_y
        current_x = temp_base_x
        
        # Draw text differently based on vertical or horizontal orientation
        if is_vertical:
            # Draw vertical text
            for i, line in enumerate(lines):
                # Reset y position for each line
                current_y = temp_base_y
                
                # Calculate x position based on alignment
                if text_alignment == 'left':
                    line_x = current_x
                elif text_alignment == 'center':
                    line_x = current_x + (line_widths[i] // 2)
                else:  # right
                    line_x = current_x + line_widths[i]
                
                # Draw each character vertically
                for char in line:
                    char_bbox = temp_draw.textbbox((0, 0), char, font=font)
                    char_width = char_bbox[2] - char_bbox[0]
                    char_height = char_bbox[3] - char_bbox[1]
                    
                    # Center character horizontally within line width
                    if text_alignment == 'left':
                        char_x = line_x
                    elif text_alignment == 'center':
                        char_x = line_x - (char_width // 2)
                    else:  # right
                        char_x = line_x - char_width
                    
                    char_position = (char_x, current_y)
                    
                    # Add effects for each character
                    self.draw_character_with_effects(
                        temp_draw, char, font, char_position,
                        text_color, outline_width, outline_color,
                        glow_radius, glow_intensity, chromatic_aberration
                    )
                    
                    # Move down for next character
                    current_y += char_height + letter_spacing
                
                # Move right for next line
                current_x += line_widths[i] + line_spacing
        else:
            # Draw horizontal text (original behavior)
            for i, line in enumerate(lines):
                # Calculate x position based on alignment
                if text_alignment == 'left':
                    text_x = temp_base_x
                elif text_alignment == 'center':
                    text_x = temp_base_x + (max_width - line_widths[i]) // 2
                else:  # right
                    text_x = temp_base_x + max_width - line_widths[i]
                    
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
                            temp_draw.text(outline_pos, line, font=font, fill=(*outline_color, outline_alpha))
                
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
                            temp_draw.text(pos, line, font=font, fill=(*text_color, alpha))
                
                # Add chromatic aberration
                if chromatic_aberration > 0:
                    # Red channel offset
                    temp_draw.text((text_position[0] + chromatic_aberration, text_position[1]),
                            line, font=font, fill=(255, 0, 0, 200))
                    # Blue channel offset
                    temp_draw.text((text_position[0] - chromatic_aberration, text_position[1]),
                            line, font=font, fill=(0, 0, 255, 200))
                
                # Main text
                temp_draw.text(text_position, line, font=font, fill=(*text_color, 255))
                
                # Update y position for next line
                current_y += line_heights[i] + line_spacing
        
        # Apply rotation if needed
        if text_rotation != 0:
            # Rotate the temporary layer
            rotated_layer = temp_layer.rotate(-text_rotation, resample=Image.BICUBIC, expand=True)
            
            # Calculate where to paste the rotated layer on the original text layer
            # We need to align the center of the rotated image with our original anchor point
            paste_x = base_x - (rotated_layer.width // 2) + (max_width // 2)
            paste_y = base_y - (rotated_layer.height // 2) + (total_height // 2)
            
            # Paste the rotated text onto the main text layer
            text_layer.paste(rotated_layer, (paste_x, paste_y), rotated_layer)
        elif text_rotation == 0 and temp_layer != text_layer:
            # If we created a temp layer but didn't rotate, we still need to paste it
            paste_x = base_x - (temp_layer.width // 2) + (max_width // 2)
            paste_y = base_y - (temp_layer.height // 2) + (total_height // 2)
            text_layer.paste(temp_layer, (paste_x, paste_y), temp_layer)
        
        return Image.alpha_composite(image, text_layer)

    def draw_character_with_effects(self, draw, char, font, position, 
                                   text_color, outline_width, outline_color,
                                   glow_radius, glow_intensity, chromatic_aberration):
        """Draw a single character with all effects applied"""
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
                    outline_pos = (position[0] + dx, position[1] + dy)
                    draw.text(outline_pos, char, font=font, fill=(*outline_color, outline_alpha))
        
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
                    pos = (position[0] + offset_x, position[1] + offset_y)
                    draw.text(pos, char, font=font, fill=(*text_color, alpha))
        
        # Add chromatic aberration
        if chromatic_aberration > 0:
            # Red channel offset
            draw.text((position[0] + chromatic_aberration, position[1]),
                    char, font=font, fill=(255, 0, 0, 200))
            # Blue channel offset
            draw.text((position[0] - chromatic_aberration, position[1]),
                    char, font=font, fill=(0, 0, 255, 200))
        
        # Main text
        draw.text(position, char, font=font, fill=(*text_color, 255))

    def add_text(self, images, text, font, position, x_offset, y_offset, padding,
                font_size, line_spacing, letter_spacing, text_color, glow_radius, 
                glow_intensity, outline_width, outline_color, chromatic_aberration,
                text_alignment, text_rotation, vertical_text):
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
                text_alignment, line_spacing, letter_spacing,
                text_rotation, vertical_text
            )
            
            # Convert back to tensor format
            image_np = np.array(image.convert('RGB')).astype(np.float32) / 255.0
            processed_tensors.append(torch.from_numpy(image_np))

        # Stack tensors back into batch
        result = torch.stack(processed_tensors)
        return (result,)

# Node registration for ComfyUI
NODE_CLASS_MAPPINGS = {
    "VideoTextV2": VideoTextV2
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VideoTextV2": "Video Text V2"
}
