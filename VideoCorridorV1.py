import numpy as np
import torch
import cv2
import colorsys
from math import sin, cos, pi

class VideoCorridorV1:
    def __init__(self):
        self.type = "VideoCorridorV1"
        self.output_type = "IMAGE"
        self.output_dims = 3
        self.compatible_decorators = ["RepeatDecorator", "LoopDecorator"]
        self.required_extensions = []
        self.category = "Video/Animation"
        self.name = "🌀 Infinite Corridor Generator"
        self.description = "Generates infinite corridor video sequences with perspective effects"

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
                "corridor_depth": ("FLOAT", {
                    "default": 2.0,
                    "min": 0.5,
                    "max": 5.0,
                    "step": 0.1
                }),
                "movement_speed": ("FLOAT", {
                    "default": 0.05,
                    "min": 0.01,
                    "max": 0.2,
                    "step": 0.01
                }),
                "color_scheme": (["neon", "classic", "rainbow", "monochrome", "sunset", "cyberpunk"],),
                "wall_pattern": (["solid", "gradient", "grid", "diagonal"],),
                "lighting_mode": (["dynamic", "static", "pulsing", "ambient"],),
                "perspective_strength": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.5,
                    "max": 2.0,
                    "step": 0.1
                })
            }
        }

    def get_color_palette(self, scheme):
        """Define color palettes for different schemes"""
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

    def apply_wall_pattern(self, img, corners, pattern, color, frame):
        """Apply different wall patterns to the corridor"""
        if pattern == "solid":
            cv2.fillPoly(img, [corners], color)
            
        elif pattern == "gradient":
            steps = 20
            for i in range(steps):
                blend = i / steps
                current_color = tuple(int(c1 + (c2 - c1) * blend) for c1, c2 in zip(color, (255, 255, 255)))
                current_corners = np.array([
                    corners[0] + (corners[1] - corners[0]) * blend,
                    corners[1] + (corners[2] - corners[1]) * blend,
                    corners[2] + (corners[3] - corners[2]) * blend,
                    corners[3] + (corners[0] - corners[3]) * blend
                ], np.int32)
                cv2.fillPoly(img, [current_corners], current_color)
                
        elif pattern == "grid":
            cv2.fillPoly(img, [corners], color)
            grid_size = 30
            for i in range(0, img.shape[1], grid_size):
                cv2.line(img, (i, 0), (i, img.shape[0]), (0, 0, 0), 1)
            for i in range(0, img.shape[0], grid_size):
                cv2.line(img, (0, i), (img.shape[1], i), (0, 0, 0), 1)
                
        elif pattern == "diagonal":
            cv2.fillPoly(img, [corners], color)
            spacing = 30
            for i in range(-img.shape[0], img.shape[1], spacing):
                start_point = (i, 0)
                end_point = (i + img.shape[0], img.shape[0])
                cv2.line(img, start_point, end_point, (0, 0, 0), 1)

    def apply_lighting(self, color, mode, frame, depth):
        """Apply different lighting effects"""
        if mode == "static":
            return color
            
        elif mode == "dynamic":
            intensity = max(0.4, min(1.0, 1.0 - depth/5.0))
            return tuple(int(c * intensity) for c in color)
            
        elif mode == "pulsing":
            pulse = (sin(frame * 0.1) + 1) * 0.3 + 0.4
            return tuple(int(c * pulse) for c in color)
            
        elif mode == "ambient":
            ambient = 0.3
            return tuple(int(c * ambient + (255 - c) * 0.1) for c in color)
            
        return color

    def create_corridor_frame(self, width, height, frame, params):
        """Generate a single frame of the corridor"""
        img = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Calculate vanishing point
        vanishing_point = (width // 2, height // 2)
        
        # Calculate depth offset based on frame
        depth_offset = (frame * params["movement_speed"]) % 1.0
        
        # Get base color
        colors = self.get_color_palette(params["color_scheme"])
        color_idx = int(depth_offset * (len(colors) - 1))
        base_color = colors[color_idx]
        
        # Apply lighting
        color = self.apply_lighting(base_color, 
                                  params["lighting_mode"],
                                  frame,
                                  depth_offset)
        
        # Calculate corridor corners with perspective
        perspective = params["perspective_strength"]
        depth = params["corridor_depth"]
        
        scale = (0.1 + depth_offset * depth) * perspective
        corridor_width = width * scale
        corridor_height = height * scale
        
        corners = np.array([
            # Near points
            [int(width * 0.1), int(height * 0.1)],
            [int(width * 0.9), int(height * 0.1)],
            [int(width * 0.9), int(height * 0.9)],
            [int(width * 0.1), int(height * 0.9)],
            
            # Far points (towards vanishing point)
            [int(vanishing_point[0] - corridor_width/2), int(vanishing_point[1] - corridor_height/2)],
            [int(vanishing_point[0] + corridor_width/2), int(vanishing_point[1] - corridor_height/2)],
            [int(vanishing_point[0] + corridor_width/2), int(vanishing_point[1] + corridor_height/2)],
            [int(vanishing_point[0] - corridor_width/2), int(vanishing_point[1] + corridor_height/2)]
        ], np.int32)
        
        # Draw walls
        for i in range(4):  # Draw four walls (left, right, top, bottom)
            wall_corners = np.array([
                corners[i],
                corners[(i+1)%4],
                corners[i+4],
                corners[((i+1)%4)+4]
            ], np.int32)
            
            self.apply_wall_pattern(img, wall_corners, params["wall_pattern"], color, frame)
        
        return img

    def generate(self, width, height, fps, max_frames, corridor_depth, movement_speed, 
                color_scheme, wall_pattern, lighting_mode, perspective_strength):
        """Generate video frames"""
        frames = []
        params = {
            "corridor_depth": corridor_depth,
            "movement_speed": movement_speed,
            "color_scheme": color_scheme,
            "wall_pattern": wall_pattern,
            "lighting_mode": lighting_mode,
            "perspective_strength": perspective_strength
        }
        
        for i in range(max_frames):
            frame = self.create_corridor_frame(width, height, i, params)
            frame_tensor = torch.from_numpy(frame).float() / 255.0
            frames.append(frame_tensor)
        
        return (torch.stack(frames),)

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    FUNCTION = "generate"

NODE_CLASS_MAPPINGS = {
    "VideoCorridorV1": VideoCorridorV1
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VideoCorridorV1": "🌀 Infinite Corridor Generator"
}