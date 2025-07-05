import os
import random
import torch
import torchaudio
import numpy as np

class ZenkaiAmbienceAudioV1:
    @classmethod
    def INPUT_TYPES(cls):
        # Determine the path to the ambience folder relative to this file
        ambience_folder = os.path.join(os.path.dirname(__file__), "ambience")
        # Create the folder if it doesn't exist
        if not os.path.exists(ambience_folder):
            os.makedirs(ambience_folder)
        # List subdirectories in the ambience folder
        subfolders = [d for d in os.listdir(ambience_folder) if os.path.isdir(os.path.join(ambience_folder, d))]
        
        # If no subfolders exist, provide a default option
        if not subfolders:
            subfolders = ["default"]
            # Create a default folder
            default_folder = os.path.join(ambience_folder, "default")
            if not os.path.exists(default_folder):
                os.makedirs(default_folder)
        
        return {
            "required": {
                "ambience_folder": (subfolders,),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 0xFFFFFFFF
                })
            }
        }

    RETURN_TYPES = ("AUDIO",)
    FUNCTION = "load_ambience"
    CATEGORY = "DJZ-Nodes"

    def load_ambience(self, ambience_folder, seed):
        # Build absolute path to the selected subfolder under ambience
        folder_path = os.path.join(os.path.dirname(__file__), "ambience", ambience_folder)
        # Allowed audio file extensions
        allowed_extensions = (".wav", ".mp3", ".ogg", ".flac")
        # List all allowed audio files in the selected folder
        audio_files = [f for f in os.listdir(folder_path) if f.lower().endswith(allowed_extensions)]
        
        if not audio_files:
            # Return empty audio if no files found
            return ({"waveform": torch.zeros(1, 1, 1), "sample_rate": 44100, "path": None},)
        
        # Use the seed to get a consistent random selection
        random.seed(seed)
        selected_file = random.choice(audio_files)
        file_path = os.path.join(folder_path, selected_file)
        
        try:
            # Load audio file
            waveform, sample_rate = torchaudio.load(file_path)
            
            # Ensure correct shape [batch, channels, samples]
            if waveform.dim() == 2:  # [channels, samples]
                waveform = waveform.unsqueeze(0)  # Add batch dimension
            elif waveform.dim() == 1:  # [samples]
                waveform = waveform.unsqueeze(0).unsqueeze(0)  # Add batch and channel dimensions
            
            # Create audio dictionary format compatible with ComfyUI
            audio = {
                "waveform": waveform,
                "sample_rate": sample_rate,
                "path": file_path
            }
            
            return (audio,)
            
        except Exception as e:
            print(f"Error loading audio file {file_path}: {str(e)}")
            # Return empty audio in case of error
            return ({"waveform": torch.zeros(1, 1, 1), "sample_rate": 44100, "path": None},)

NODE_CLASS_MAPPINGS = {
    "ZenkaiAmbienceAudioV1": ZenkaiAmbienceAudioV1
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ZenkaiAmbienceAudioV1": "Zenkai Ambience Audio"
}
