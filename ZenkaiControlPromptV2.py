import os
import random
import re
from PIL import Image
import numpy as np
import torch

class ZenkaiControlPromptV2:
    @classmethod
    def INPUT_TYPES(cls):
        # Determine the path to the imageprompts folder relative to this file
        imageprompts_folder = os.path.join(os.path.dirname(__file__), "controlprompts")
        
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
                "whitelist": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "placeholder": "e.g., table, cat, \"no humans\""
                })
            }
        }

    # Updated return types to include all control images
    RETURN_TYPES = ("IMAGE", "IMAGE", "IMAGE", "IMAGE", "IMAGE", "STRING",)
    RETURN_NAMES = ("image", "mask", "depth", "pose", "canny", "prompt",)
    FUNCTION = "load_image_prompt"
    CATEGORY = "DJZ-Nodes"

    def parse_whitelist(self, whitelist_str):
        if not whitelist_str.strip():
            return []
        
        # Pattern to match either quoted phrases or single words
        pattern = r'"([^"]+)"|([^,\s]+)'
        matches = re.findall(pattern, whitelist_str)
        
        # Combine both quoted and unquoted matches, strip whitespace
        return [quoted or unquoted.strip() for quoted, unquoted in matches if quoted or unquoted.strip()]

    def is_whitelisted(self, text, whitelist_terms):
        text_lower = text.lower()
        return any(term.lower() in text_lower for term in whitelist_terms)

    def natural_sort_key(self, s):
        """Natural sort key function for sorting filenames with numeric parts.
        This ensures that 'image1.png' comes before 'image10.png' in sorting."""
        # Split the string into text and numeric parts
        def convert(text):
            return int(text) if text.isdigit() else text.lower()
        return [convert(c) for c in re.split(r'(\d+)', s)]

    def find_base_images(self, folder_path):
        """Find all base images (those without _M, _D, _P, _C suffixes) that have matching text files."""
        print(f"Searching for base images in: {folder_path}")
        
        # Allowed image extensions
        allowed_extensions = (".jpeg", ".jpg", ".png")
        
        # Get all image files
        all_image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(allowed_extensions)]
        print(f"Total image files found: {len(all_image_files)}")
        
        # Filter to find only base images (those without control suffixes)
        base_images = []
        control_images = set()
        
        for img_file in all_image_files:
            base_name = os.path.splitext(img_file)[0]
            
            if base_name.endswith(("_M", "_D", "_P", "_C")):
                # This is a control image, add to control set
                control_images.add(img_file)
                continue
                
            # Check for matching text file
            txt_file = os.path.join(folder_path, base_name + ".txt")
            
            if os.path.exists(txt_file):
                try:
                    with open(txt_file, 'r', encoding='utf-8') as f:
                        text_content = f.read().strip()
                    base_images.append((img_file, text_content))
                    print(f"Added base image with text: {img_file}")
                except Exception as e:
                    # Skip if there's an error reading the text file
                    print(f"Error reading text file for {img_file}: {str(e)}")
                    continue
        
        print(f"Found {len(base_images)} base images with text files")
        print(f"Found {len(control_images)} control variant images")
            
        # Sort pairs by image filename using natural sort for consistent ordering
        return sorted(base_images, key=lambda x: self.natural_sort_key(x[0]))

    def load_image_file(self, file_path):
        """Load an image file and convert it to a tensor."""
        try:
            print(f"Loading image file: {file_path}")
            image = Image.open(file_path)
            
            # Print image details for debugging
            print(f"Original image mode: {image.mode}, size: {image.size}")
            
            # Force RGB mode to ensure proper channel count (handle grayscale, indexed, etc.)
            if image.mode != "RGB":
                try:
                    image = image.convert("RGB")
                    print(f"Converted image to RGB mode from {image.mode}")
                except Exception as convert_error:
                    print(f"Error converting image mode: {str(convert_error)}")
                    # Create a fallback RGB image if conversion fails
                    if hasattr(image, 'size'):
                        print(f"Creating fallback RGB image of size {image.size}")
                        fallback = Image.new("RGB", image.size, (0, 0, 0))
                        image = fallback
                    else:
                        print("Cannot determine image size, using default")
                        fallback = Image.new("RGB", (64, 64), (0, 0, 0))
                        image = fallback
            
            # Convert to numpy array with proper dtype
            try:
                image_np = np.array(image).astype(np.float32) / 255.0
                print(f"Numpy array shape: {image_np.shape}, dtype: {image_np.dtype}")
                
                # Verify array has correct number of channels
                if len(image_np.shape) == 2:
                    # Single channel image (grayscale), convert to 3-channel
                    print(f"Converting single channel image to RGB")
                    image_np = np.stack([image_np, image_np, image_np], axis=2)
                elif len(image_np.shape) == 3 and image_np.shape[2] == 1:
                    # Single channel with explicit dimension, convert to 3-channel
                    print(f"Converting single channel image (with dimension) to RGB")
                    image_np = np.concatenate([image_np, image_np, image_np], axis=2)
                elif len(image_np.shape) == 3 and image_np.shape[2] == 4:
                    # RGBA image, drop alpha channel
                    print(f"Dropping alpha channel from RGBA image")
                    image_np = image_np[:, :, :3]
                elif len(image_np.shape) == 3 and image_np.shape[2] != 3:
                    # Unusual channel count, create new RGB array
                    print(f"Unusual channel count ({image_np.shape[2]}), creating new RGB array")
                    new_np = np.zeros((image_np.shape[0], image_np.shape[1], 3), dtype=np.float32)
                    # Copy available channels, up to 3
                    for i in range(min(image_np.shape[2], 3)):
                        new_np[:, :, i] = image_np[:, :, i]
                    image_np = new_np
            except Exception as np_error:
                print(f"Error creating numpy array: {str(np_error)}")
                # Create fallback array
                print("Creating fallback numpy array")
                image_np = np.zeros((64, 64, 3), dtype=np.float32)
            
            # Convert to tensor
            image_tensor = torch.from_numpy(image_np)
            
            # Add batch dimension if not present
            if image_tensor.dim() == 3:
                image_tensor = image_tensor.unsqueeze(0)
                
            print(f"Final tensor shape: {image_tensor.shape}, dtype: {image_tensor.dtype}")
            
            # Final validation
            if image_tensor.shape[1] != 3:
                print(f"WARNING: Final tensor still has unusual channel count ({image_tensor.shape[1]})")
                # Create proper tensor as last resort
                fixed_tensor = torch.zeros(1, 3, image_tensor.shape[2], image_tensor.shape[3])
                # Copy data from channels that exist
                for i in range(min(image_tensor.shape[1], 3)):
                    fixed_tensor[:, i] = image_tensor[:, i]
                return fixed_tensor
                
            return image_tensor
        except Exception as e:
            print(f"Error loading image {file_path}: {str(e)}")
            # Return empty tensor as fallback
            return torch.zeros(1, 3, 64, 64)

    def find_control_file(self, folder_path, base_filename, suffix):
        """Find a control file with the given suffix for a base image filename."""
        base_name, ext = os.path.splitext(base_filename)
        control_path = os.path.join(folder_path, f"{base_name}_{suffix}{ext}")
        
        if os.path.exists(control_path):
            print(f"Found control file for {base_filename} with suffix _{suffix}")
            return control_path
        else:
            print(f"No control file found for {base_filename} with suffix _{suffix}")
            return None

    def load_image_prompt(self, prompt_folder, seed, mode="sequential", num_images=1, whitelist=""):
        print(f"Loading image prompts with: folder={prompt_folder}, seed={seed}, mode={mode}, num_images={num_images}")
        
        # Build absolute path to the selected subfolder under controlprompts
        folder_path = os.path.join(os.path.dirname(__file__), "controlprompts", prompt_folder)
        
        # Create the folder if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Created folder: {folder_path}")
            empty_tensor = torch.zeros(1, 3, 64, 64)
            return (empty_tensor, empty_tensor, empty_tensor, empty_tensor, empty_tensor, 
                    "No images found in the selected folder")
        
        # Get all valid base image-text pairs
        valid_pairs = self.find_base_images(folder_path)
        
        if not valid_pairs:
            print("No valid image-text pairs found")
            empty_tensor = torch.zeros(1, 3, 64, 64)
            return (empty_tensor, empty_tensor, empty_tensor, empty_tensor, empty_tensor, 
                    "No valid image-text pairs found in the selected folder")
        
        # Parse whitelist - only apply if there's content in the whitelist
        whitelist_terms = self.parse_whitelist(whitelist)
        
        # Filter using whitelist if it's not empty
        if whitelist_terms:
            print(f"Filtering with whitelist terms: {whitelist_terms}")
            valid_pairs = [(img, text) for img, text in valid_pairs 
                           if self.is_whitelisted(text, whitelist_terms)]
            
            if not valid_pairs:
                print("No valid pairs matching whitelist criteria")
                empty_tensor = torch.zeros(1, 3, 64, 64)
                return (empty_tensor, empty_tensor, empty_tensor, empty_tensor, empty_tensor, 
                        "No valid pairs matching whitelist criteria")
        
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
        
        print(f"Selected {len(selected_pairs)} image-text pairs")
        
        # Process selected pairs
        if not selected_pairs:
            print("No pairs selected")
            empty_tensor = torch.zeros(1, 3, 64, 64)
            return (empty_tensor, empty_tensor, empty_tensor, empty_tensor, empty_tensor, 
                    "No pairs selected")
        
        # Load all selected images and their control variants
        loaded_images = []
        loaded_masks = []
        loaded_depths = []
        loaded_poses = []
        loaded_cannies = []
        combined_text = []
        
        for img_file, text_content in selected_pairs:
            base_path = os.path.join(folder_path, img_file)
            print(f"Processing base image: {img_file}")
            
            # Load main image
            base_image = self.load_image_file(base_path)
            if base_image is None:
                print(f"Failed to load base image: {img_file}")
                continue
            
            # Load control variants if they exist
            # Mask (_M suffix)
            mask_path = self.find_control_file(folder_path, img_file, "M")
            mask_image = self.load_image_file(mask_path) if mask_path else None
            
            # Depth (_D suffix)
            depth_path = self.find_control_file(folder_path, img_file, "D")
            depth_image = self.load_image_file(depth_path) if depth_path else None
            
            # Pose (_P suffix)
            pose_path = self.find_control_file(folder_path, img_file, "P")
            pose_image = self.load_image_file(pose_path) if pose_path else None
            
            # Canny (_C suffix)
            canny_path = self.find_control_file(folder_path, img_file, "C")
            canny_image = self.load_image_file(canny_path) if canny_path else None
            
            # If any control image is missing, create a placeholder with same shape as base image
            if mask_image is None:
                print(f"Creating placeholder for mask image for {img_file}")
                mask_image = torch.zeros_like(base_image)
                
            if depth_image is None:
                print(f"Creating placeholder for depth image for {img_file}")
                depth_image = torch.zeros_like(base_image)
                
            if pose_image is None:
                print(f"Creating placeholder for pose image for {img_file}")
                pose_image = torch.zeros_like(base_image)
                
            if canny_image is None:
                print(f"Creating placeholder for canny image for {img_file}")
                canny_image = torch.zeros_like(base_image)
            
            # Add to our collection
            loaded_images.append(base_image)
            loaded_masks.append(mask_image)
            loaded_depths.append(depth_image)
            loaded_poses.append(pose_image)
            loaded_cannies.append(canny_image)
            combined_text.append(text_content)
            
            print(f"Successfully processed image set for {img_file}")
        
        if not loaded_images:
            print("No images were successfully loaded")
            empty_tensor = torch.zeros(1, 3, 64, 64)
            return (empty_tensor, empty_tensor, empty_tensor, empty_tensor, empty_tensor, 
                    "Error loading selected images")
        
        # Combine all images into batches
        try:
            print("Combining images into batches")
            
            # Find maximum dimensions across all image types
            # For tensor shape [batch, channel, height, width]
            max_h = max(max(img.shape[2] for img in loaded_images),
                         max(img.shape[2] for img in loaded_masks),
                         max(img.shape[2] for img in loaded_depths),
                         max(img.shape[2] for img in loaded_poses),
                         max(img.shape[2] for img in loaded_cannies))
            
            max_w = max(max(img.shape[3] for img in loaded_images),
                         max(img.shape[3] for img in loaded_masks),
                         max(img.shape[3] for img in loaded_depths),
                         max(img.shape[3] for img in loaded_poses),
                         max(img.shape[3] for img in loaded_cannies))
            
            print(f"Maximum dimensions: {max_h}x{max_w}")
            
            # Function to pad and batch images
            def batch_images(images, max_h, max_w):
                if not images:
                    print("No images to batch, returning empty tensor")
                    return torch.zeros(1, 3, 64, 64)
                
                padded = []
                for i, img in enumerate(images):
                    print(f"Processing image {i} with shape {img.shape}")
                    
                    # Check for unusual tensor shapes that might cause problems
                    if len(img.shape) != 4:
                        print(f"WARNING: Image {i} has unexpected dimensions: {img.shape}")
                        continue
                        
                    if img.shape[1] != 3:
                        print(f"WARNING: Image {i} has {img.shape[1]} channels instead of 3")
                        continue
                    
                    # If image dimensions match max dimensions, add it as is
                    if img.shape[2] == max_h and img.shape[3] == max_w:
                        padded.append(img)
                        print(f"Added image {i} directly (exact dimensions match)")
                    else:
                        try:
                            # Otherwise, create a new padded tensor
                            padded_img = torch.zeros(1, 3, max_h, max_w)
                            h, w = img.shape[2], img.shape[3]
                            # Copy content from original image
                            padded_img[0, :, :h, :w] = img[0, :, :h, :w]
                            padded.append(padded_img)
                            print(f"Padded image {i} from {h}x{w} to {max_h}x{max_w}")
                        except Exception as pad_error:
                            print(f"Error padding image {i}: {str(pad_error)}")
                            print(f"Original shape: {img.shape}, Target: {max_h}x{max_w}")
                            continue
                
                if not padded:
                    print("WARNING: No valid images to batch, returning empty tensor")
                    return torch.zeros(1, 3, 64, 64)
                
                try:
                    # Concatenate along batch dimension
                    result = torch.cat(padded, dim=0)
                    print(f"Batched {len(padded)} images to shape {result.shape}")
                    return result
                except Exception as cat_error:
                    print(f"Error concatenating images: {str(cat_error)}")
                    if padded:
                        print("Returning first valid image as fallback")
                        return padded[0]
                    else:
                        return torch.zeros(1, 3, 64, 64)
            
            # Batch all image types
            batched_images = batch_images(loaded_images, max_h, max_w)
            batched_masks = batch_images(loaded_masks, max_h, max_w)
            batched_depths = batch_images(loaded_depths, max_h, max_w)
            batched_poses = batch_images(loaded_poses, max_h, max_w)
            batched_cannies = batch_images(loaded_cannies, max_h, max_w)
            
            # Join all texts with a separator
            joined_text = " | ".join(combined_text)
            
            print("Successfully batched all images")
            return (batched_images, batched_masks, batched_depths, batched_poses, batched_cannies, joined_text)
            
        except Exception as e:
            print(f"Exception during batching: {str(e)}")
            
            # If batching fails, return first image of each type as fallback
            try:
                print("Falling back to returning first images")
                return (loaded_images[0], loaded_masks[0], loaded_depths[0], 
                        loaded_poses[0], loaded_cannies[0], combined_text[0])
            except Exception as fallback_error:
                print(f"Error in fallback handling: {str(fallback_error)}")
                
                # Last resort: empty tensors
                empty_tensor = torch.zeros(1, 3, 64, 64)
                return (empty_tensor, empty_tensor, empty_tensor, empty_tensor, empty_tensor, 
                        "Failed to process images")

    @classmethod
    def IS_CHANGED(cls, prompt_folder, seed, mode, num_images, whitelist=""):
        return float(seed)  # This ensures the node updates when the seed changes

NODE_CLASS_MAPPINGS = {
    "ZenkaiControlPromptV2": ZenkaiControlPromptV2
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ZenkaiControlPromptV2": "Zenkai Control Prompt V2"
}
