import os
import hashlib
import safetensors.torch
import folder_paths
import torch

class DJZLoadLatent:
    """
    Loads latent tensors directly from ComfyUI's output directory.
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
        
        # If no latents found, provide an empty option
        if not latents:
            latents = [""]
            
        return {
            "required": {
                "latent_file": (sorted(latents),),
            },
        }

    CATEGORY = "DJZ-Nodes"
    RETURN_TYPES = ("LATENT",)
    FUNCTION = "load_latent"

    def load_latent(self, latent_file):
        if not latent_file:
            raise ValueError("No latent file selected")
        
        # Get the full path by joining with output directory
        output_dir = folder_paths.get_output_directory()
        latent_path = os.path.join(output_dir, latent_file)
        
        try:
            # Load the latent file
            latent = safetensors.torch.load_file(latent_path, device="cpu")
            
            # Apply the correct multiplier based on format version
            multiplier = 1.0 if "latent_format_version_0" in latent else 1.0 / 0.18215
            
            # Return the properly formatted samples
            samples = {
                "samples": latent["latent_tensor"].float() * multiplier
            }
            
            return (samples,)
            
        except Exception as e:
            print(f"Error loading latent: {str(e)}")
            return ({"samples": torch.zeros((1, 4, 8, 8))},)

    @classmethod
    def IS_CHANGED(s, latent_file):
        if not latent_file:
            return "NO_FILE_SELECTED"
            
        output_dir = folder_paths.get_output_directory()
        latent_path = os.path.join(output_dir, latent_file)
        
        try:
            m = hashlib.sha256()
            with open(latent_path, 'rb') as f:
                m.update(f.read())
            return m.digest().hex()
        except Exception:
            return "ERROR_READING_FILE"

    @classmethod
    def VALIDATE_INPUTS(s, latent_file):
        if not latent_file:
            return "No latent file selected"
            
        output_dir = folder_paths.get_output_directory()
        latent_path = os.path.join(output_dir, latent_file)
        
        if not os.path.exists(latent_path):
            return f"Latent file not found: {latent_file}"
        return True


NODE_CLASS_MAPPINGS = {
    "DJZ-LoadLatent": DJZLoadLatent
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DJZ-LoadLatent": "DJZ Load Latent"
}