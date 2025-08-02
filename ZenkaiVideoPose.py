import os
from PIL import Image
import numpy as np
import torch

class ZenkaiVideoPose:
    @classmethod
    def INPUT_TYPES(cls):
        # Determine the path to the posemaps folder relative to this file
        posemaps_folder = os.path.join(os.path.dirname(__file__), "posemaps")
        # List subdirectories in the posemaps folder
        subfolders = [d for d in os.listdir(posemaps_folder) if os.path.isdir(os.path.join(posemaps_folder, d))]
        
        return {
            "required": {
                "pose_folder": (subfolders,),
                "max_frames": ("INT", {
                    "default": 30,
                    "min": 1,
                    "max": 1000
                })
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "load_pose_sequence"
    CATEGORY = "DJZ-Nodes"

    def load_pose_sequence(self, pose_folder, max_frames):
        # Build absolute path to the selected subfolder under posemaps
        folder_path = os.path.join(os.path.dirname(__file__), "posemaps", pose_folder)
        # Allowed image extensions
        allowed_extensions = (".jpeg", ".jpg", ".png")
        # List all allowed image files in the selected folder and sort them
        image_files = sorted([f for f in os.listdir(folder_path) if f.lower().endswith(allowed_extensions)])
        
        if not image_files:
            return (None,)
        
        # Prepare list to hold the image tensors
        image_tensors = []
        
        # Load images up to max_frames, looping if necessary
        for i in range(max_frames):
            # Use modulo to loop back to start if we exceed available images
            file_index = i % len(image_files)
            selected_file = image_files[file_index]
            file_path = os.path.join(folder_path, selected_file)
            
            image = Image.open(file_path)
            # Ensure image is in RGB mode
            if image.mode != "RGB":
                image = image.convert("RGB")
            image_np = np.array(image).astype(np.float32) / 255.0
            image_tensor = torch.from_numpy(image_np)
            image_tensors.append(image_tensor)
        
        # Stack all image tensors into a batch
        batch_tensor = torch.stack(image_tensors, dim=0)
        return (batch_tensor,)

NODE_CLASS_MAPPINGS = {
    "ZenkaiVideoPose": ZenkaiVideoPose
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ZenkaiVideoPose": "Zenkai Video Pose"
}
