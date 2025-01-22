import numpy as np
import torch
import cv2
import colorsys
from math import sin, cos, pi, tan

class VideoMazeV2:
    def __init__(self):
        self.type = "VideoMazeV2"
        self.output_type = "IMAGE"
        self.output_dims = 3
        self.compatible_decorators = ["RepeatDecorator", "LoopDecorator"]
        self.required_extensions = []
        self.category = "Video/Animation"
        self.name = "🌀 Video Maze Generator V2"
        self.description = "Generates infinite 3D maze video sequences with enhanced visuals and deterministic generation"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "width": ("INT", {
                    "default": 512,
                    "min": 128,
                    "max": 4096,
                    "step": 64
                }),
                "height": ("INT", {
                    "default": 512,
                    "min": 128,
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
                    "default": 300,
                    "min": 1,
                    "max": 9999,
                    "step": 1
                }),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 0xffffffff
                }),
                "maze_size": ("INT", {
                    "default": 30,
                    "min": 15,
                    "max": 100,
                    "step": 5
                }),
                "wall_height": ("FLOAT", {
                    "default": 0.8,
                    "min": 0.5,
                    "max": 3.0,
                    "step": 0.1
                }),
                "wall_thickness": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 5,
                    "step": 1
                }),
                "camera_height": ("FLOAT", {
                    "default": 0.3,
                    "min": 0.1,
                    "max": 1.0,
                    "step": 0.1
                }),
                "fog_distance": ("FLOAT", {
                    "default": 20.0,
                    "min": 5.0,
                    "max": 50.0,
                    "step": 1.0
                }),
                "fov": ("FLOAT", {
                    "default": 75.0,
                    "min": 30.0,
                    "max": 120.0,
                    "step": 5.0
                }),
                "movement_speed": ("FLOAT", {
                    "default": 0.05,
                    "min": 0.01,
                    "max": 0.2,
                    "step": 0.01
                }),
                "rotation_speed": ("FLOAT", {
                    "default": 0.03,
                    "min": 0.01,
                    "max": 0.15,
                    "step": 0.01
                }),
                "color_scheme": (["neon", "classic", "rainbow", "monochrome", "sunset", "cyberpunk"],),
                "wall_pattern": (["solid", "gradient", "brick", "circuit"],),
                "lighting_mode": (["dynamic", "static", "pulsing", "ambient"],),
                "render_quality": (["standard", "high", "ultra"],),
                "ceiling_color": ("STRING", {
                    "default": "#000000",
                    "multiline": False
                }),
                "floor_color": ("STRING", {
                    "default": "#000000",
                    "multiline": False
                }),
                "camera_pitch": ("FLOAT", {
                    "default": 0.0,
                    "min": -45.0,
                    "max": 45.0,
                    "step": 1.0
                })
            }
        }

    def get_color_palette(self, scheme):
        """Enhanced color palettes with more variety"""
        palettes = {
            "neon": [
                (255, 0, 255), (0, 255, 255), (255, 255, 0),
                (255, 0, 128), (128, 0, 255), (0, 255, 128)
            ],
            "classic": [
                (0, 0, 255), (0, 255, 255), (0, 255, 0),
                (255, 255, 0), (255, 128, 0), (255, 0, 0)
            ],
            "rainbow": [
                tuple(int(c * 255) for c in colorsys.hsv_to_rgb(h/6, 1.0, 1.0))
                for h in range(7)
            ],
            "monochrome": [
                (i, i, i) for i in [255, 220, 180, 140, 100, 60]
            ],
            "sunset": [
                (255, 100, 0), (255, 50, 0), (255, 0, 50),
                (200, 0, 100), (150, 0, 150), (100, 0, 200)
            ],
            "cyberpunk": [
                (255, 0, 128), (0, 255, 255), (255, 255, 0),
                (128, 0, 255), (255, 0, 255), (0, 255, 128)
            ]
        }
        return palettes.get(scheme, palettes["neon"])

    def apply_wall_pattern(self, img, x, wall_top, wall_height, color, pattern, frame, thickness):
        """Apply different wall patterns with customizable thickness"""
        if pattern == "solid":
            cv2.line(img, (int(x), int(wall_top)), (int(x), int(wall_top + wall_height)), color, thickness)
        elif pattern == "gradient":
            for y in range(wall_top, wall_top + wall_height):
                blend = (y - wall_top) / wall_height
                c = tuple(int(c1 + (c2 - c1) * blend) for c1, c2 in zip(color, (255, 255, 255)))
                cv2.line(img, (int(x), int(y)), (int(x), int(y+1)), c, thickness)
        elif pattern == "brick":
            brick_height = 20
            for y in range(wall_top, wall_top + wall_height, brick_height):
                offset = (x // brick_height + frame) % 2 * (brick_height // 2)
                y_pos = y + offset
                cv2.line(img, (int(x), int(y_pos)), (int(x), int(min(y_pos + brick_height, wall_top + wall_height))), color, thickness)
        elif pattern == "circuit":
            circuit_height = 30
            y_offset = (frame * 2) % circuit_height
            for y in range(wall_top, wall_top + wall_height, circuit_height):
                y_pos = y + y_offset
                cv2.line(img, (int(x), int(y_pos)), (int(x), int(min(y_pos + circuit_height//2, wall_top + wall_height))), color, thickness)

    def apply_lighting(self, color, mode, frame, dist, fog_distance):
        """Apply different lighting effects with fog"""
        base_color = list(color)
        
        # Apply fog effect
        fog_factor = min(1.0, dist / fog_distance)
        fog_color = (128, 128, 128)  # Neutral gray fog
        base_color = [int(c * (1 - fog_factor) + fog_color[i] * fog_factor) for i, c in enumerate(base_color)]
        
        if mode == "static":
            return tuple(base_color)
        elif mode == "dynamic":
            intensity = max(0.4, min(1.0, 1.0 - dist/20.0))
            return tuple(int(c * intensity) for c in base_color)
        elif mode == "pulsing":
            pulse = (sin(frame * 0.1) + 1) * 0.3 + 0.4
            return tuple(int(c * pulse) for c in base_color)
        elif mode == "ambient":
            ambient = 0.3
            return tuple(int(c * ambient + (255 - c) * 0.1) for c in base_color)
        return tuple(base_color)

    def generate_enhanced_maze(self, size, seed):
        """Generate deterministic maze using seed"""
        # Set random seed for reproducibility
        rng = np.random.RandomState(seed)
        maze = np.ones((size, size), dtype=np.uint8)
        
        def carve_path(x, y):
            maze[y, x] = 0
            directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
            rng.shuffle(directions)
            
            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy
                if (0 <= new_x < size and 0 <= new_y < size and 
                    maze[new_y, new_x] == 1):
                    if rng.random() < 0.15:
                        maze[y + dy//2, x + dx//2] = 2
                    else:
                        maze[y + dy//2, x + dx//2] = 0
                    carve_path(new_x, new_y)
        
        carve_path(1, 1)
        return maze

    def cast_enhanced_ray(self, maze, pos_x, pos_y, angle, max_depth, quality):
        """Enhanced ray casting with quality settings"""
        ray_x = cos(angle)
        ray_y = sin(angle)
        
        step_size = {"standard": 1.0, "high": 0.5, "ultra": 0.25}[quality]
        max_steps = int(max_depth / step_size)
        
        dist = 0.0
        for _ in range(max_steps):
            check_x = pos_x + ray_x * dist
            check_y = pos_y + ray_y * dist
            
            map_x = int(check_x)
            map_y = int(check_y)
            
            if (map_x < 0 or map_x >= maze.shape[1] or 
                map_y < 0 or map_y >= maze.shape[0]):
                break
                
            if maze[map_y, map_x] == 1:
                break
                
            dist += step_size
            
        return dist

    def hex_to_rgb(self, hex_color):
        """Convert hex color string to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def render_frame(self, width, height, frame, state, params):
        """Render a single enhanced frame"""
        img = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Initialize or update maze if needed
        if state['maze'] is None or state['maze_size'] != params['maze_size']:
            state['maze'] = self.generate_enhanced_maze(params['maze_size'], params['seed'])
            state['maze_size'] = params['maze_size']
            state['pos_x'] = 1.5
            state['pos_y'] = 1.5
        
        # Get color palette
        colors = self.get_color_palette(params['color_scheme'])
        
        # Update position with collision detection
        new_x = state['pos_x'] + cos(state['angle']) * params['movement_speed']
        new_y = state['pos_y'] + sin(state['angle']) * params['movement_speed']
        
        # Enhanced collision detection with sliding
        if (state['maze'][int(new_y), int(new_x)] == 1):
            if state['maze'][int(state['pos_y']), int(new_x)] != 1:
                new_y = state['pos_y']
            elif state['maze'][int(new_y), int(state['pos_x'])] != 1:
                new_x = state['pos_x']
            else:
                state['angle'] += pi
        
        state['pos_x'] = new_x
        state['pos_y'] = new_y
        state['angle'] += params['rotation_speed']
        
        # Ray casting with enhanced quality
        fov = params['fov'] * pi / 180.0
        for x in range(width):
            ray_angle = (state['angle'] - fov/2.0) + (x / float(width)) * fov
            dist = self.cast_enhanced_ray(state['maze'], 
                                        state['pos_x'], 
                                        state['pos_y'],
                                        ray_angle,
                                        params['fog_distance'],
                                        params['render_quality'])
            
            # Enhanced wall rendering with camera height and pitch
            pitch_angle = params['camera_pitch'] * pi / 180.0
            
            # Adjust wall height based on distance and pitch
            wall_height_base = height * params['wall_height']
            wall_height_adj = wall_height_base / (dist + 0.0001)
            wall_height = min(int(wall_height_adj * cos(pitch_angle)), height)
            
            # Calculate wall position with proper perspective
            camera_height_offset = height * params['camera_height']
            pitch_offset = int(height * sin(pitch_angle) * 0.5)  # Pitch affects vertical position
            perspective_offset = int(wall_height * tan(pitch_angle) * 0.25)  # Perspective correction
            
            # Combine all offsets for final wall position
            wall_center = height // 2 + camera_height_offset
            wall_top = wall_center - (wall_height // 2) + pitch_offset + perspective_offset
            
            # Get base color
            color_idx = int((dist / params['fog_distance']) * (len(colors) - 1))
            color_idx = max(0, min(color_idx, len(colors) - 1))
            base_color = colors[color_idx]
            
            # Apply lighting and fog effects
            final_color = self.apply_lighting(base_color, 
                                           params['lighting_mode'],
                                           frame,
                                           dist,
                                           params['fog_distance'])
            
            # Draw wall with pattern and thickness
            self.apply_wall_pattern(img,
                                  x,
                                  wall_top,
                                  wall_height,
                                  final_color,
                                  params['wall_pattern'],
                                  frame,
                                  params['wall_thickness'])
            
            # Use hex colors for ceiling and floor
            ceiling_color = self.hex_to_rgb(params['ceiling_color'])
            floor_color = self.hex_to_rgb(params['floor_color'])
            
            cv2.line(img, (int(x), 0), (int(x), int(wall_top)), ceiling_color, params['wall_thickness'])
            cv2.line(img, (int(x), int(wall_top + wall_height)), (int(x), height), floor_color, params['wall_thickness'])
        
        return img, state

    def generate(self, width, height, fps, max_frames, seed, **kwargs):
        """Generate video frames with seed control"""
        frames = []
        state = {
            'maze': None,
            'pos_x': 1.5,
            'pos_y': 1.5,
            'angle': 0,
            'maze_size': None
        }
        
        # Set the seed for reproducibility
        np.random.seed(seed)
        
        for i in range(max_frames):
            frame, state = self.render_frame(width, height, i, state, {**kwargs, 'seed': seed})
            frame_tensor = torch.from_numpy(frame).float() / 255.0
            frames.append(frame_tensor)
        
        return (torch.stack(frames),)

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    FUNCTION = "generate"

NODE_CLASS_MAPPINGS = {
    "VideoMazeV2": VideoMazeV2
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VideoMazeV2": "🌀 Video Maze Generator V2"
}
