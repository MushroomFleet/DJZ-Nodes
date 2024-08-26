import os
import random
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ZenkaiWildcard:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True}),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 0xFFFFFFFF
                }),
                "wildcard_symbol": ("STRING", {"default": "$$"})
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "process_wildcards"
    CATEGORY = "DJZ-Nodes"

    def process_wildcards(self, prompt, seed, wildcard_symbol):
        random.seed(seed)
        wildcards_folder = os.path.join(os.path.dirname(__file__), 'wildcards')
        logger.info(f"Wildcards folder: {wildcards_folder}")
        
        def replace_wildcard(match):
            wildcard = match.group(1)
            file_path = os.path.join(wildcards_folder, f"{wildcard}.txt")
            logger.info(f"Looking for file: {file_path}")
            
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = [line.strip() for line in f if line.strip()]
                if lines:
                    choice = random.choice(lines)
                    logger.info(f"Replaced {wildcard} with: {choice}")
                    return choice
                else:
                    logger.warning(f"File {file_path} is empty")
                    return match.group(0)
            else:
                logger.warning(f"File not found: {file_path}")
                return match.group(0)  # Return the original text if file not found

        # Escape the wildcard symbol for regex
        escaped_symbol = re.escape(wildcard_symbol)
        pattern = f"{escaped_symbol}([a-zA-Z0-9_]+)"  # Removed the trailing wildcard symbol
        
        logger.info(f"Original prompt: {prompt}")
        logger.info(f"Using pattern: {pattern}")
        
        processed_prompt = re.sub(pattern, replace_wildcard, prompt)
        logger.info(f"Processed prompt: {processed_prompt}")
        
        # If no changes were made, log the content of the color.txt file
        if processed_prompt == prompt:
            color_file_path = os.path.join(wildcards_folder, "color.txt")
            if os.path.exists(color_file_path):
                with open(color_file_path, 'r', encoding='utf-8') as f:
                    logger.info(f"Content of color.txt: {f.read()}")
            else:
                logger.warning("color.txt file not found")
        
        return (processed_prompt,)

    @classmethod
    def IS_CHANGED(cls, prompt, seed, wildcard_symbol):
        return float(seed)  # This ensures the node updates when the seed changes

NODE_CLASS_MAPPINGS = {
    "ZenkaiWildcard": ZenkaiWildcard
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ZenkaiWildcard": "Zenkai-Wildcard"
}