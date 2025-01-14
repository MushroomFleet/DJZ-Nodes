import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PromptDupeRemover:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True}),
                "preserve_case": ("BOOLEAN", {
                    "default": True, 
                    "label": "Preserve Original Case"
                })
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "remove_duplicates"
    CATEGORY = "Custom-Nodes"

    def remove_duplicates(self, text, preserve_case=True):
        # Split the input text into words, preserving punctuation
        import re
        words = re.findall(r'\b\w+\b|[^\w\s]', text)
        
        # Keep track of seen words (case insensitive)
        seen_words = set()
        cleaned_words = []
        
        for word in words:
            # Skip punctuation
            if not word.isalnum():
                cleaned_words.append(word)
                continue
                
            # Check for duplicates using lowercase for comparison
            word_lower = word.lower()
            if word_lower not in seen_words:
                # Add the original word if preserving case, otherwise use lowercase
                cleaned_words.append(word if preserve_case else word_lower)
                seen_words.add(word_lower)
        
        # Join the remaining words back together
        cleaned_text = ' '.join(cleaned_words)
        
        logger.info(f"Original text: {text}")
        logger.info(f"Duplicate words removed: {len(words) - len(cleaned_words)} words removed")
        logger.info(f"Cleaned text: {cleaned_text}")
        
        return (cleaned_text,)

    @classmethod
    def IS_CHANGED(cls, text, preserve_case):
        return (text, preserve_case)

NODE_CLASS_MAPPINGS = {
    "PromptDupeRemover": PromptDupeRemover
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptDupeRemover": "Prompt Duplicate Remover"
}