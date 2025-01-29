import numpy as np
import torch
import cv2
from math import sin, cos, pi
import colorsys

class VideoPyramidV1:
    def __init__(self):
        self.type = "VideoPyramidV1"
        self.output_type = "IMAGE"
        self.output_dims = 3
        self.compatible_decorators = ["RepeatDecorator", "LoopDecorator"]
        self.required_extensions = []
        self.category = "Video/Animation"
        self.name = "🎆 Video Pyramid Generator"
        self.description = "Generates 3D rotating pyramid animations with customizable parameters"

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
                    "default": 120,
                    "min": 1,
                    "max": 9999,
                    "step": 1
                }),
                "pyramid_size": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 5.0,
                    "step": 0.1
                }),
                "distance": ("FLOAT", {
                    "default": 5.0,
                    "min": 2.0,
                    "max": 20.0,
                    "step": 0.5
                }),
                "fov": ("FLOAT", {
                    "default": 75.0,
                    "min": 30.0,
                    "max": 120.0,
                    "step": 5.0
                }),
                "rotation_x": ("FLOAT", {
                    "default": 0.02,
                    "min": -0.1,
                    "max": 0.1,
                    "step": 0.01
                }),
                "rotation_y": ("FLOAT", {
                    "default": 0.03,
                    "min": -0.1,
                    "max": 0.1,
                    "step": 0.01
                }),
                "rotation_z": ("FLOAT", {
                    "default": 0.01,
                    "min": -0.1,
                    "max": 0.1,
                    "step": 0.01
                }),
                "color_scheme": (["rainbow", "monochrome", "neon", "pastel", "cyberpunk"],),
                "render_style": (["wireframe", "solid", "points"],),
                "lighting_mode": (["basic", "ambient", "dynamic", "none"],)
            }
        }

    def get_color_palette(self, scheme):
        """Define color palettes for the pyramid faces"""
        palettes = {
            "rainbow": [
                tuple(int(c * 255) for c in colorsys.hsv_to_rgb(h/6, 0.8, 1.0))
                for h in range(6)
            ],
            "monochrome": [
                (i, i, i) for i in [255, 220, 180, 140, 100, 60]
            ],
            "neon": [
                (255, 0, 255), (0, 255, 255), (255, 255, 0),
                (255, 0, 128), (128, 0, 255), (0, 255, 128)
            ],
            "pastel": [
                (255, 182, 193), (176, 224, 230), (255, 218, 185),
                (221, 160, 221), (176, 196, 222), (144, 238, 144)
            ],
            "cyberpunk": [
                (255, 0, 128), (0, 255, 255), (255, 255, 0),
                (128, 0, 255), (255, 0, 255), (0, 255, 128)
            ]
        }
        return palettes.get(scheme, palettes["rainbow"])

    def create_pyramid_vertices(self, size=1.0):
        """Create pyramid vertices"""
        return np.array([
            [-size, -size, 0],  # Base vertices
            [size, -size, 0],
            [size, size, 0],
            [-size, size, 0],
            [0, 0, size]      # Apex
        ], dtype=np.float32)

    def create_pyramid_faces(self):
        """Define pyramid faces for solid rendering"""
        return [
            [0, 1, 4],  # Front face
            [1, 2, 4],  # Right face
            [2, 3, 4],  # Back face
            [3, 0, 4],  # Left face
            [0, 1, 2, 3]  # Base
        ]

    def rotate_points(self, points, angles):
        """Apply 3D rotation to points"""
        rx, ry, rz = angles
        
        # Rotation matrices
        Rx = np.array([
            [1, 0, 0],
            [0, cos(rx), -sin(rx)],
            [0, sin(rx), cos(rx)]
        ])
        
        Ry = np.array([
            [cos(ry), 0, sin(ry)],
            [0, 1, 0],
            [-sin(ry), 0, cos(ry)]
        ])
        
        Rz = np.array([
            [cos(rz), -sin(rz), 0],
            [sin(rz), cos(rz), 0],
            [0, 0, 1]
        ])
        
        # Apply rotations
        points = points @ Rx @ Ry @ Rz
        return points

    def project_points(self, points, width, height, fov, distance):
        """Project 3D points to 2D screen space"""
        f = 1.0 / np.tan(fov * pi / 360)
        
        # Move points away from camera
        points = points + [0, 0, distance]
        
        # Perspective projection
        projected = np.zeros((len(points), 2))
        for i, (x, y, z) in enumerate(points):
            if z != 0:
                projected[i] = [x * f / z, y * f / z]
        
        # Scale to screen space
        projected *= min(width, height) / 2
        projected += [width/2, height/2]
        
        return projected

    def apply_lighting(self, color, mode, normal, light_dir):
        """Apply lighting effects to faces"""
        if mode == "none":
            return color
        
        # Calculate basic diffuse lighting
        intensity = max(0.2, min(1.0, np.dot(normal, light_dir) * 0.7 + 0.3))
        
        if mode == "basic":
            return tuple(int(c * intensity) for c in color)
        elif mode == "ambient":
            ambient = 0.3
            return tuple(int(c * (ambient + intensity * 0.7)) for c in color)
        elif mode == "dynamic":
            specular = pow(max(0, np.dot(normal, light_dir)), 8) * 0.3
            return tuple(min(255, int(c * intensity + specular * 255)) for c in color)
        
        return color

    def render_frame(self, width, height, frame, params):
        """Render a single frame of the pyramid animation"""
        img = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Create pyramid vertices
        vertices = self.create_pyramid_vertices(params['pyramid_size'])
        faces = self.create_pyramid_faces()
        colors = self.get_color_palette(params['color_scheme'])
        
        # Calculate rotation angles for this frame
        angles = [
            frame * params['rotation_x'],
            frame * params['rotation_y'],
            frame * params['rotation_z']
        ]
        
        # Rotate vertices
        rotated = self.rotate_points(vertices, angles)
        
        # Project to 2D
        projected = self.project_points(
            rotated, width, height, 
            params['fov'], params['distance']
        )
        
        # Define light direction (pointing slightly down and to the right)
        light_dir = np.array([0.5, -0.5, -1.0])
        light_dir = light_dir / np.linalg.norm(light_dir)
        
        if params['render_style'] == 'wireframe':
            # Draw edges
            edges = [(0,1), (1,2), (2,3), (3,0),
                    (0,4), (1,4), (2,4), (3,4)]
            
            for edge in edges:
                pt1 = tuple(map(int, projected[edge[0]]))
                pt2 = tuple(map(int, projected[edge[1]]))
                cv2.line(img, pt1, pt2, colors[0], 2)
        
        elif params['render_style'] == 'solid':
            # Calculate face depths for sorting
            face_depths = []
            for i, face in enumerate(faces):
                if len(face) == 3:
                    z_depth = np.mean(rotated[face][:, 2])
                    face_depths.append((z_depth, i))
            
            # Sort faces by depth (painter's algorithm)
            for _, face_idx in sorted(face_depths, reverse=True):
                face = faces[face_idx]
                if len(face) == 3:
                    pts = np.array([projected[i] for i in face], np.int32)
                    
                    # Calculate face normal for lighting
                    v1 = rotated[face[1]] - rotated[face[0]]
                    v2 = rotated[face[2]] - rotated[face[0]]
                    normal = np.cross(v1, v2)
                    normal = normal / np.linalg.norm(normal)
                    
                    # Apply lighting to face color
                    color = self.apply_lighting(
                        colors[face_idx % len(colors)],
                        params['lighting_mode'],
                        normal,
                        light_dir
                    )
                    
                    cv2.fillPoly(img, [pts], color)
        
        else:  # points
            for i, pt in enumerate(projected):
                cv2.circle(img, tuple(map(int, pt)), 4, colors[i % len(colors)], -1)
        
        return img

    def generate(self, width, height, fps, max_frames, **kwargs):
        """Generate video frames"""
        frames = []
        
        for i in range(max_frames):
            frame = self.render_frame(width, height, i, kwargs)
            frame_tensor = torch.from_numpy(frame).float() / 255.0
            frames.append(frame_tensor)
        
        return (torch.stack(frames),)

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    FUNCTION = "generate"

NODE_CLASS_MAPPINGS = {
    "VideoPyramidV1": VideoPyramidV1
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VideoPyramidV1": "🎆 Video Pyramid Generator"
}
