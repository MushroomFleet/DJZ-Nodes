import os
import glob
import random

ALLOWED_TEXT_EXT = ('.txt', '.md')

class LoadTextDirectory:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mode": (["single_file", "incremental_file", "random"],),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "index": ("INT", {"default": 0, "min": 0, "max": 150000, "step": 1}),
                "label": ("STRING", {"default": 'Text Batch 001', "multiline": False}),
                "path": ("STRING", {"default": '', "multiline": False}),
                "pattern": ("STRING", {"default": '*', "multiline": False}),
            },
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("text", "filename_text")
    FUNCTION = "load_text_directory"

    CATEGORY = "text"

    def load_text_directory(self, path, pattern='*', index=0, mode="single_file", seed=0, label='Text Batch 001'):
        if not os.path.exists(path):
            raise ValueError(f"Path does not exist: {path}")
            
        tl = self.TextDirectoryLoader(path, pattern)
        
        if mode == 'single_file':
            text_content, filename = tl.get_text_by_id(index)
            if text_content is None:
                raise ValueError(f"No valid text file found for index {index}")
        elif mode == 'incremental_file':
            text_content, filename = tl.get_next_text(index)
            if text_content is None:
                raise ValueError("No valid text file found")
        else:  # random mode
            random.seed(seed)
            newindex = int(random.random() * len(tl.text_paths))
            text_content, filename = tl.get_text_by_id(newindex)
            if text_content is None:
                raise ValueError("No valid text file found")

        return (text_content, filename)

    class TextDirectoryLoader:
        def __init__(self, directory_path, pattern):
            self.text_paths = []
            self.load_text_files(directory_path, pattern)
            self.text_paths.sort()
            self.index = 0

        def load_text_files(self, directory_path, pattern):
            for file_name in glob.glob(os.path.join(glob.escape(directory_path), pattern), recursive=True):
                if file_name.lower().endswith(ALLOWED_TEXT_EXT):
                    abs_file_path = os.path.abspath(file_name)
                    self.text_paths.append(abs_file_path)

        def get_text_by_id(self, text_id):
            if text_id < 0 or text_id >= len(self.text_paths):
                return None, None
                
            text_path = self.text_paths[text_id]
            try:
                with open(text_path, 'r', encoding='utf-8') as f:
                    text_content = f.read()
                return (text_content, os.path.basename(text_path))
            except Exception as e:
                print(f"Error reading file {text_path}: {str(e)}")
                return None, None

        def get_next_text(self, index):
            if index >= len(self.text_paths):
                index = 0
            return self.get_text_by_id(index)

# This is required for ComfyUI to recognize and load the node
NODE_CLASS_MAPPINGS = {
    "LoadTextDirectory": LoadTextDirectory
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadTextDirectory": "Load Text Directory"
}
