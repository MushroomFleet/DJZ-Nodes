import numpy as np
import torch
import cv2
import colorsys
from math import sin, cos, pi

class VideoMazeV1:
    def __init__(self):
        self.type = "VideoMazeV1"
        self.output_type = "IMAGE"
        self.output_dims = 3
        self.compatible_decorators = ["RepeatDecorator", "LoopDecorator"]
        self.required_extensions = []
        self.category = "Video/Animation"
        self.name = "🌀 Video Maze Generator"
        self.description = "Generates infinite 3D maze video sequences with enhanced visuals"

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
                "maze_size": ("INT", {
                    "default": 30,
                    "min": 15,
                    "max": 100,
                    "step": 5
                }),
                "wall_height": ("FLOAT", {
                    "default": 1.2,
                    "min": 0.5,
                    "max": 3.0,
                    "step": 0.1
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
                "render_quality": (["standard", "high", "ultra"],)
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

    def apply_wall_pattern(self, img, x, wall_top, wall_height, color, pattern, frame):
        """Apply different wall patterns"""
        if pattern == "solid":
            cv2.line(img, (x, wall_top), (x, wall_top + wall_height), color, 1)
        elif pattern == "gradient":
            for y in range(wall_top, wall_top + wall_height):
                blend = (y - wall_top) / wall_height
                c = tuple(int(c1 + (c2 - c1) * blend) for c1, c2 in zip(color, (255, 255, 255)))
                cv2.line(img, (x, y), (x, y+1), c, 1)
        elif pattern == "brick":
            brick_height = 20
            for y in range(wall_top, wall_top + wall_height, brick_height):
                offset = (x // brick_height + frame) % 2 * (brick_height // 2)
                y_pos = y + offset
                cv2.line(img, (x, y_pos), (x, min(y_pos + brick_height, wall_top + wall_height)), color, 1)
        elif pattern == "circuit":
            circuit_height = 30
            y_offset = (frame * 2) % circuit_height
            for y in range(wall_top, wall_top + wall_height, circuit_height):
                y_pos = y + y_offset
                cv2.line(img, (x, y_pos), (x, min(y_pos + circuit_height//2, wall_top + wall_height)), color, 1)

    def apply_lighting(self, color, mode, frame, dist):
        """Apply different lighting effects"""
        if mode == "static":
            return color
        elif mode == "dynamic":
            intensity = max(0.4, min(1.0, 1.0 - dist/20.0))
            return tuple(int(c * intensity) for c in color)
        elif mode == "pulsing":
            pulse = (sin(frame * 0.1) + 1) * 0.3 + 0.4
            return tuple(int(c * pulse) for c in color)
        elif mode == "ambient":
            ambient = 0.3
            return tuple(int(c * ambient + (255 - c) * 0.1) for c in color)
        return color

    def generate_enhanced_maze(self, size):
        """Generate more complex maze with improved algorithm"""
        maze = np.ones((size, size), dtype=np.uint8)
        
        def carve_path(x, y):
            maze[y, x] = 0
            directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
            np.random.shuffle(directions)
            
            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy
                if (0 <= new_x < size and 0 <= new_y < size and 
                    maze[new_y, new_x] == 1):
                    # Add occasional wider passages
                    if np.random.random() < 0.15:
                        maze[y + dy//2, x + dx//2] = 2  # Special passage marker
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

    def render_frame(self, width, height, frame, state, params):
        """Render a single enhanced frame"""
        img = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Initialize or update maze if needed
        if state['maze'] is None or state['maze_size'] != params['maze_size']:
            state['maze'] = self.generate_enhanced_maze(params['maze_size'])
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
            # Try sliding along walls
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
                                        20.0,
                                        params['render_quality'])
            
            # Enhanced wall rendering
            wall_height = min(int((height * params['wall_height']) / (dist + 0.0001)), height)
            wall_top = (height - wall_height) // 2
            
            # Get base color
            color_idx = int((dist / 20.0) * (len(colors) - 1))
            color_idx = max(0, min(color_idx, len(colors) - 1))
            base_color = colors[color_idx]
            
            # Apply lighting effects
            final_color = self.apply_lighting(base_color, 
                                           params['lighting_mode'],
                                           frame,
                                           dist)
            
            # Draw wall with pattern
            self.apply_wall_pattern(img,
                                  x,
                                  wall_top,
                                  wall_height,
                                  final_color,
                                  params['wall_pattern'],
                                  frame)
            
            # Enhanced ceiling and floor
            ceiling_color = (20, 20, 20)
            floor_color = (40, 40, 40)
            cv2.line(img, (x, 0), (x, wall_top), ceiling_color, 1)
            cv2.line(img, (x, wall_top + wall_height), (x, height), floor_color, 1)
        
        return img, state

    def generate(self, width, height, fps, max_frames, **kwargs):
        """Generate video frames"""
        frames = []
        state = {
            'maze': None,
            'pos_x': 1.5,
            'pos_y': 1.5,
            'angle': 0,
            'maze_size': None
        }
        
        for i in range(max_frames):
            frame, state = self.render_frame(width, height, i, state, kwargs)
            frame_tensor = torch.from_numpy(frame).float() / 255.0
            frames.append(frame_tensor)
        
        return (torch.stack(frames),)

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    FUNCTION = "generate"

NODE_CLASS_MAPPINGS = {
    "VideoMazeV1": VideoMazeV1
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VideoMazeV1": "🌀 Video Maze Generator"
}
