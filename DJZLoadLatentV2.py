import os
import hashlib
import safetensors.torch
import folder_paths
import torch

class DJZLoadLatentV2:
    """
    Loads latent tensors directly from ComfyUI's output directory.
    Uses seed value to determine position in the latent list.
    Shows numbered list of latents for reference.
    """
    @classmethod
    def INPUT_TYPES(s):
        # Get the output directory
        output_dir = folder_paths.get_output_directory()
        
        # Scan for .latent files in outputs
        latents = []
        
        def scan_folder(folder, relative_path=""):
            try:
                for item in os.listdir(folder):
                    full_path = os.path.join(folder, item)
                    rel_path = os.path.join(relative_path, item)
                    
                    if os.path.isfile(full_path) and item.endswith(".latent"):
                        # Store relative path for cleaner display
                        latents.append(rel_path)
                    elif os.path.isdir(full_path):
                        # Recursively scan subdirectories
                        scan_folder(full_path, rel_path)
            except Exception as e:
                print(f"Error scanning directory {folder}: {str(e)}")
        
        # Start scan from output directory
        scan_folder(output_dir)
        
        # Sort the latents list
        latents = sorted(latents)
        
        # Create numbered list for display
        numbered_latents = [f"[{i}] {path}" for i, path in enumerate(latents)] if latents else ["No latents found"]
        
        return {
            "required": {
                "latent_index": (numbered_latents,), # Renamed to better reflect its role as a reference
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            },
        }

    CATEGORY = "DJZ-Nodes"
    RETURN_TYPES = ("LATENT", "STRING",)
    RETURN_NAMES = ("samples", "current_file",)
    FUNCTION = "load_latent"

    def load_latent(self, latent_index, seed):
        # Get the output directory and current list of latents
        output_dir = folder_paths.get_output_directory()
        latents = []
        for root, _, files in os.walk(output_dir):
            for file in files:
                if file.endswith(".latent"):
                    rel_path = os.path.relpath(os.path.join(root, file), output_dir)
                    latents.append(rel_path)
        latents = sorted(latents)
        
        if not latents:
            raise ValueError("No latent files found")
        
        # Use seed to determine position in list
        position = seed % len(latents)
        file_to_load = latents[position]
        print(f"Loading latent {position} of {len(latents)-1}: {file_to_load}")
        
        # Load the selected file
        latent_path = os.path.join(output_dir, file_to_load)
        
        try:
            # Load the latent file
            latent = safetensors.torch.load_file(latent_path, device="cpu")
            
            # Apply the correct multiplier based on format version
            multiplier = 1.0 if "latent_format_version_0" in latent else 1.0 / 0.18215
            
            # Return the properly formatted samples
            samples = {
                "samples": latent["latent_tensor"].float() * multiplier
            }
            
            return (samples, file_to_load)
            
        except Exception as e:
            print(f"Error loading latent: {str(e)}")
            return ({"samples": torch.zeros((1, 4, 8, 8))}, file_to_load)

    @classmethod
    def IS_CHANGED(s, latent_index, seed):
        # Only update when seed changes
        return seed

    @classmethod
    def VALIDATE_INPUTS(s, latent_index, seed):
        if not isinstance(seed, int):
            return "Seed must be an integer"
        return True


NODE_CLASS_MAPPINGS = {
    "DJZ-LoadLatentV2": DJZLoadLatentV2
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DJZ-LoadLatentV2": "DJZ Load Latent V2"
}