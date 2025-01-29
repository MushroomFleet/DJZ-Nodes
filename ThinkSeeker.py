import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ThinkSeeker:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING",)  # First for thinking_text, second for response_text
    FUNCTION = "parse_thinking"
    CATEGORY = "Custom-Nodes"

    def parse_thinking(self, text):
        """
        Parse input text and split it into thinking sections and response sections.
        If no think tags are found, thinking_sections will be empty string.
        Returns a tuple of (thinking_text, response_text)
        """
        # Pattern to match content between thinking tags
        thinking_pattern = r'<think>(.*?)</think>'
        
        # Find all thinking sections
        thinking_sections = re.findall(thinking_pattern, text, re.DOTALL)
        
        # Remove thinking sections from the original text to get response content
        response_content = re.sub(thinking_pattern, '', text, flags=re.DOTALL)
        
        # Join thinking sections with newlines if any exist, otherwise empty string
        thinking_text = "\n".join(thinking_sections) if thinking_sections else ""
        
        # Log the parsing results
        logger.info(f"Original text: {text}")
        logger.info(f"Extracted thinking text: {thinking_text}")
        logger.info(f"Response text: {response_content.strip()}")
        
        return (thinking_text, response_content.strip())

    @classmethod
    def IS_CHANGED(cls, text):
        return text

NODE_CLASS_MAPPINGS = {
    "ThinkSeeker": ThinkSeeker
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ThinkSeeker": "Think Seeker"
}