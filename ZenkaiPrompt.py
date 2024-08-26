import os
import random

class ZenkaiPrompt:
    @classmethod
    def INPUT_TYPES(cls):
        # Get the list of text files in the 'prompts' folder
        prompts_folder = os.path.join(os.path.dirname(__file__), 'prompts')
        text_files = [f for f in os.listdir(prompts_folder) if f.endswith('.txt')]
        
        return {
            "required": {
                "text_file": (text_files,),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 0xFFFFFFFF
                })
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate_prompt"
    CATEGORY = "DJZ-Nodes"

    def generate_prompt(self, text_file, seed):
        prompts_folder = os.path.join(os.path.dirname(__file__), 'prompts')
        file_path = os.path.join(prompts_folder, text_file)

        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Use the seed to consistently select a line
        random.seed(seed)
        selected_line = random.choice(lines).strip()

        return (selected_line,)

NODE_CLASS_MAPPINGS = {
    "ZenkaiPrompt": ZenkaiPrompt
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ZenkaiPrompt": "Zenkai-Prompt"
}