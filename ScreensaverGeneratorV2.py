import numpy as np
import torch
from PIL import Image
import colorsys
import cv2
import os
import sys
import glob

class ScreensaverGeneratorV2:
    # Base parameters that are always visible
    BASE_PARAMS = ["preset", "width", "height", "fps", "max_frames", "color_scheme", "speed"]

    def __init__(self):
        self.type = "ScreensaverGeneratorV2"
        self.output_type = "IMAGE"
        self.output_dims = 3
        self.compatible_decorators = ["RepeatDecorator", "LoopDecorator"]
        self.required_extensions = []
        self.category = "Video"
        self.name = "Screensaver Generator V2"
        self.description = "Enhanced screensaver generator with external presets"
        self.current_frame = 0
        self.states = {}
        self.presets = {}
        self.load_presets()
        
    def load_presets(self):
        """Load all available screensaver presets from the ScreenGen directory"""
        preset_dir = os.path.join(os.path.dirname(__file__), "ScreenGen")
        if not os.path.exists(preset_dir):
            print(f"Warning: ScreenGen directory not found at {preset_dir}")
            return

        # Add ScreenGen directory to Python path if not already there
        if preset_dir not in sys.path:
            sys.path.append(preset_dir)
            
        # Get all .scg files
        preset_files = glob.glob(os.path.join(preset_dir, "*.scg"))
        
        for preset_path in preset_files:
            filename = os.path.basename(preset_path)
            module_name = filename[:-4]  # Remove .scg extension
            
            try:
                # Load the module content
                with open(preset_path, 'r') as f:
                    module_content = f.read()
                
                # Create namespace for the module
                namespace = {}
                
                # Execute the module content in the namespace
                exec(module_content, namespace)
                
                # Find the screensaver class in the namespace
                screensaver_class = None
                for item_name, item in namespace.items():
                    if isinstance(item, type) and item_name.endswith('Screensaver'):
                        screensaver_class = item
                        break
                
                if screensaver_class:
                    preset_instance = screensaver_class()
                    self.presets[preset_instance.name.lower()] = preset_instance
                else:
                    print(f"Warning: No screensaver class found in {filename}")
                    
            except Exception as e:
                print(f"Error loading preset {filename}: {str(e)}")

    @classmethod
    def INPUT_TYPES(cls):
        """Define input parameters dynamically based on loaded presets"""
        # Create an instance to load presets
        instance = cls()
        
        # Base parameters
        input_types = {
            "required": {
                "preset": (list(instance.presets.keys()),),  # This needs to be first to control visibility
                "width": ("INT", {
                    "default": 512,
                    "min": 64,
                    "max": 4096,
                    "step": 64
                }),
                "height": ("INT", {
                    "default": 512,
                    "min": 64,
                    "max": 4096,
                    "step": 64
                }),
                "fps": ("INT", {
                    "default": 30,
                    "min": 1,
                    "max": 60,
                    "step": 1
                }),
                "max_frames": ("INT", {
                    "default": 60,
                    "min": 1,
                    "max": 9999,
                    "step": 1
                }),
                "color_scheme": (["classic", "rainbow", "neon", "monochrome"],),
                "speed": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 5.0,
                    "step": 0.1
                })
            }
        }
        
        # Add parameters for each preset
        for preset_name, preset in instance.presets.items():
            for param_name, param_config in preset.parameters.items():
                input_name = f"{preset_name}_{param_name}"
                param_type = param_config["type"]
                
                if param_type == "INT":
                    input_types["required"][input_name] = ("INT", {
                        "default": param_config["default"],
                        "min": param_config["min"],
                        "max": param_config["max"],
                        "step": param_config["step"]
                    })
                elif param_type == "FLOAT":
                    input_types["required"][input_name] = ("FLOAT", {
                        "default": param_config["default"],
                        "min": param_config["min"],
                        "max": param_config["max"],
                        "step": param_config["step"]
                    })
                elif param_type == "STRING" and "choices" in param_config:
                    input_types["required"][input_name] = (param_config["choices"],)
        
        return input_types

    @classmethod
    def VALIDATE_INPUTS(cls, **kwargs):
        """Validate inputs and handle visibility"""
        current_preset = kwargs.get("preset")
        if not current_preset:
            return True
            
        # Create instance to access presets
        instance = cls()
        
        # Get visible parameters for current preset
        visible_params = instance.get_visible_parameters(current_preset)
        
        # Check if all required parameters for the preset are present
        for param in visible_params:
            if param not in kwargs:
                return False
                
        return True

    def get_visible_parameters(self, preset):
        """Get list of visible parameters for current preset"""
        visible = self.BASE_PARAMS.copy()
        
        if preset in self.presets:
            preset_instance = self.presets[preset]
            # Add preset-specific parameters
            for param_name in preset_instance.parameters:
                visible.append(f"{preset}_{param_name}")
                
        return visible

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        """Tell ComfyUI to update when preset changes"""
        return float("nan")  # Forces update when parameters change

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    FUNCTION = "generate"

    def get_color_palette(self, scheme):
        """Get color palette for the screensaver"""
        palettes = {
            "classic": [(0, 0, 255), (0, 255, 255), (0, 255, 0)],
            "rainbow": [(int(r*255), int(g*255), int(b*255)) 
                       for r,g,b in [colorsys.hsv_to_rgb(h/360, 1.0, 1.0) 
                                   for h in range(0, 360, 30)]],
            "neon": [(255, 0, 255), (0, 255, 255), (255, 255, 0)],
            "monochrome": [(0, 255, 0), (0, 192, 0), (0, 128, 0)]
        }
        return palettes.get(scheme, palettes["classic"])

    def generate(self, width, height, fps, max_frames, preset, color_scheme, speed, **kwargs):
        """Generate screensaver animation frames"""
        if preset not in self.presets:
            raise ValueError(f"Unknown preset: {preset}")
            
        # Get color palette
        color_palette = self.get_color_palette(color_scheme)
        
        # Get the preset instance
        preset_instance = self.presets[preset]
        
        # Extract preset-specific parameters
        preset_params = {}
        for param_name in preset_instance.parameters.keys():
            param_key = f"{preset}_{param_name}"
            if param_key in kwargs:
                preset_params[param_name] = kwargs[param_key]
        
        # Generate frames
        frames = []
        state = None
        
        for i in range(max_frames):
            # Render frame using the preset
            frame, state = preset_instance.render(
                width, height, i, color_palette, speed, state, preset_params
            )
            
            # Convert to tensor
            frame_tensor = torch.from_numpy(frame).float() / 255.0
            frames.append(frame_tensor)
        
        # Stack frames into batch
        return (torch.stack(frames),)

NODE_CLASS_MAPPINGS = {
    "ScreensaverGeneratorV2": ScreensaverGeneratorV2
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ScreensaverGeneratorV2": "🖥️ Screensaver Generator V2"
}
