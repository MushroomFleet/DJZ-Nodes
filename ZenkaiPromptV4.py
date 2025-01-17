import os
import random
import re

class ZenkaiPromptV4:
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
                "suffix": ("STRING", {"default": ""}),
                "blacklist": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "placeholder": "e.g., table, cat, \"no humans\""
                })
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate_prompts"
    CATEGORY = "DJZ-Nodes"

    def parse_blacklist(self, blacklist_str):
        if not blacklist_str.strip():
            return []
        
        # Pattern to match either quoted phrases or single words
        pattern = r'"([^"]+)"|([^,\s]+)'
        matches = re.findall(pattern, blacklist_str)
        
        # Combine both quoted and unquoted matches, strip whitespace
        return [quoted or unquoted.strip() for quoted, unquoted in matches if quoted or unquoted.strip()]

    def is_blacklisted(self, prompt, blacklist_terms):
        prompt_lower = prompt.lower()
        return any(term.lower() in prompt_lower for term in blacklist_terms)

    def generate_prompts(self, text_file, seed, num_prompts, prefix="", suffix="", blacklist=""):
        prompts_folder = os.path.join(os.path.dirname(__file__), 'prompts')
        file_path = os.path.join(prompts_folder, text_file)

        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]

        blacklist_terms = self.parse_blacklist(blacklist)
        
        # Filter out blacklisted prompts
        if blacklist_terms:
            lines = [line for line in lines if not self.is_blacklisted(line, blacklist_terms)]
            
            if not lines:
                return ("No prompts available after applying blacklist filter.",)

        random.seed(seed)
        selected_lines = random.sample(lines, min(num_prompts, len(lines)))

        prompts = [f"{prefix}{line}{suffix}" for line in selected_lines]
        return (", ".join(prompts),)

    @classmethod
    def IS_CHANGED(cls, text_file, seed, num_prompts, prefix, suffix, blacklist):
        return float(seed)  # This ensures the node updates when the seed changes

NODE_CLASS_MAPPINGS = {
    "ZenkaiPromptV4": ZenkaiPromptV4
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ZenkaiPromptV4": "Zenkai-Prompt V4"
}
