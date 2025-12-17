import colorsys
import random

class DJZColorWheel:
    """
    A custom ComfyUI node that generates color combinations based on color wheel theory
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "base_color": ("STRING", {
                    "default": "#FF0000",
                    "multiline": False,
                    "placeholder": "Enter hex color (e.g., #FF0000)"
                }),
                "color_scheme": (["Complementary", "Triadic", "Tetradic", "Analogous", "Split-Complementary", "Square"], {
                    "default": "Complementary"
                }),
                "contrast_style": (["Standard", "High Contrast", "Muted", "Vibrant", "Pastel", "Dark"], {
                    "default": "Standard"
                }),
                "randomize": ("BOOLEAN", {
                    "default": False,
                    "label_on": "Random",
                    "label_off": "Fixed"
                }),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 999999
                })
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("color_1", "color_2", "color_3")
    FUNCTION = "generate_colors"
    CATEGORY = "DJZ/Color"
    DESCRIPTION = "Generate harmonious color combinations using color wheel theory"

    def hex_to_hsv(self, hex_color):
        """Convert hex color to HSV"""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r, g, b = r/255.0, g/255.0, b/255.0
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        return h * 360, s, v  # Convert hue to degrees

    def hsv_to_hex(self, h, s, v):
        """Convert HSV to hex color"""
        h = h / 360.0  # Convert degrees to 0-1 range
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        r, g, b = int(r * 255), int(g * 255), int(b * 255)
        return f"#{r:02X}{g:02X}{b:02X}"

    def adjust_contrast_style(self, h, s, v, style):
        """Adjust saturation and value based on contrast style"""
        if style == "High Contrast":
            s = min(1.0, s * 1.3)
            v = max(0.8, v) if v > 0.5 else min(0.2, v)
        elif style == "Muted":
            s = max(0.2, s * 0.6)
            v = max(0.3, min(0.7, v))
        elif style == "Vibrant":
            s = max(0.8, s)
            v = max(0.8, v)
        elif style == "Pastel":
            s = max(0.2, min(0.4, s))
            v = max(0.8, v)
        elif style == "Dark":
            v = max(0.1, min(0.4, v))
            s = max(0.6, s)
        # "Standard" uses original values
        
        return h, s, v

    def generate_color_scheme(self, base_h, base_s, base_v, scheme_type, contrast_style):
        """Generate colors based on the selected scheme"""
        colors = []
        
        if scheme_type == "Complementary":
            # Base color + complementary (180° opposite)
            colors.append(self.adjust_contrast_style(base_h, base_s, base_v, contrast_style))
            comp_h = (base_h + 180) % 360
            colors.append(self.adjust_contrast_style(comp_h, base_s, base_v, contrast_style))
            # Add a neutral variation
            colors.append(self.adjust_contrast_style(base_h, base_s * 0.3, base_v * 0.8, contrast_style))
            
        elif scheme_type == "Triadic":
            # Three colors equally spaced (120° apart)
            for i in range(3):
                h = (base_h + i * 120) % 360
                colors.append(self.adjust_contrast_style(h, base_s, base_v, contrast_style))
                
        elif scheme_type == "Tetradic":
            # Four colors in two complementary pairs (90° apart)
            angles = [0, 90, 180, 270]
            for i in range(3):  # Only take first 3 for our 3 outputs
                h = (base_h + angles[i]) % 360
                colors.append(self.adjust_contrast_style(h, base_s, base_v, contrast_style))
                
        elif scheme_type == "Analogous":
            # Three adjacent colors (30° apart)
            for i in range(3):
                h = (base_h + (i - 1) * 30) % 360
                # Vary saturation and value slightly for depth
                s_var = base_s + (i - 1) * 0.1
                v_var = base_v + (i - 1) * 0.05
                s_var = max(0.1, min(1.0, s_var))
                v_var = max(0.1, min(1.0, v_var))
                colors.append(self.adjust_contrast_style(h, s_var, v_var, contrast_style))
                
        elif scheme_type == "Split-Complementary":
            # Base + two colors adjacent to its complement
            colors.append(self.adjust_contrast_style(base_h, base_s, base_v, contrast_style))
            comp_h = (base_h + 180) % 360
            colors.append(self.adjust_contrast_style((comp_h - 30) % 360, base_s, base_v, contrast_style))
            colors.append(self.adjust_contrast_style((comp_h + 30) % 360, base_s, base_v, contrast_style))
            
        elif scheme_type == "Square":
            # Four colors equally spaced (90° apart)
            for i in range(3):  # Only take first 3 for our 3 outputs
                h = (base_h + i * 90) % 360
                colors.append(self.adjust_contrast_style(h, base_s, base_v, contrast_style))
        
        return colors

    def generate_colors(self, base_color, color_scheme, contrast_style, randomize, seed):
        """Main function to generate the color combination"""
        
        # Set random seed if randomize is enabled
        if randomize:
            random.seed(seed)
            # Generate a random base color
            base_h = random.uniform(0, 360)
            base_s = random.uniform(0.5, 1.0)
            base_v = random.uniform(0.6, 1.0)
        else:
            # Use the provided base color
            try:
                base_h, base_s, base_v = self.hex_to_hsv(base_color)
            except (ValueError, IndexError):
                # Fallback to red if invalid hex
                base_h, base_s, base_v = 0, 1.0, 1.0
        
        # Generate the color scheme
        color_hsv_list = self.generate_color_scheme(base_h, base_s, base_v, color_scheme, contrast_style)
        
        # Convert to hex codes
        hex_colors = []
        for h, s, v in color_hsv_list:
            hex_colors.append(self.hsv_to_hex(h, s, v))
        
        # Ensure we have exactly 3 colors
        while len(hex_colors) < 3:
            hex_colors.append(hex_colors[-1])  # Duplicate last color if needed
        
        return (hex_colors[0], hex_colors[1], hex_colors[2])


# Node registration for ComfyUI
NODE_CLASS_MAPPINGS = {
    "DJZColorWheel": DJZColorWheel
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DJZColorWheel": "DJZ Color Wheel"
}

# Optional: Add node description
NODE_DESCRIPTIONS = {
    "DJZColorWheel": "Generate harmonious color combinations using color wheel theory. Supports multiple color schemes and contrast styles."
}