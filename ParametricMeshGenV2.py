"""
@author: DJZ-Nodes
Parametric Mesh Generator V2 - An enhanced node that generates 3D parametric meshes with advanced controls
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import torch
from datetime import datetime
import os

class ParametricMeshGenV2:
    """A ComfyUI node that generates parametric 3D meshes with enhanced controls"""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "surface_type": (["SPHERE", "TORUS", "KLEIN_BOTTLE", "MOBIUS"], {"default": "SPHERE"}),
                "resolution": ("INT", {"default": 30, "min": 10, "max": 200}),
                "scale": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 10.0}),
                # Primary wave
                "amplitude": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 2.0}),
                "frequency": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 5.0}),
                "phase": ("FLOAT", {"default": 0.0, "min": -3.14159, "max": 3.14159}),
                # Secondary wave for complex deformations
                "secondary_amplitude": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 2.0}),
                "secondary_frequency": ("FLOAT", {"default": 2.0, "min": 0.1, "max": 5.0}),
                "secondary_phase": ("FLOAT", {"default": 0.0, "min": -3.14159, "max": 3.14159}),
                # Surface properties
                "smoothness": ("INT", {"default": 1, "min": 0, "max": 3}),
                "twist": ("FLOAT", {"default": 0.0, "min": -2.0, "max": 2.0}),
                # Preview settings
                "preview_elevation": ("INT", {"default": 30, "min": 0, "max": 90}),
                "preview_azimuth": ("INT", {"default": 45, "min": 0, "max": 360}),
                "mesh_color": (["CYAN", "RED", "GREEN", "BLUE", "PURPLE", "ORANGE"], {"default": "CYAN"}),
                "edge_visibility": ("FLOAT", {"default": 0.3, "min": 0.0, "max": 1.0}),
            }
        }
    
    RETURN_TYPES = ("IMAGE", "STRING",)
    RETURN_NAMES = ("preview_image", "obj_path",)
    FUNCTION = "generate_mesh"
    CATEGORY = "DJZ-Nodes"

    def generate_unique_filename(self, base="model", ext=""):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"{base}_{timestamp}.{ext}"

    def generate_faces(self, width, height):
        faces = []
        for i in range(height - 1):
            for j in range(width - 1):
                # Calculate vertex indices correctly based on grid position
                v1 = i * width + j           # Current vertex
                v2 = i * width + (j + 1)     # Right vertex
                v3 = (i + 1) * width + j     # Bottom vertex
                v4 = (i + 1) * width + (j + 1) # Bottom-right vertex
                
                # Create two triangles for each quad
                faces.append([v1, v2, v4])  # Upper triangle
                faces.append([v1, v4, v3])  # Lower triangle
        return faces

    def save_to_obj(self, filepath, vertices, faces, smoothness=1):
        with open(filepath, "w") as file:
            # Write vertices
            for vertex in vertices:
                file.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")
            
            # Write smoothing group if enabled
            if smoothness > 0:
                file.write(f"s {smoothness}\n")
            
            # Write faces
            for face in faces:
                file.write(f"f {face[0]+1} {face[1]+1} {face[2]+1}\n")

    def get_color_map(self, color_name):
        color_maps = {
            "CYAN": (0, 0.8, 0.8),
            "RED": (0.8, 0, 0),
            "GREEN": (0, 0.8, 0),
            "BLUE": (0, 0, 0.8),
            "PURPLE": (0.5, 0, 0.5),
            "ORANGE": (1.0, 0.5, 0)
        }
        return color_maps.get(color_name, (0, 0.8, 0.8))

    def create_preview_image(self, x, y, z, elevation, azimuth, mesh_color, edge_visibility):
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        color = self.get_color_map(mesh_color)
        ax.plot_surface(x, y, z, color=color, edgecolor='black', alpha=0.8, linewidth=edge_visibility)
        
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
        ax.view_init(elev=elevation, azim=azimuth)
        
        # Save to memory buffer
        import io
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
        plt.close(fig)
        
        # Convert to PIL Image
        from PIL import Image
        buf.seek(0)
        image = Image.open(buf)
        
        # Convert PIL image to tensor
        image_np = np.array(image).astype(np.float32) / 255.0
        if len(image_np.shape) == 2:  # Grayscale
            image_np = np.stack([image_np, image_np, image_np], axis=2)
        elif image_np.shape[2] == 4:  # RGBA
            image_np = image_np[:, :, :3]  # Remove alpha channel
            
        # Convert to PyTorch tensor (B,H,W,C)
        image_tensor = torch.from_numpy(image_np).unsqueeze(0)
        
        return image_tensor

    def generate_parametric_surface(self, surface_type, u, v, scale, amplitude, frequency, phase,
                                  secondary_amplitude, secondary_frequency, secondary_phase, twist):
        if surface_type == "SPHERE":
            x = scale * (np.sin(v) * np.cos(u))
            y = scale * (np.sin(v) * np.sin(u))
            z = scale * (np.cos(v) + amplitude * np.sin(frequency * u + phase) +
                        secondary_amplitude * np.sin(secondary_frequency * v + secondary_phase))
            
            # Apply twist
            if twist != 0:
                angle = twist * v
                x_new = x * np.cos(angle) - y * np.sin(angle)
                y_new = x * np.sin(angle) + y * np.cos(angle)
                x, y = x_new, y_new
                
        elif surface_type == "TORUS":
            R = scale  # Major radius
            r = scale * 0.3  # Minor radius
            x = (R + r * np.cos(v)) * np.cos(u)
            y = (R + r * np.cos(v)) * np.sin(u)
            z = r * np.sin(v) + amplitude * np.sin(frequency * u + phase) + \
                secondary_amplitude * np.sin(secondary_frequency * v + secondary_phase)
                
        elif surface_type == "KLEIN_BOTTLE":
            # Improved Klein bottle parametric equations
            r = 4  # Major radius
            a = 2  # Minor radius
            n = 4  # Number of lobes for better visualization
            
            # Pre-calculate trigonometric values
            cos_u = np.cos(u)
            sin_u = np.sin(u)
            cos_v = np.cos(v)
            sin_v = np.sin(v)
            cos_nu = np.cos(n*u)
            sin_nu = np.sin(n*u)
            
            # Calculate the characteristic Klein bottle shape
            c = 0.5 * (1 - cos_u/2)  # Transition factor
            
            # Base shape
            x = scale * ((r + a*cos_v)*cos_u * (1 - c) + a*cos_v*cos_nu * c)
            y = scale * ((r + a*cos_v)*sin_u * (1 - c) + a*cos_v*sin_nu * c)
            z = scale * (a * sin_v + 2 * a * sin_u * c)
            
            # Add wave deformations
            x += scale * amplitude * np.sin(frequency * u + phase) * cos_v
            y += scale * amplitude * np.sin(frequency * u + phase) * sin_v
            z += scale * amplitude * np.cos(frequency * u + phase)
            
        else:  # MOBIUS
            # Parametric equations for Möbius strip
            u = u / 2  # Adjust range for Möbius strip
            x = scale * (1 + v/2 * np.cos(u/2)) * np.cos(u)
            y = scale * (1 + v/2 * np.cos(u/2)) * np.sin(u)
            z = scale * v/2 * np.sin(u/2) + amplitude * np.sin(frequency * u + phase)

        return x, y, z

    def generate_mesh(self, surface_type, resolution, scale, amplitude, frequency, phase,
                     secondary_amplitude, secondary_frequency, secondary_phase, smoothness,
                     twist, preview_elevation, preview_azimuth, mesh_color, edge_visibility):
        # Create ComfyUI OBJ output directory if it doesn't exist
        output_dir = os.path.join(os.path.dirname(__file__), "..", "..", "output", "OBJ")
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate unique filename for OBJ
        obj_filename = self.generate_unique_filename(base=f"parametric_{surface_type.lower()}", ext="obj")
        obj_path = os.path.join(output_dir, obj_filename)
        
        # Generate parameter ranges based on surface type
        if surface_type == "MOBIUS":
            u = np.linspace(0, 2 * np.pi, resolution)
            v = np.linspace(-1, 1, resolution)  # Möbius strip needs different v range
        elif surface_type == "KLEIN_BOTTLE":
            u = np.linspace(0, 2 * np.pi, resolution)
            v = np.linspace(0, 2 * np.pi, resolution)  # Klein bottle needs full range
        else:  # SPHERE and TORUS
            u = np.linspace(0, 2 * np.pi, resolution)
            v = np.linspace(0, 2 * np.pi, resolution)
        
        u, v = np.meshgrid(u, v)

        # Generate surface based on type
        x, y, z = self.generate_parametric_surface(
            surface_type, u, v, scale, amplitude, frequency, phase,
            secondary_amplitude, secondary_frequency, secondary_phase, twist
        )

        # Generate mesh data
        vertices = np.vstack([x.flatten(), y.flatten(), z.flatten()]).T
        faces = self.generate_faces(resolution, resolution)

        # Save OBJ file
        self.save_to_obj(obj_path, vertices, faces, smoothness)
        
        # Generate preview image
        preview_tensor = self.create_preview_image(
            x, y, z, preview_elevation, preview_azimuth, mesh_color, edge_visibility
        )
        
        return (preview_tensor, obj_path)

# Node registration for ComfyUI
NODE_CLASS_MAPPINGS = {
    "ParametricMeshGenV2": ParametricMeshGenV2
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ParametricMeshGenV2": "Parametric Mesh Generator V2"
}
