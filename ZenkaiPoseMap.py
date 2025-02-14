import os
import random
from PIL import Image
import numpy as np
import torch

class ZenkaiPoseMap:
    @classmethod
    def INPUT_TYPES(cls):
        # Determine the path to the posemaps folder relative to this file
        posemaps_folder = os.path.join(os.path.dirname(__file__), "posemaps")
        # List subdirectories in the posemaps folder
        subfolders = [d for d in os.listdir(posemaps_folder) if os.path.isdir(os.path.join(posemaps_folder, d))]
        
        return {
            "required": {
                "pose_folder": (subfolders,),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 0xFFFFFFFF
                })
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "load_pose_map"
    CATEGORY = "DJZ-Nodes"

    def load_pose_map(self, pose_folder, seed):
        # Build absolute path to the selected subfolder under posemaps
        folder_path = os.path.join(os.path.dirname(__file__), "posemaps", pose_folder)
        # Allowed image extensions
        allowed_extensions = (".jpeg", ".jpg", ".png")
        # List all allowed image files in the selected folder
        image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(allowed_extensions)]
        
        if not image_files:
            return (None,)
        
        # Use the seed to get a consistent random selection
        random.seed(seed)
        selected_file = random.choice(image_files)
        file_path = os.path.join(folder_path, selected_file)
        
        image = Image.open(file_path)
        # Ensure image is in RGB mode
        if image.mode != "RGB":
            image = image.convert("RGB")
        image_np = np.array(image).astype(np.float32) / 255.0
        image_tensor = torch.from_numpy(image_np)
        if image_tensor.dim() == 3:
            image_tensor = image_tensor.unsqueeze(0)
        return (image_tensor,)

NODE_CLASS_MAPPINGS = {
    "ZenkaiPoseMap": ZenkaiPoseMap
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ZenkaiPoseMap": "Zenkai Pose Map"
}
