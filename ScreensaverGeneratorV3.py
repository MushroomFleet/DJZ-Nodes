from typing import Dict, List, Tuple, Optional, Union, Any
from dataclasses import dataclass
import numpy as np
import torch
from PIL import Image
import colorsys
import cv2
import os
import sys
import glob
from torch import Tensor

# Custom exceptions for better error handling
class ScreensaverError(Exception):
    """Base exception class for screensaver generator errors."""
    pass

class PresetLoadError(ScreensaverError):
    """Raised when there's an error loading a preset."""
    pass

class ValidationError(ScreensaverError):
    """Raised when input validation fails."""
    pass

@dataclass
class PresetParameter:
    """Data class for preset parameter configuration."""
    type: str
    default: Union[int, float, str]
    min: Optional[Union[int, float]] = None
    max: Optional[Union[int, float]] = None
    step: Optional[Union[int, float]] = None
    choices: Optional[List[str]] = None

class ScreensaverGeneratorV3:
    """
    Enhanced screensaver generator V3 with external presets support.
    
    This class provides a flexible framework for generating animated
    screensavers using various presets and parameters. It supports
    dynamic loading of preset configurations and offers multiple
    color schemes and animation options.
    
    Attributes:
        type (str): Generator type identifier
        output_type (str): Output format specification
        output_dims (int): Number of output dimensions
        compatible_decorators (List[str]): List of compatible decorator types
        required_extensions (List[str]): Required file extensions
        category (str): Generator category
        name (str): Display name
        description (str): Detailed description
        current_frame (int): Current frame being processed
        states (Dict): State management for animations
        presets (Dict): Loaded preset configurations
    """
    
    # Base parameters that are always visible
    BASE_PARAMS: List[str] = ["preset", "width", "height", "fps", "max_frames", "color_scheme", "speed"]

    def __init__(self) -> None:
        self.type = "ScreensaverGeneratorV3"
        self.output_type = "IMAGE"
        self.output_dims = 3
        self.compatible_decorators = ["RepeatDecorator", "LoopDecorator"]
        self.required_extensions = []
        self.category = "Video"
        self.name = "Screensaver Generator V3"
        self.description = "Enhanced screensaver generator with external presets"
        self.current_frame = 0
        self.states: Dict[str, Any] = {}
        self.presets: Dict[str, Any] = {}
        self._color_manager = ColorPaletteManager()
        self.load_presets()
        
    def load_presets(self) -> None:
        """
        Load all available screensaver presets from the ScreenGen directory.
        
        This method scans the ScreenGen directory for .scg files containing
        screensaver preset definitions. Each preset is loaded and validated
        before being added to the available presets.
        
        Raises:
            PresetLoadError: If there are issues loading or validating presets
        """
        preset_dir = os.path.join(os.path.dirname(__file__), "ScreenGen")
        if not os.path.exists(preset_dir):
            raise PresetLoadError(f"ScreenGen directory not found at {preset_dir}")

        # Add ScreenGen directory to Python path if not already there
        if preset_dir not in sys.path:
            sys.path.append(preset_dir)
            
        # Get all .scg files
        preset_files = glob.glob(os.path.join(preset_dir, "*.scg"))
        if not preset_files:
            raise PresetLoadError("No preset files (.scg) found in ScreenGen directory")
        
        for preset_path in preset_files:
            filename = os.path.basename(preset_path)
            module_name = filename[:-4]  # Remove .scg extension
            
            try:
                # Load and validate the module content
                with open(preset_path, 'r', encoding='utf-8') as f:
                    module_content = f.read()
                
                if not module_content.strip():
                    raise PresetLoadError(f"Empty preset file: {filename}")
                
                # Create namespace for the module
                namespace: Dict[str, Any] = {}
                
                try:
                    # Execute the module content in the namespace
                    exec(module_content, namespace)
                except Exception as e:
                    raise PresetLoadError(f"Syntax error in preset {filename}: {str(e)}")
                
                # Find and validate the screensaver class
                screensaver_class = None
                for item_name, item in namespace.items():
                    if isinstance(item, type) and item_name.endswith('Screensaver'):
                        screensaver_class = item
                        break
                
                if not screensaver_class:
                    raise PresetLoadError(f"No screensaver class found in {filename}")
                
                # Validate the preset class has required attributes and methods
                preset_instance = screensaver_class()
                required_attrs = ['name', 'parameters', 'render']
                missing_attrs = [attr for attr in required_attrs if not hasattr(preset_instance, attr)]
                
                if missing_attrs:
                    raise PresetLoadError(
                        f"Preset {filename} missing required attributes: {', '.join(missing_attrs)}"
                    )
                
                # Cache the preset instance
                preset_name = preset_instance.name.lower()
                self.presets[preset_name] = preset_instance
                
            except PresetLoadError as e:
                # Re-raise PresetLoadError with additional context
                raise PresetLoadError(f"Failed to load preset {filename}: {str(e)}")
            except Exception as e:
                # Convert unexpected errors to PresetLoadError
                raise PresetLoadError(f"Unexpected error loading preset {filename}: {str(e)}")

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
    
    def _extract_preset_parameters(self, preset_instance: Any, kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract and validate preset-specific parameters from kwargs.
        
        Args:
            preset_instance: The preset instance to extract parameters for
            kwargs: Dictionary of input parameters
            
        Returns:
            Dictionary of validated preset parameters
            
        Raises:
            ValidationError: If required parameters are missing or invalid
        """
        preset_params = {}
        preset_name = preset_instance.name.lower()
        
        for param_name, param_config in preset_instance.parameters.items():
            param_key = f"{preset_name}_{param_name}"
            if param_key not in kwargs:
                raise ValidationError(f"Missing required parameter: {param_key}")
                
            value = kwargs[param_key]
            
            # Validate numeric parameter ranges
            if param_config["type"] in ["INT", "FLOAT"]:
                if value < param_config["min"] or value > param_config["max"]:
                    raise ValidationError(
                        f"Parameter {param_key} value {value} outside valid range "
                        f"[{param_config['min']}, {param_config['max']}]"
                    )
            
            preset_params[param_name] = value
            
        return preset_params
        
    def _generate_frame(
        self,
        preset_instance: Any,
        frame_index: int,
        width: int,
        height: int,
        color_palette: List[Tuple[int, int, int]],
        speed: float,
        state: Optional[Any],
        preset_params: Dict[str, Any]
    ) -> Tuple[torch.Tensor, Any]:
        """
        Generate a single animation frame.
        
        Args:
            preset_instance: The preset instance to use for rendering
            frame_index: Current frame number
            width: Frame width in pixels
            height: Frame height in pixels
            color_palette: List of RGB color tuples
            speed: Animation speed multiplier
            state: Current animation state
            preset_params: Preset-specific parameters
            
        Returns:
            Tuple of (frame tensor, new state)
            
        Raises:
            ScreensaverError: If frame generation fails
        """
        try:
            # Render frame using the preset
            frame, new_state = preset_instance.render(
                width, height, frame_index,
                color_palette, speed, state,
                preset_params
            )
            
            # Convert to tensor with proper normalization
            frame_tensor = torch.from_numpy(frame).float() / 255.0
            
            return frame_tensor, new_state
            
        except Exception as e:
            raise ScreensaverError(f"Frame generation failed: {str(e)}")

    def generate(
        self,
        width: int,
        height: int,
        fps: int,
        max_frames: int,
        preset: str,
        color_scheme: str,
        speed: float,
        **kwargs: Any
    ) -> Tuple[torch.Tensor]:
        """
        Generate screensaver animation frames.
        
        Args:
            width: Frame width in pixels
            height: Frame height in pixels
            fps: Frames per second
            max_frames: Total number of frames to generate
            preset: Name of the screensaver preset to use
            color_scheme: Color scheme name
            speed: Animation speed multiplier
            **kwargs: Additional preset-specific parameters
            
        Returns:
            Tuple containing a tensor of animation frames
            
        Raises:
            ValidationError: If parameters are invalid
            ScreensaverError: If frame generation fails
        """
        try:
            # Validate preset
            if preset not in self.presets:
                raise ValidationError(f"Unknown preset: {preset}")
                
            # Get preset instance and validate parameters
            preset_instance = self.presets[preset]
            preset_params = self._extract_preset_parameters(preset_instance, kwargs)
            
            # Get color palette
            try:
                color_palette = self._color_manager.get_palette(color_scheme)
            except ValidationError as e:
                raise ValidationError(f"Color scheme error: {str(e)}")
            
            # Pre-allocate frame list with known size for better memory efficiency
            frames = []
            state = None
            
            # Generate frames with proper error handling
            for i in range(max_frames):
                frame_tensor, state = self._generate_frame(
                    preset_instance, i, width, height,
                    color_palette, speed, state, preset_params
                )
                frames.append(frame_tensor)
            
            # Stack frames into batch efficiently
            return (torch.stack(frames),)
            
        except ValidationError:
            raise  # Re-raise validation errors as-is
        except Exception as e:
            raise ScreensaverError(f"Animation generation failed: {str(e)}")

class ColorPaletteManager:
    """
    Manages color palette generation and caching for screensaver animations.
    
    This class handles the creation and caching of color palettes used in
    screensaver animations. It supports multiple color schemes and provides
    efficient access to pre-computed palettes.
    """
    
    def __init__(self) -> None:
        self._palette_cache: Dict[str, List[Tuple[int, int, int]]] = {}
        self._initialize_palettes()
    
    def _initialize_palettes(self) -> None:
        """Initialize static color palettes."""
        self._palette_cache.update({
            "classic": [(0, 0, 255), (0, 255, 255), (0, 255, 0)],
            "neon": [(255, 0, 255), (0, 255, 255), (255, 255, 0)],
            "monochrome": [(0, 255, 0), (0, 192, 0), (0, 128, 0)]
        })
    
    def _generate_rainbow_palette(self) -> List[Tuple[int, int, int]]:
        """Generate rainbow color palette."""
        return [(int(r*255), int(g*255), int(b*255)) 
                for r,g,b in [colorsys.hsv_to_rgb(h/360, 1.0, 1.0) 
                             for h in range(0, 360, 30)]]
    
    def get_palette(self, scheme: str) -> List[Tuple[int, int, int]]:
        """
        Get color palette for the specified scheme.
        
        Args:
            scheme: Color scheme name
            
        Returns:
            List of RGB color tuples
            
        Raises:
            ValidationError: If scheme is invalid
        """
        if scheme not in ["classic", "rainbow", "neon", "monochrome"]:
            raise ValidationError(f"Invalid color scheme: {scheme}")
            
        # Generate and cache rainbow palette on first use
        if scheme == "rainbow" and scheme not in self._palette_cache:
            self._palette_cache["rainbow"] = self._generate_rainbow_palette()
            
        return self._palette_cache.get(scheme, self._palette_cache["classic"])

    def get_color_palette(self, scheme: str) -> List[Tuple[int, int, int]]:
        """Get color palette for the screensaver (legacy method)"""
        return self.get_palette(scheme)

NODE_CLASS_MAPPINGS = {
    "ScreensaverGeneratorV3": ScreensaverGeneratorV3
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ScreensaverGeneratorV3": "🖥️ Screensaver Generator V3"
}
