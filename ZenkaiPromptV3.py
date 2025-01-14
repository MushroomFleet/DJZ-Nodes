import os
import random

class ZenkaiPromptV3:
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
                "interpolation_mode": (["none", "lines", "directory"],),
                "division_preset": (["words", "halves", "thirds", "quarters", "fifths"],),
            },
            "optional": {
                "prefix": ("STRING", {"default": ""}),
                "suffix": ("STRING", {"default": ""})
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate_prompt"
    CATEGORY = "DJZ-Nodes"

    def __init__(self):
        self.division_map = {
            "words": 1,
            "halves": 2,
            "thirds": 3,
            "quarters": 4,
            "fifths": 5
        }

    def split_prompt(self, prompt, parts):
        words = prompt.split()
        total_words = len(words)
        words_per_part = total_words // parts
        remainder = total_words % parts
        
        sections = []
        start = 0
        
        for i in range(parts):
            section_size = words_per_part + (1 if i < remainder else 0)
            end = start + section_size
            sections.append(" ".join(words[start:end]))
            start = end
            
        return sections

    def get_random_line(self, file_path, seed):
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
        random.seed(seed)
        return random.choice(lines)

    def generate_prompt(self, text_file, seed, interpolation_mode, division_preset, prefix="", suffix=""):
        prompts_folder = os.path.join(os.path.dirname(__file__), 'prompts')
        file_path = os.path.join(prompts_folder, text_file)
        
        # Set random seed for reproducibility
        random.seed(seed)
        
        # Get initial prompt
        base_prompt = self.get_random_line(file_path, seed)
        
        if interpolation_mode == "none":
            return (f"{prefix}{base_prompt}{suffix}",)
            
        # Get number of divisions from preset
        num_parts = self.division_map[division_preset]
        sections = self.split_prompt(base_prompt, num_parts)
        
        # Handle different interpolation modes
        if interpolation_mode == "lines":
            # Get additional random lines from the same file
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f if line.strip()]
            
            for i in range(1, len(sections)):
                random_line = random.choice(lines)
                random_sections = self.split_prompt(random_line, num_parts)
                sections[i] = random_sections[i]
                
        elif interpolation_mode == "directory":
            # Get random lines from random files in the directory
            text_files = [f for f in os.listdir(prompts_folder) if f.endswith('.txt')]
            
            for i in range(1, len(sections)):
                random_file = random.choice(text_files)
                random_file_path = os.path.join(prompts_folder, random_file)
                random_line = self.get_random_line(random_file_path, random.randint(0, 0xFFFFFFFF))
                random_sections = self.split_prompt(random_line, num_parts)
                sections[i] = random_sections[i]
        
        # Combine sections into final prompt
        interpolated_prompt = " ".join(sections)
        return (f"{prefix}{interpolated_prompt}{suffix}",)

    @classmethod
    def IS_CHANGED(cls, text_file, seed, interpolation_mode, division_preset, prefix, suffix):
        return float(seed)

NODE_CLASS_MAPPINGS = {
    "ZenkaiPromptV3": ZenkaiPromptV3
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ZenkaiPromptV3": "Zenkai-Prompt V3"
}