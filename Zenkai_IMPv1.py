import os
import random
import re
from PIL import Image
import numpy as np
import torch
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Zenkai_IMPv1")

class Zenkai_IMPv1:
    @classmethod
    def INPUT_TYPES(cls):
        # Determine the path to the imageprompts folder relative to this file
        imageprompts_folder = os.path.join(os.path.dirname(__file__), "imagemaskprompts")
        
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

    RETURN_TYPES = ("IMAGE", "STRING", "IMAGE",)  # Added third output for mask
    RETURN_NAMES = ("image", "prompt", "mask",)   # Named outputs for clarity
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
        """Find all valid image-text pairs in the folder with logging for debugging."""
        # Allowed image extensions
        allowed_extensions = (".jpeg", ".jpg", ".png")
        
        # List all files in directory for debugging
        all_files = os.listdir(folder_path)
        logger.info(f"All files in directory {folder_path}: {all_files}")
        
        # More robust mask detection - exclude files ending with _M before the extension
        image_files = []
        for f in all_files:
            if not f.lower().endswith(allowed_extensions):
                continue
                
            base_name, ext = os.path.splitext(f)
            if base_name.endswith("_M"):
                logger.info(f"Skipping mask file: {f}")
                continue
                
            image_files.append(f)
            
        logger.info(f"Filtered image files (excluding masks): {image_files}")
        
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
                    logger.info(f"Found valid image-text pair: {img_file}")
                except Exception as e:
                    logger.warning(f"Error reading text file {txt_file}: {str(e)}")
                    continue
            else:
                logger.info(f"No text file found for image: {img_file}")
                    
        # Sort pairs by image filename using natural sort for consistent and intuitive ordering
        sorted_pairs = sorted(valid_pairs, key=lambda x: self.natural_sort_key(x[0]))
        logger.info(f"Total valid image-text pairs found: {len(sorted_pairs)}")
        return sorted_pairs

    def load_image_prompt(self, prompt_folder, seed, mode="sequential", num_images=1, blacklist=""):
        # Fix folder path: use imagemaskprompts consistent with INPUT_TYPES
        folder_path = os.path.join(os.path.dirname(__file__), "imagemaskprompts", prompt_folder)
        logger.info(f"Loading from folder: {folder_path}")
        
        # Create a standard empty tensor to use for error conditions
        empty_tensor = torch.zeros(1, 3, 64, 64)
        
        # Create the folder if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            logger.warning(f"Created folder: {folder_path} as it didn't exist")
            return (empty_tensor, "No images found in the selected folder", empty_tensor)
        
        # Get all valid image-text pairs
        valid_pairs = self.get_valid_image_text_pairs(folder_path)
        
        if not valid_pairs:
            logger.warning(f"No valid image-text pairs found in {folder_path}")
            return (empty_tensor, "No valid image-text pairs found in the selected folder", empty_tensor)
        
        # Parse blacklist
        blacklist_terms = self.parse_blacklist(blacklist)
        if blacklist_terms:
            logger.info(f"Applying blacklist terms: {blacklist_terms}")
        
        # Filter out blacklisted pairs
        if blacklist_terms:
            filtered_pairs = [(img, text) for img, text in valid_pairs 
                           if not self.is_blacklisted(text, blacklist_terms)]
            
            logger.info(f"After blacklist filtering: {len(filtered_pairs)} of {len(valid_pairs)} pairs remain")
            
            if not filtered_pairs:
                return (empty_tensor, "No valid pairs remaining after blacklist filtering", empty_tensor)
            
            valid_pairs = filtered_pairs
        
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
            empty_tensor = torch.zeros(1, 3, 64, 64)
            return (empty_tensor, "No pairs selected", empty_tensor)
        
        # Load all selected images and their corresponding masks
        loaded_images = []
        loaded_masks = []
        combined_text = []
        
        for img_file, text_content in selected_pairs:
            file_path = os.path.join(folder_path, img_file)
            
            # Determine mask file path with _M suffix
            base_name, ext = os.path.splitext(img_file)
            mask_file = os.path.join(folder_path, f"{base_name}_M{ext}")
            
            logger.info(f"Processing image: {img_file}")
            logger.info(f"Looking for mask at: {mask_file}")
            
            try:
                # Load main image
                image = Image.open(file_path)
                # Ensure image is in RGB mode
                if image.mode != "RGB":
                    image = image.convert("RGB")
                    logger.info(f"Converted image to RGB mode: {img_file}")
                
                image_np = np.array(image).astype(np.float32) / 255.0
                image_tensor = torch.from_numpy(image_np)
                
                # Handle tensor dimensions correctly - ensure it's in format [batch, height, width, channels]
                if image_tensor.dim() == 3:
                    image_tensor = image_tensor.unsqueeze(0)
                
                logger.info(f"Image tensor shape: {image_tensor.shape}")
                loaded_images.append(image_tensor)
                combined_text.append(text_content)
                
                # Try to load mask image if it exists
                if os.path.exists(mask_file):
                    logger.info(f"Found mask file: {mask_file}")
                    mask = Image.open(mask_file)
                    # Convert to RGB for consistency with ComfyUI
                    if mask.mode != "RGB":
                        mask = mask.convert("RGB")
                        logger.info(f"Converted mask to RGB mode: {mask_file}")
                    
                    mask_np = np.array(mask).astype(np.float32) / 255.0
                    mask_tensor = torch.from_numpy(mask_np)
                    
                    # Ensure mask has same dimensionality as image
                    if mask_tensor.dim() == 3:
                        mask_tensor = mask_tensor.unsqueeze(0)
                    
                    logger.info(f"Mask tensor shape: {mask_tensor.shape}")
                else:
                    logger.info(f"No mask file found. Creating default white mask.")
                    # Create a default white mask with correct dimensions
                    h, w = image_tensor.shape[1], image_tensor.shape[2]
                    # Create mask with shape [1, height, width, 3] to match image tensor
                    mask_tensor = torch.ones(1, h, w, 3)
                    logger.info(f"Default mask tensor shape: {mask_tensor.shape}")
                
                loaded_masks.append(mask_tensor)
                
            except Exception as e:
                logger.error(f"Error processing image {img_file}: {str(e)}")
                continue
        
        if not loaded_images:
            empty_tensor = torch.zeros(1, 3, 64, 64)
            return (empty_tensor, "Error loading selected images", empty_tensor)
        
        # Combine all images and masks into batches
        try:
            # Check if we have any valid images to process
            if not loaded_images:
                logger.warning("No valid images were loaded")
                return (empty_tensor, "No valid images were loaded", empty_tensor)
                
            # Log the image shapes for debugging
            logger.info(f"Image tensor shapes before batching: {[img.shape for img in loaded_images]}")
            logger.info(f"Mask tensor shapes before batching: {[mask.shape for mask in loaded_masks]}")
            
            # Ensure all images have the same dimensions by padding if necessary
            max_h = max(img.shape[1] for img in loaded_images)
            max_w = max(img.shape[2] for img in loaded_images)
            logger.info(f"Maximum dimensions for batching: {max_h}x{max_w}")
            
            # Pad images to the same size if needed
            padded_images = []
            padded_masks = []
            
            for i, (img, mask) in enumerate(zip(loaded_images, loaded_masks)):
                # Pad main image if needed
                if img.shape[1] == max_h and img.shape[2] == max_w:
                    logger.info(f"Image {i} already has correct dimensions")
                    padded_images.append(img)
                else:
                    logger.info(f"Padding image {i} from {img.shape} to [1, {max_h}, {max_w}, 3]")
                    # Create a new tensor with the maximum dimensions
                    padded = torch.zeros(1, max_h, max_w, 3)
                    h, w = img.shape[1], img.shape[2]
                    padded[0, :h, :w, :] = img[0]
                    padded_images.append(padded)
                
                # Pad mask if needed
                if mask.shape[1] == max_h and mask.shape[2] == max_w:
                    logger.info(f"Mask {i} already has correct dimensions")
                    padded_masks.append(mask)
                else:
                    logger.info(f"Padding mask {i} from {mask.shape} to [1, {max_h}, {max_w}, 3]")
                    # Create a new tensor with the maximum dimensions
                    padded = torch.zeros(1, max_h, max_w, 3)
                    h, w = mask.shape[1], mask.shape[2]
                    padded[0, :h, :w, :] = mask[0]
                    padded_masks.append(padded)
            
            # Stack all images and masks into batches
            batched_images = torch.cat(padded_images, dim=0)
            batched_masks = torch.cat(padded_masks, dim=0)
            
            logger.info(f"Final batched image tensor shape: {batched_images.shape}")
            logger.info(f"Final batched mask tensor shape: {batched_masks.shape}")
            
            # Join all texts with a separator
            joined_text = " | ".join(combined_text)
            logger.info(f"Returning batch with {len(combined_text)} images/masks")
            
            return (batched_images, joined_text, batched_masks)
        except Exception as e:
            logger.error(f"Error during batching: {str(e)}")
            # If we have at least one valid image, return it instead of an empty tensor
            if loaded_images:
                logger.info(f"Falling back to single image return: {loaded_images[0].shape}")
                return (loaded_images[0], combined_text[0], loaded_masks[0])
            else:
                # In case of catastrophic failure, return empty tensors
                return (empty_tensor, "Error processing images", empty_tensor)

    @classmethod
    def IS_CHANGED(cls, prompt_folder, seed, mode, num_images, blacklist=""):
        return float(seed)  # This ensures the node updates when the seed changes

NODE_CLASS_MAPPINGS = {
    "Zenkai_IMPv1": Zenkai_IMPv1
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Zenkai_IMPv1": "Zenkai IMP v1"
}
