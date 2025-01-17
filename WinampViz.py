import numpy as np
import torch
from PIL import Image
import scipy.fft
import colorsys
import json
import cv2

class WinampViz:
    def __init__(self):
        self.type = "WinampViz"
        self.output_type = "IMAGE"
        self.output_dims = 3
        self.compatible_decorators = ["RepeatDecorator", "LoopDecorator"]
        self.required_extensions = []
        self.category = "Audio/Video"
        self.name = "Winamp-Style Visualizer"
        self.description = "Generates Winamp-style visualizations from audio input"
        self.default_preset = None
        self.current_frame = 0
        self.particle_systems = []
        self.color_offset = 0.0
        
    @classmethod
    def INPUT_TYPES(cls):
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
                "viz_type": (["oscilloscope", "spectrum", "particle_storm", "plasma_wave", "milkdrop_bars", "circular_wave", "butterfly", "tunnel_beat"],),
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
    
    def get_presets(self):
        return {
            "classic_oscilloscope": {
                "viz_type": "oscilloscope",
                "color_scheme": "classic",
                "sensitivity": 1.0,
                "smoothing": 0.5
            },
            "particle_storm_rainbow": {
                "viz_type": "particle_storm",
                "color_scheme": "rainbow",
                "sensitivity": 1.5,
                "smoothing": 0.7
            },
            "matrix_spectrum": {
                "viz_type": "spectrum",
                "color_scheme": "matrix",
                "sensitivity": 1.2,
                "smoothing": 0.6
            },
            "milkdrop_rainbow": {
                "viz_type": "milkdrop_bars",
                "color_scheme": "rainbow",
                "sensitivity": 1.3,
                "smoothing": 0.65
            },
            "circular_fire": {
                "viz_type": "circular_wave",
                "color_scheme": "fire",
                "sensitivity": 1.4,
                "smoothing": 0.6
            },
            "butterfly_classic": {
                "viz_type": "butterfly",
                "color_scheme": "classic",
                "sensitivity": 1.2,
                "smoothing": 0.7
            },
            "tunnel_matrix": {
                "viz_type": "tunnel_beat",
                "color_scheme": "matrix",
                "sensitivity": 1.6,
                "smoothing": 0.75
            }
        }

    def process_audio_chunk(self, audio_data, sample_rate):
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

    def get_color_palette(self, scheme):
        palettes = {
            "classic": [(0, 0, 255), (0, 255, 255), (0, 255, 0)],
            "rainbow": [(int(r*255), int(g*255), int(b*255)) for r,g,b in [colorsys.hsv_to_rgb(h/360, 1.0, 1.0) for h in range(0, 360, 30)]],
            "fire": [(255, 0, 0), (255, 128, 0), (255, 255, 0)],
            "matrix": [(0, 32, 0), (0, 128, 0), (0, 255, 0)]
        }
        return palettes.get(scheme, palettes["classic"])

    def render_oscilloscope(self, features, width, height, color_scheme):
        image = np.zeros((height, width, 3), dtype=np.uint8)
        color_palette = self.get_color_palette(color_scheme)
        
        waveform = features['waveform']
        points = []
        for x in range(width):
            sample_idx = int(x * len(waveform) / width)
            y = int(height/2 + waveform[sample_idx] * height/2)
            y = max(0, min(y, height-1))  # Clamp y value
            points.append((x, y))
        
        # Draw the waveform using numpy operations
        points = np.array(points)
        for i in range(len(points)-1):
            color = color_palette[i % len(color_palette)]
            p1 = tuple(points[i])
            p2 = tuple(points[i+1])
            # Draw line using numpy slicing
            x1, y1 = p1
            x2, y2 = p2
            if x1 == x2:  # Vertical line
                y_start, y_end = sorted([y1, y2])
                image[y_start:y_end+1, x1] = color
            else:  # Use cv2.line for non-vertical lines
                cv2.line(image, p1, p2, color, 2)
            
        return image

    def render_spectrum(self, features, width, height, color_scheme):
        image = np.zeros((height, width, 3), dtype=np.uint8)
        color_palette = self.get_color_palette(color_scheme)
        
        spectrum = features['spectrum']
        bar_width = max(1, width // len(spectrum))
        
        for i, amp in enumerate(spectrum):
            if i * bar_width >= width:
                break
                
            bar_height = int(amp * height)
            bar_height = max(1, min(bar_height, height))  # Clamp height
            color = color_palette[i % len(color_palette)]
            
            # Draw rectangle using numpy slicing
            x_start = i * bar_width
            x_end = min(x_start + bar_width, width)
            y_start = height - bar_height
            y_end = height
            
            image[y_start:y_end, x_start:x_end] = color
            
        return image

    def update_particle_system(self, features):
        # Update particle positions and properties based on audio features
        for particle in self.particle_systems[:]:
            particle['life'] -= 1.0 / self.fps
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            
            # Remove dead particles
            if particle['life'] <= 0:
                self.particle_systems.remove(particle)
                
        # Add new particles based on audio intensity
        intensity = (features['bass'] + features['mids'] + features['highs']) / 3
        if intensity > 0.1:
            for _ in range(int(intensity * 10)):
                angle = np.random.rand() * 2 * np.pi
                speed = 2 + intensity * 5
                self.particle_systems.append({
                    'x': self.width // 2,
                    'y': self.height // 2,
                    'vx': np.cos(angle) * speed,
                    'vy': np.sin(angle) * speed,
                    'size': 3 + intensity * 10,
                    'life': 1.0,
                    'color': self.color_offset
                })

    def render_particle_storm(self, features, width, height, color_scheme):
        image = np.zeros((height, width, 3), dtype=np.uint8)
        self.update_particle_system(features)
        
        for particle in self.particle_systems:
            hue = (self.color_offset + particle['life']) % 1.0
            rgb = colorsys.hsv_to_rgb(hue, 0.8, 1.0)
            color = tuple(int(x * 255) for x in rgb)
            
            cv2.circle(image,
                      (int(particle['x']), int(particle['y'])),
                      int(particle['size'] * particle['life']),
                      color,
                      -1)
            
        self.color_offset += 0.01
        return image

    def render_plasma_wave(self, features, width, height, color_scheme):
        image = np.zeros((height, width, 3), dtype=np.uint8)
        color_palette = self.get_color_palette(color_scheme)
        
        # Create plasma effect using sine waves modulated by audio features
        for y in range(height):
            for x in range(width):
                v = np.sin(x/30.0 + features['bass'] * 10)
                v += np.sin(y/20.0 + features['mids'] * 10)
                v += np.sin((x+y)/40.0 + features['highs'] * 10)
                v = (v + 3) / 6.0
                
                color_idx = int(v * (len(color_palette)-1))
                image[y,x] = color_palette[color_idx]
                
        return image

    def render_milkdrop_bars(self, features, width, height, color_scheme):
        image = np.zeros((height, width, 3), dtype=np.uint8)
        color_palette = self.get_color_palette(color_scheme)
        
        spectrum = features['spectrum']
        num_bars = min(32, len(spectrum))
        bar_width = width // num_bars
        
        for i in range(num_bars):
            # Calculate bar properties
            amp = spectrum[i] * (1 + features['bass'] * 2)  # Amplify with bass
            bar_height = int(amp * height * 0.8)  # 80% max height
            
            # Calculate color based on amplitude and position
            color_idx = int((i / num_bars + amp) * len(color_palette)) % len(color_palette)
            color = color_palette[color_idx]
            
            # Draw main bar
            x_start = i * bar_width
            x_end = x_start + bar_width - 1
            y_start = height - bar_height
            y_end = height
            
            # Add glow effect
            cv2.rectangle(image, (x_start, y_start), (x_end, y_end), color, -1)
            cv2.GaussianBlur(image[y_start:y_end, x_start:x_end], (5, 5), 2, 
                           dst=image[y_start:y_end, x_start:x_end])
            
        return image

    def render_circular_wave(self, features, width, height, color_scheme):
        image = np.zeros((height, width, 3), dtype=np.uint8)
        color_palette = self.get_color_palette(color_scheme)
        center_x, center_y = width // 2, height // 2
        
        # Create circular waves based on audio features
        max_radius = min(width, height) // 2
        num_circles = 32
        
        for i in range(num_circles):
            radius = int(max_radius * (i / num_circles))
            thickness = max(1, int(radius * 0.1))
            
            # Modulate radius with audio features
            radius_mod = radius * (1 + features['mids'] * 0.3)
            
            # Calculate color
            color_idx = int((i / num_circles + features['highs']) * len(color_palette)) % len(color_palette)
            color = color_palette[color_idx]
            
            cv2.circle(image, (center_x, center_y), int(radius_mod), color, thickness)
            
        return image

    def render_butterfly(self, features, width, height, color_scheme):
        image = np.zeros((height, width, 3), dtype=np.uint8)
        color_palette = self.get_color_palette(color_scheme)
        center_x, center_y = width // 2, height // 2
        
        # Generate butterfly curve points modulated by audio
        t = np.linspace(0, 24*np.pi, 1000)
        bass_mod = 1 + features['bass'] * 2
        mids_mod = 1 + features['mids']
        
        x = np.sin(t) * (np.exp(np.cos(t)) - 2*np.cos(4*t) - np.power(np.sin(t/12), 5)) * bass_mod
        y = np.cos(t) * (np.exp(np.cos(t)) - 2*np.cos(4*t) - np.power(np.sin(t/12), 5)) * mids_mod
        
        # Scale and center the points
        scale = min(width, height) * 0.2
        x = (x * scale / np.max(np.abs(x)) + center_x).astype(np.int32)
        y = (y * scale / np.max(np.abs(y)) + center_y).astype(np.int32)
        
        # Draw the curve with color variation
        points = np.column_stack((x, y))
        for i in range(len(points)-1):
            color_idx = int((i / len(points) + features['highs']) * len(color_palette)) % len(color_palette)
            cv2.line(image, tuple(points[i]), tuple(points[i+1]), color_palette[color_idx], 2)
            
        return image

    def render_tunnel_beat(self, features, width, height, color_scheme):
        image = np.zeros((height, width, 3), dtype=np.uint8)
        color_palette = self.get_color_palette(color_scheme)
        center_x, center_y = width // 2, height // 2
        
        # Create tunnel effect modulated by audio
        bass_intensity = features['bass'] * 2
        for radius in range(0, min(width, height) // 2, 10):
            # Modulate radius with bass
            radius_mod = int(radius * (1 + bass_intensity * np.sin(radius * 0.1)))
            
            # Calculate color based on radius and audio features
            color_idx = int((radius / (min(width, height) // 2) + features['mids']) * len(color_palette)) % len(color_palette)
            color = color_palette[color_idx]
            
            # Draw modulated circle
            thickness = max(1, int(3 + features['highs'] * 5))
            cv2.circle(image, (center_x, center_y), radius_mod, color, thickness)
            
            # Add beat-reactive glow
            if features['bass'] > 0.6:
                cv2.GaussianBlur(image, (5, 5), features['bass'] * 3)
                
        return image

    def generate(self, audio, width, height, fps, max_frames, viz_type, color_scheme, sensitivity, smoothing):
        self.width = width
        self.height = height
        self.fps = fps
        
        # Process audio into features
        audio_features = self.process_audio_chunk(audio, sample_rate=44100)
        
        # Generate frames
        frames = []
        render_funcs = {
            "oscilloscope": self.render_oscilloscope,
            "spectrum": self.render_spectrum,
            "particle_storm": self.render_particle_storm,
            "plasma_wave": self.render_plasma_wave,
            "milkdrop_bars": self.render_milkdrop_bars,
            "circular_wave": self.render_circular_wave,
            "butterfly": self.render_butterfly,
            "tunnel_beat": self.render_tunnel_beat
        }
        
        frame_count = len(audio_features)
        if max_frames > 0:
            frame_count = min(frame_count, max_frames)
            
        render_func = render_funcs[viz_type]
        
        for i in range(frame_count):
            # Apply smoothing to features
            if i > 0:
                for key in audio_features[i].keys():
                    audio_features[i][key] = (audio_features[i][key] * (1-smoothing) + 
                                            audio_features[i-1][key] * smoothing)
            
            # Apply sensitivity
            features = {k: v * sensitivity for k, v in audio_features[i].items()}
            
            # Render frame
            frame = render_func(features, width, height, color_scheme)
            
            # Convert to tensor
            frame_tensor = torch.from_numpy(frame).float() / 255.0
            frames.append(frame_tensor)
        
        # Stack frames into batch
        return (torch.stack(frames),)

NODE_CLASS_MAPPINGS = {
    "WinampViz": WinampViz
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "WinampViz": "🦙 Winamp Viz"
}
