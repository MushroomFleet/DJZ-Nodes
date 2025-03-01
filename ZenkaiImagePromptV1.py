import os
import random
import re
from PIL import Image
import numpy as np
import torch

class ZenkaiImagePromptV1:
    @classmethod
    def INPUT_TYPES(cls):
        # Determine the path to the imageprompts folder relative to this file
        imageprompts_folder = os.path.join(os.path.dirname(__file__), "imageprompts")
        
        # Create the folder if it doesn't exist
        if not os.path.exists(imageprompts_folder):
            os.makedirs(imageprompts_folder)
            
        # List subdirectories in the imageprompts folder
        subfolders = [d for d in os.listdir(imageprompts_folder) if os.path.isdir(os.path.join(imageprompts_folder, d))]
        
        # If there are no subfolders, provide a placeholder
        if not subfolders:
            subfolders = ["default"]
            # Create a default folder
            default_folder = os.path.join(imageprompts_folder, "default")
            if not os.path.exists(default_folder):
                os.makedirs(default_folder)
        
        return {
            "required": {
                "prompt_folder": (subfolders,),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 0xFFFFFFFF
                })
            },
            "optional": {
                "blacklist": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "placeholder": "e.g., table, cat, \"no humans\""
                })
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING",)
    FUNCTION = "load_image_prompt"
    CATEGORY = "DJZ-Nodes"

    def parse_blacklist(self, blacklist_str):
        if not blacklist_str.strip():
            return []
        
        # Pattern to match either quoted phrases or single words
        pattern = r'"([^"]+)"|([^,\s]+)'
        matches = re.findall(pattern, blacklist_str)
        
        # Combine both quoted and unquoted matches, strip whitespace
        return [quoted or unquoted.strip() for quoted, unquoted in matches if quoted or unquoted.strip()]

    def is_blacklisted(self, text, blacklist_terms):
        text_lower = text.lower()
        return any(term.lower() in text_lower for term in blacklist_terms)

    def load_image_prompt(self, prompt_folder, seed, blacklist=""):
        # Build absolute path to the selected subfolder under imageprompts
        folder_path = os.path.join(os.path.dirname(__file__), "imageprompts", prompt_folder)
        
        # Create the folder if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            return (torch.zeros(1, 3, 64, 64), "No images found in the selected folder")
        
        # Allowed image extensions
        allowed_extensions = (".jpeg", ".jpg", ".png")
        # List all allowed image files in the selected folder
        image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(allowed_extensions)]
        
        if not image_files:
            return (torch.zeros(1, 3, 64, 64), "No images found in the selected folder")
        
        # Parse blacklist
        blacklist_terms = self.parse_blacklist(blacklist)
        
        # Use the seed to establish a deterministic order
        random.seed(seed)
        # Shuffle the image files to process them in a random but deterministic order
        shuffled_files = image_files.copy()
        random.shuffle(shuffled_files)
        
        selected_image = None
        selected_text = "No valid image-text pair found after blacklist filtering"
        
        # Iterate through each image file
        for img_file in shuffled_files:
            # Construct the path to potential text file with same name but .txt extension
            base_name = os.path.splitext(img_file)[0]
            txt_file = os.path.join(folder_path, base_name + ".txt")
            
            # Skip if matching text file doesn't exist
            if not os.path.exists(txt_file):
                continue
            
            # Read the text file content
            try:
                with open(txt_file, 'r', encoding='utf-8') as f:
                    text_content = f.read().strip()
                
                # Skip if the text content contains blacklisted words
                if blacklist_terms and self.is_blacklisted(text_content, blacklist_terms):
                    continue
                
                # We found a matching pair that passes the blacklist filter
                selected_image = img_file
                selected_text = text_content
                break
                
            except Exception as e:
                # Skip this file if there's an error reading the text
                continue
        
        # If no valid pairs found, return placeholder
        if selected_image is None:
            return (torch.zeros(1, 3, 64, 64), selected_text)
        
        # Load the selected image
        file_path = os.path.join(folder_path, selected_image)
        try:
            image = Image.open(file_path)
            # Ensure image is in RGB mode
            if image.mode != "RGB":
                image = image.convert("RGB")
            image_np = np.array(image).astype(np.float32) / 255.0
            image_tensor = torch.from_numpy(image_np)
            if image_tensor.dim() == 3:
                image_tensor = image_tensor.unsqueeze(0)
            return (image_tensor, selected_text)
        except Exception as e:
            # Return placeholder if image can't be loaded
            return (torch.zeros(1, 3, 64, 64), f"Error loading image: {str(e)}")

    @classmethod
    def IS_CHANGED(cls, prompt_folder, seed, blacklist=""):
        return float(seed)  # This ensures the node updates when the seed changes

NODE_CLASS_MAPPINGS = {
    "ZenkaiImagePromptV1": ZenkaiImagePromptV1
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ZenkaiImagePromptV1": "Zenkai Image Prompt V1"
}
