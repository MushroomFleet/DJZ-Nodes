import numpy as np
import torch
from PIL import Image
import scipy.fft
import colorsys
import json
import cv2
import os
import glob
import importlib.util
import sys
import types

class VizLoader:
    @staticmethod
    def load_viz_file(file_path):
        """Load a .viz file as a Python module"""
        try:
            # Get module name from filename
            module_name = os.path.splitext(os.path.basename(file_path))[0]
            
            # Create module
            module = types.ModuleType(module_name)
            
            # Read the file content
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Compile the code
            code = compile(content, file_path, 'exec')
            
            # Execute the code in module's namespace
            exec(code, module.__dict__)
            
            return module
            
        except Exception as e:
            print(f"Error loading visualization {file_path}: {str(e)}")
            return None

class WinampVizV2:
    def __init__(self):
        self.type = "WinampVizV2"
        self.output_type = "IMAGE"
        self.output_dims = 3
        self.compatible_decorators = ["RepeatDecorator", "LoopDecorator"]
        self.required_extensions = []
        self.category = "Audio/Video"
        self.name = "Winamp-Style Visualizer V2"
        self.description = "Generates Winamp-style visualizations from audio input with extensible visualizations"
        self.current_frame = 0
        self.viz_modules = {}
        self.viz_states = {}
        self.load_visualizations()
        
    def load_visualizations(self):
        """Load all .viz files from the VIZ directory"""
        viz_dir = os.path.join(os.path.dirname(__file__), 'VIZ')
        viz_files = glob.glob(os.path.join(viz_dir, '*.viz'))
        
        for viz_file in viz_files:
            try:
                module = VizLoader.load_viz_file(viz_file)
                if module is not None and hasattr(module, 'render'):
                    module_name = os.path.splitext(os.path.basename(viz_file))[0]
                    self.viz_modules[module_name] = module
                    print(f"Successfully loaded visualization: {module_name}")
            except Exception as e:
                print(f"Error loading visualization {viz_file}: {str(e)}")
        
    @classmethod
    def INPUT_TYPES(cls):
        """Dynamically get list of available visualizations from VIZ directory"""
        viz_dir = os.path.join(os.path.dirname(__file__), 'VIZ')
        viz_files = glob.glob(os.path.join(viz_dir, '*.viz'))
        viz_names = []
        
        # Only include visualizations that can be successfully loaded
        for viz_file in viz_files:
            try:
                module = VizLoader.load_viz_file(viz_file)
                if module is not None and hasattr(module, 'render'):
                    name = os.path.splitext(os.path.basename(viz_file))[0]
                    viz_names.append(name)
            except Exception:
                continue
        
        if not viz_names:
            viz_names = ["none"]
            
        return {
            "required": {
                "audio": ("AUDIO",),
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
                    "default": 0,
                    "min": 0,
                    "max": 9999,
                    "step": 1
                }),
                "visualization": (viz_names,),
                "color_scheme": (["classic", "rainbow", "fire", "matrix"],),
                "sensitivity": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 5.0,
                    "step": 0.1
                }),
                "smoothing": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.0,
                    "max": 0.99,
                    "step": 0.01
                })
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    FUNCTION = "generate"

    def get_color_palette(self, scheme):
        """Get color palette for the visualization"""
        palettes = {
            "classic": [(0, 0, 255), (0, 255, 255), (0, 255, 0)],
            "rainbow": [(int(r*255), int(g*255), int(b*255)) 
                       for r,g,b in [colorsys.hsv_to_rgb(h/360, 1.0, 1.0) 
                                   for h in range(0, 360, 30)]],
            "fire": [(255, 0, 0), (255, 128, 0), (255, 255, 0)],
            "matrix": [(0, 32, 0), (0, 128, 0), (0, 255, 0)]
        }
        return palettes.get(scheme, palettes["classic"])

    def process_audio_chunk(self, audio_data, sample_rate):
        """Process audio data into features"""
        # Handle dictionary input recursively
        def extract_audio_data(data):
            if isinstance(data, dict):
                # Try common keys
                for key in ['samples', 'audio', 'data', 'tensor', 'array']:
                    if key in data:
                        return extract_audio_data(data[key])
                # If no common keys found, try the first value that's not a dict
                for value in data.values():
                    if not isinstance(value, dict):
                        return extract_audio_data(value)
            elif isinstance(data, torch.Tensor):
                return data.numpy()
            elif isinstance(data, (list, tuple, np.ndarray)):
                return np.asarray(data, dtype=np.float32)
            return data

        # Extract and convert audio data
        audio_data = extract_audio_data(audio_data)
        if audio_data is None:
            raise ValueError("Could not extract valid audio data from input")
            
        # Ensure we have a 1D numpy array
        audio_data = np.asarray(audio_data, dtype=np.float32).flatten()
        
        # Process a chunk of audio data to extract features
        chunk_size = int(sample_rate / self.fps)
        
        # Pre-process the entire audio data to ensure it's a numpy array
        if isinstance(audio_data, (list, tuple)):
            audio_data = np.array(audio_data, dtype=np.float32)
        
        # Create chunks using numpy array operations
        num_chunks = (len(audio_data) + chunk_size - 1) // chunk_size
        chunks = []
        for i in range(num_chunks):
            start = i * chunk_size
            end = start + chunk_size
            chunk = audio_data[start:end]
            if len(chunk) < chunk_size:
                # Pad last chunk if needed
                chunk = np.pad(chunk, (0, chunk_size - len(chunk)), mode='constant')
            chunks.append(chunk)
        
        features = []
        for chunk in chunks:
            # Compute FFT
            fft_data = np.abs(scipy.fft.fft(chunk)[:chunk_size//2])
            
            # Normalize
            fft_data = fft_data / np.max(fft_data) if np.max(fft_data) > 0 else fft_data
            
            # Extract features
            feature_dict = {
                'spectrum': fft_data,
                'waveform': chunk,
                'bass': np.mean(fft_data[:int(len(fft_data)*0.1)]),
                'mids': np.mean(fft_data[int(len(fft_data)*0.1):int(len(fft_data)*0.5)]),
                'highs': np.mean(fft_data[int(len(fft_data)*0.5):])
            }
            features.append(feature_dict)
            
        return features

    def generate(self, audio, width, height, fps, max_frames, visualization, color_scheme, sensitivity, smoothing):
        self.fps = fps
        
        # Reload visualizations to ensure we have the latest versions
        self.load_visualizations()
        
        # Check if visualization exists
        if visualization not in self.viz_modules:
            raise ValueError(f"Visualization '{visualization}' not found in VIZ directory")
        
        # Get visualization module
        viz_module = self.viz_modules[visualization]
        
        # Process audio into features
        audio_features = self.process_audio_chunk(audio, sample_rate=44100)
        
        # Get color palette
        color_palette = self.get_color_palette(color_scheme)
        
        # Generate frames
        frames = []
        frame_count = len(audio_features)
        if max_frames > 0:
            frame_count = min(frame_count, max_frames)
        
        for i in range(frame_count):
            # Apply smoothing to features
            if i > 0:
                for key in audio_features[i].keys():
                    if key not in ['waveform', 'spectrum']:  # Don't smooth raw data
                        audio_features[i][key] = (audio_features[i][key] * (1-smoothing) + 
                                                audio_features[i-1][key] * smoothing)
            
            # Apply sensitivity to features
            features = audio_features[i].copy()
            for key in ['bass', 'mids', 'highs']:
                features[key] *= sensitivity
            
            # Render frame
            if visualization in self.viz_states:
                frame, state = viz_module.render(features, width, height, color_palette, 
                                               self.viz_states[visualization])
                self.viz_states[visualization] = state
            else:
                result = viz_module.render(features, width, height, color_palette)
                if isinstance(result, tuple):
                    frame, state = result
                    self.viz_states[visualization] = state
                else:
                    frame = result
            
            # Convert to tensor
            frame_tensor = torch.from_numpy(frame).float() / 255.0
            frames.append(frame_tensor)
        
        # Stack frames into batch
        return (torch.stack(frames),)

NODE_CLASS_MAPPINGS = {
    "WinampVizV2": WinampVizV2
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "WinampVizV2": "🦙 Winamp Viz V2"
}
