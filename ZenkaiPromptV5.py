import os
import random

class ZenkaiPromptV5:
    @classmethod
    def INPUT_TYPES(cls):
        prompts_folder = os.path.join(os.path.dirname(__file__), 'prompts')
        text_files = [f for f in os.listdir(prompts_folder) if f.endswith('.txt')]
        
        return {
            "required": {
                "text_file": (text_files,),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 0xFFFFFFFF
                }),
                "num_prompts": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 10,
                    "step": 1
                }),
                "mode": (["sequential", "random"],),
            },
            "optional": {
                "prefix": ("STRING", {"default": ""}),
                "suffix": ("STRING", {"default": ""})
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate_prompts"
    CATEGORY = "DJZ-Nodes"

    def generate_prompts(self, text_file, seed, num_prompts, mode="sequential", prefix="", suffix=""):
        prompts_folder = os.path.join(os.path.dirname(__file__), 'prompts')
        file_path = os.path.join(prompts_folder, text_file)

        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
        
        total_lines = len(lines)
        if total_lines == 0:
            return ("No valid prompts found in the file.",)
            
        if mode == "sequential":
            # Sequential mode: Directly map seed to line index with looping
            selected_lines = []
            for i in range(num_prompts):
                # Calculate line index based on seed, looping if needed
                line_index = (seed + i) % total_lines
                selected_lines.append(lines[line_index])
        else:
            # Random mode: Use seed for reproducible randomness
            random.seed(seed)
            selected_lines = random.sample(lines, min(num_prompts, total_lines))

        prompts = [f"{prefix}{line}{suffix}" for line in selected_lines]
        return (", ".join(prompts),)

    @classmethod
    def IS_CHANGED(cls, text_file, seed, num_prompts, mode, prefix, suffix):
        return float(seed)  # This ensures the node updates when the seed changes

NODE_CLASS_MAPPINGS = {
    "ZenkaiPromptV5": ZenkaiPromptV5
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ZenkaiPromptV5": "Zenkai Prompt V5"
}