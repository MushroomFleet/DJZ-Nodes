import numpy as np
import torch
from PIL import Image
import colorsys
import cv2

class ScreensaverGenerator:
    def __init__(self):
        self.type = "ScreensaverGenerator"
        self.output_type = "IMAGE"
        self.output_dims = 3
        self.compatible_decorators = ["RepeatDecorator", "LoopDecorator"]
        self.required_extensions = []
        self.category = "Video"
        self.name = "Screensaver Generator"
        self.description = "Generates classic screensaver-style animations"
        self.current_frame = 0
        self.states = {}
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
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
                "preset": (["pipes", "starfield", "matrix", "bounce", "plasma"],),
                "color_scheme": (["classic", "rainbow", "neon", "monochrome"],),
                "speed": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 5.0,
                    "step": 0.1
                })
            }
        }

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

    def render_pipes(self, width, height, frame, colors, speed, state):
        """Render 3D pipes screensaver"""
        if 'pipes' not in state:
            state['pipes'] = []
            state['next_pipe'] = 0
        
        img = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Update existing pipes
        for pipe in state['pipes']:
            # Update pipe position and draw
            pipe['length'] += speed * 5
            cv2.line(img, 
                    (int(pipe['start'][0]), int(pipe['start'][1])),
                    (int(pipe['start'][0] + pipe['dir'][0] * pipe['length']),
                     int(pipe['start'][1] + pipe['dir'][1] * pipe['length'])),
                    colors[pipe['color_idx']], 
                    thickness=5)
        
        # Add new pipe occasionally
        state['next_pipe'] -= 1
        if state['next_pipe'] <= 0:
            state['pipes'].append({
                'start': (np.random.randint(0, width), np.random.randint(0, height)),
                'dir': (np.random.rand() * 2 - 1, np.random.rand() * 2 - 1),
                'length': 0,
                'color_idx': np.random.randint(0, len(colors))
            })
            state['next_pipe'] = 20
        
        # Remove old pipes
        state['pipes'] = [p for p in state['pipes'] if p['length'] < max(width, height)]
        
        return img, state

    def render_starfield(self, width, height, frame, colors, speed, state):
        """Render starfield screensaver"""
        if 'stars' not in state:
            state['stars'] = []
            for _ in range(100):
                state['stars'].append({
                    'x': np.random.randint(0, width),
                    'y': np.random.randint(0, height),
                    'z': np.random.randint(1, 100)
                })
        
        img = np.zeros((height, width, 3), dtype=np.uint8)
        
        for star in state['stars']:
            # Update z position
            star['z'] -= speed
            if star['z'] <= 0:
                star['x'] = np.random.randint(0, width)
                star['y'] = np.random.randint(0, height)
                star['z'] = 100
            
            # Project star position
            size = int(1 + (100 - star['z']) / 20)
            color_idx = min(len(colors)-1, size-1)
            cv2.circle(img, (int(star['x']), int(star['y'])), size, colors[color_idx], -1)
        
        return img, state

    def render_matrix(self, width, height, frame, colors, speed, state):
        """Render Matrix-style falling characters"""
        if 'streams' not in state:
            state['streams'] = []
            state['next_stream'] = 0
        
        img = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Update existing streams
        for stream in state['streams']:
            pos = stream['pos']
            for i, char in enumerate(stream['chars']):
                y = int(pos + i * 20)
                if 0 <= y < height:
                    color_intensity = 255 - i * 20
                    if color_intensity > 0:
                        cv2.putText(img, char, (stream['x'], y), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                  (0, color_intensity, 0), 1)
            stream['pos'] += speed * 5
        
        # Add new stream
        state['next_stream'] -= 1
        if state['next_stream'] <= 0:
            chars = [chr(np.random.randint(33, 127)) for _ in range(10)]
            state['streams'].append({
                'x': np.random.randint(0, width),
                'pos': 0,
                'chars': chars
            })
            state['next_stream'] = 10
        
        # Remove old streams
        state['streams'] = [s for s in state['streams'] if s['pos'] < height + 200]
        
        return img, state

    def render_bounce(self, width, height, frame, colors, speed, state):
        """Render bouncing shapes screensaver"""
        if 'shapes' not in state:
            state['shapes'] = []
            for _ in range(5):
                state['shapes'].append({
                    'pos': np.array([np.random.randint(0, width), 
                                   np.random.randint(0, height)], dtype=np.float64),
                    'vel': np.array([np.random.rand() * 10 - 5, 
                                   np.random.rand() * 10 - 5]) * speed,
                    'size': np.random.randint(20, 50),
                    'color_idx': np.random.randint(0, len(colors))
                })
        
        img = np.zeros((height, width, 3), dtype=np.uint8)
        
        for shape in state['shapes']:
            # Update position
            shape['pos'] += shape['vel']
            
            # Bounce off walls
            if shape['pos'][0] < 0 or shape['pos'][0] > width:
                shape['vel'][0] *= -1
            if shape['pos'][1] < 0 or shape['pos'][1] > height:
                shape['vel'][1] *= -1
            
            # Draw shape
            cv2.circle(img, 
                      (int(shape['pos'][0]), int(shape['pos'][1])), 
                      shape['size'], 
                      colors[shape['color_idx']], 
                      -1)
        
        return img, state

    def render_plasma(self, width, height, frame, colors, speed, state):
        """Render plasma effect screensaver"""
        if 'time' not in state:
            state['time'] = 0
        
        img = np.zeros((height, width, 3), dtype=np.uint8)
        x = np.linspace(0, 1, width)
        y = np.linspace(0, 1, height)
        X, Y = np.meshgrid(x, y)
        
        # Generate plasma effect
        plasma = (np.sin(X * 10 + state['time'] * speed) + 
                 np.sin(Y * 10 + state['time'] * speed) + 
                 np.sin(np.sqrt((X-0.5)**2 + (Y-0.5)**2) * 20) +
                 np.sin(np.sqrt(X**2 + Y**2) * 10)) / 4
        
        # Map plasma values to colors
        plasma = ((plasma + 1) / 2 * (len(colors)-1)).astype(int)
        for i in range(len(colors)):
            mask = plasma == i
            img[mask] = colors[i]
        
        state['time'] += 0.1
        return img, state

    def generate(self, width, height, fps, max_frames, preset, color_scheme, speed):
        """Generate screensaver animation frames"""
        # Get color palette
        color_palette = self.get_color_palette(color_scheme)
        
        # Select render function based on preset
        render_funcs = {
            'pipes': self.render_pipes,
            'starfield': self.render_starfield,
            'matrix': self.render_matrix,
            'bounce': self.render_bounce,
            'plasma': self.render_plasma
        }
        render_func = render_funcs.get(preset)
        
        if not render_func:
            raise ValueError(f"Unknown preset: {preset}")
        
        # Generate frames
        frames = []
        state = {}
        
        for i in range(max_frames):
            # Render frame
            frame, state = render_func(width, height, i, color_palette, speed, state)
            
            # Convert to tensor
            frame_tensor = torch.from_numpy(frame).float() / 255.0
            frames.append(frame_tensor)
        
        # Stack frames into batch
        return (torch.stack(frames),)

NODE_CLASS_MAPPINGS = {
    "ScreensaverGenerator": ScreensaverGenerator
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ScreensaverGenerator": "🖥️ Screensaver Generator"
}
