import os
import random
import re
from PIL import Image
import numpy as np
import torch

class ZenkaiImagePromptV2:
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
                }),
                "mode": (["sequential", "random"],),
                "num_images": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 10,
                    "step": 1
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

    def natural_sort_key(self, s):
        """Natural sort key function for sorting filenames with numeric parts.
        This ensures that 'image1.png' comes before 'image10.png' in sorting."""
        # Split the string into text and numeric parts
        def convert(text):
            return int(text) if text.isdigit() else text.lower()
        return [convert(c) for c in re.split(r'(\d+)', s)]

    def get_valid_image_text_pairs(self, folder_path):
        """Find all valid image-text pairs in the folder."""
        # Allowed image extensions
        allowed_extensions = (".jpeg", ".jpg", ".png")
        # Get all image files
        image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(allowed_extensions)]
        
        valid_pairs = []
        for img_file in image_files:
            # Check for matching text file
            base_name = os.path.splitext(img_file)[0]
            txt_file = os.path.join(folder_path, base_name + ".txt")
            
            if os.path.exists(txt_file):
                try:
                    with open(txt_file, 'r', encoding='utf-8') as f:
                        text_content = f.read().strip()
                    valid_pairs.append((img_file, text_content))
                except Exception:
                    # Skip if there's an error reading the text file
                    continue
                    
        # Sort pairs by image filename using natural sort for consistent and intuitive ordering
        return sorted(valid_pairs, key=lambda x: self.natural_sort_key(x[0]))

    def load_image_prompt(self, prompt_folder, seed, mode="sequential", num_images=1, blacklist=""):
        # Build absolute path to the selected subfolder under imageprompts
        folder_path = os.path.join(os.path.dirname(__file__), "imageprompts", prompt_folder)
        
        # Create the folder if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            return (torch.zeros(1, 3, 64, 64), "No images found in the selected folder")
        
        # Get all valid image-text pairs
        valid_pairs = self.get_valid_image_text_pairs(folder_path)
        
        if not valid_pairs:
            return (torch.zeros(1, 3, 64, 64), "No valid image-text pairs found in the selected folder")
        
        # Parse blacklist
        blacklist_terms = self.parse_blacklist(blacklist)
        
        # Filter out blacklisted pairs
        if blacklist_terms:
            valid_pairs = [(img, text) for img, text in valid_pairs 
                           if not self.is_blacklisted(text, blacklist_terms)]
            
            if not valid_pairs:
                return (torch.zeros(1, 3, 64, 64), "No valid pairs remaining after blacklist filtering")
        
        total_pairs = len(valid_pairs)
        selected_pairs = []
        
        if mode == "sequential":
            # Sequential mode: Directly map seed to index with looping
            for i in range(num_images):
                # Calculate pair index based on seed, looping if needed
                pair_index = (seed + i) % total_pairs
                selected_pairs.append(valid_pairs[pair_index])
        else:
            # Random mode: Use seed for reproducible randomness
            random.seed(seed)
            # Sample with replacement if num_images > total_pairs
            if num_images <= total_pairs:
                selected_pairs = random.sample(valid_pairs, num_images)
            else:
                selected_pairs = random.choices(valid_pairs, k=num_images)
        
        # Process selected pairs
        if not selected_pairs:
            return (torch.zeros(1, 3, 64, 64), "No pairs selected")
        
        # Load all selected images
        loaded_images = []
        combined_text = []
        
        for img_file, text_content in selected_pairs:
            file_path = os.path.join(folder_path, img_file)
            try:
                image = Image.open(file_path)
                # Ensure image is in RGB mode
                if image.mode != "RGB":
                    image = image.convert("RGB")
                image_np = np.array(image).astype(np.float32) / 255.0
                image_tensor = torch.from_numpy(image_np)
                if image_tensor.dim() == 3:
                    image_tensor = image_tensor.unsqueeze(0)
                
                loaded_images.append(image_tensor)
                combined_text.append(text_content)
            except Exception as e:
                # Skip this image if there's an error
                continue
        
        if not loaded_images:
            return (torch.zeros(1, 3, 64, 64), "Error loading selected images")
        
        # Combine all images into a batch
        try:
            # Ensure all images have the same dimensions by padding if necessary
            max_h = max(img.shape[1] for img in loaded_images)
            max_w = max(img.shape[2] for img in loaded_images)
            
            # Pad images to the same size if needed
            padded_images = []
            for img in loaded_images:
                if img.shape[1] == max_h and img.shape[2] == max_w:
                    padded_images.append(img)
                else:
                    # Create a new tensor with the maximum dimensions
                    padded = torch.zeros(1, max_h, max_w, 3)
                    h, w = img.shape[1], img.shape[2]
                    padded[0, :h, :w, :] = img[0]
                    padded_images.append(padded)
            
            # Stack all images into a batch
            batched_images = torch.cat(padded_images, dim=0)
            
            # Join all texts with a separator
            joined_text = " | ".join(combined_text)
            
            return (batched_images, joined_text)
        except Exception as e:
            # Return just the first image if batching fails
            return (loaded_images[0], combined_text[0])

    @classmethod
    def IS_CHANGED(cls, prompt_folder, seed, mode, num_images, blacklist=""):
        return float(seed)  # This ensures the node updates when the seed changes

NODE_CLASS_MAPPINGS = {
    "ZenkaiImagePromptV2": ZenkaiImagePromptV2
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ZenkaiImagePromptV2": "Zenkai Image Prompt V2"
}
