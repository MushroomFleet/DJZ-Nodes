import os
import random

class ZenkaiPromptV2:
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
                })
            },
            "optional": {
                "prefix": ("STRING", {"default": ""}),
                "suffix": ("STRING", {"default": ""})
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate_prompts"
    CATEGORY = "DJZ-Nodes"

    def generate_prompts(self, text_file, seed, num_prompts, prefix="", suffix=""):
        prompts_folder = os.path.join(os.path.dirname(__file__), 'prompts')
        file_path = os.path.join(prompts_folder, text_file)

        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]

        random.seed(seed)
        selected_lines = random.sample(lines, min(num_prompts, len(lines)))

        prompts = [f"{prefix}{line}{suffix}" for line in selected_lines]
        return (", ".join(prompts),)

    @classmethod
    def IS_CHANGED(cls, text_file, seed, num_prompts, prefix, suffix):
        return float(seed)  # This ensures the node updates when the seed changes

NODE_CLASS_MAPPINGS = {
    "ZenkaiPromptV2": ZenkaiPromptV2
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ZenkaiPromptV2": "Zenkai-Prompt V2"
}