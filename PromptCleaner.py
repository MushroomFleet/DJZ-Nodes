import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PromptCleaner:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True}),
                "words_to_remove": ("STRING", {
                    "multiline": False,
                    "default": "man, woman, world"
                })
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "clean_prompt"
    CATEGORY = "Custom-Nodes"

    def clean_prompt(self, text, words_to_remove):
        # Split the words to remove and strip whitespace
        remove_words = [word.strip().lower() for word in words_to_remove.split(',')]
        
        # Split the input text into words, preserving punctuation
        import re
        words = re.findall(r'\b\w+\b|[^\w\s]', text)
        
        # Filter out the words that should be removed (case insensitive)
        cleaned_words = []
        skip_next = False
        for i, word in enumerate(words):
            word_lower = word.lower()
            # Skip if word is in remove list
            if word_lower in remove_words:
                continue
            # Add punctuation and words not in remove list
            cleaned_words.append(word)
        
        # Join the remaining words back together
        cleaned_text = ' '.join(cleaned_words)
        
        logger.info(f"Original text: {text}")
        logger.info(f"Words removed: {words_to_remove}")
        logger.info(f"Cleaned text: {cleaned_text}")
        
        return (cleaned_text,)

    @classmethod
    def IS_CHANGED(cls, text, words_to_remove):
        return (text, words_to_remove)

NODE_CLASS_MAPPINGS = {
    "PromptCleaner": PromptCleaner
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptCleaner": "Prompt Cleaner"
}
