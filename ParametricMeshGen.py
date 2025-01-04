"""
@author: DJZ-Nodes
Parametric Mesh Generator - A node that generates 3D parametric meshes and their previews
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import torch
from datetime import datetime
import os

class ParametricMeshGen:
    """A ComfyUI node that generates parametric 3D meshes"""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "resolution": ("INT", {"default": 30, "min": 10, "max": 100}),
                "scale": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 10.0}),
                "amplitude": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 2.0}),
                "frequency": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 5.0}),
                "phase": ("FLOAT", {"default": 0.0, "min": -3.14159, "max": 3.14159}),
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
                v1 = i + j * width
                v2 = i + (j + 1) * width
                v3 = i + j * width + 1
                v4 = i + (j + 1) * width + 1
                faces.append([v1, v2, v3])
                faces.append([v2, v4, v3])
        return faces

    def save_to_obj(self, filepath, vertices, faces):
        with open(filepath, "w") as file:
            for vertex in vertices:
                file.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")
            for face in faces:
                # OBJ format uses 1-based indices
                file.write(f"f {face[0]+1} {face[1]+1} {face[2]+1}\n")

    def create_preview_image(self, x, y, z):
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(x, y, z, color='cyan', edgecolor='black', alpha=0.8)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
        ax.view_init(elev=30, azim=45)
        
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

    def generate_mesh(self, resolution, scale, amplitude, frequency, phase):
        # Create ComfyUI OBJ output directory if it doesn't exist
        output_dir = os.path.join(os.path.dirname(__file__), "..", "..", "output", "OBJ")
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate unique filename for OBJ
        obj_filename = self.generate_unique_filename(base="parametric_model", ext="obj")
        obj_path = os.path.join(output_dir, obj_filename)
        
        # Generate parametric surface
        u = np.linspace(0, 2 * np.pi, resolution)
        v = np.linspace(0, np.pi, resolution)
        u, v = np.meshgrid(u, v)

        # Parametric equations
        x = scale * (np.sin(v) * np.cos(u))
        y = scale * (np.sin(v) * np.sin(u))
        z = scale * (np.cos(v) + amplitude * np.sin(frequency * u + phase))

        # Generate mesh data
        vertices = np.vstack([x.flatten(), y.flatten(), z.flatten()]).T
        faces = self.generate_faces(resolution, resolution)

        # Save OBJ file
        self.save_to_obj(obj_path, vertices, faces)
        
        # Generate preview image
        preview_tensor = self.create_preview_image(x, y, z)
        
        return (preview_tensor, obj_path)

# Node registration for ComfyUI
NODE_CLASS_MAPPINGS = {
    "ParametricMeshGen": ParametricMeshGen
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ParametricMeshGen": "Parametric Mesh Generator"
}
