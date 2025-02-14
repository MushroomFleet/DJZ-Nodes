import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PromptCleanerV2:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True}),
                "words_to_remove": ("STRING", {
                    "multiline": False,
                    "default": "man, woman, world"
                }),
                "phrase_to_remove": ("STRING", {
                    "multiline": False,
                    "default": ""
                })
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "clean_prompt"
    CATEGORY = "Custom-Nodes"

    def clean_prompt(self, text, words_to_remove, phrase_to_remove):
        # If a phrase is provided, remove it from the original text preserving formatting
        if phrase_to_remove:
            pattern = re.compile(re.escape(phrase_to_remove), re.IGNORECASE)
            result_text = pattern.sub("", text)
            logger.info(f"Phrase removed: {phrase_to_remove}")
            logger.info(f"Original text: {text}")
            logger.info(f"Result text: {result_text}")
            return (result_text,)
        else:
            # Split the words to remove and strip whitespace
            remove_words = [word.strip().lower() for word in words_to_remove.split(',')]
            
            # Split the input text into words, preserving punctuation
            words = re.findall(r'\b\w+\b|[^\w\s]', text)
            
            # Filter out the words that should be removed (case insensitive)
            cleaned_words = []
            for word in words:
                if word.lower() in remove_words:
                    continue
                cleaned_words.append(word)
            
            # Join the remaining words back together
            cleaned_text = ' '.join(cleaned_words)
            
            logger.info(f"Original text: {text}")
            logger.info(f"Words removed: {words_to_remove}")
            logger.info(f"Cleaned text: {cleaned_text}")
            
            return (cleaned_text,)

    @classmethod
    def IS_CHANGED(cls, text, words_to_remove, phrase_to_remove):
        return (text, words_to_remove, phrase_to_remove)

NODE_CLASS_MAPPINGS = {
    "PromptCleanerV2": PromptCleanerV2
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptCleanerV2": "Prompt Cleaner V2"
}
