import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PromptSwap:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True}),
                "target_words": ("STRING", {
                    "multiline": False,
                    "default": "man, woman, \"no humans\""
                }),
                "exchange_words": ("STRING", {
                    "multiline": False,
                    "default": "woman, man, \"many monsters\""
                })
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "swap_words"
    CATEGORY = "Custom-Nodes"

    def swap_words(self, text, target_words, exchange_words):
        import re
        
        def split_with_quotes(s):
            # Pattern matches either a quoted string or a non-comma string
            pattern = r'"([^"]*)"|\s*([^,]+)'
            matches = re.finditer(pattern, s)
            return [match.group(1) or match.group(2).strip() for match in matches if match.group(1) or match.group(2).strip()]
        
        # Split and get the raw phrases/words
        targets = split_with_quotes(target_words)
        exchanges = split_with_quotes(exchange_words)
        
        # Create word mapping dictionary, stripping quotes for storage
        word_map = {}
        for target, exchange in zip(targets, exchanges):
            # Remove quotes if present
            target_clean = target.strip('"').strip().lower()
            exchange_clean = exchange.strip('"').strip()
            word_map[target_clean] = exchange_clean
        
        # Sort targets by length (descending) to match longer phrases first
        sorted_targets = sorted(word_map.keys(), key=len, reverse=True)
        
        # Process the text
        result = text
        for target in sorted_targets:
            # For multi-word phrases (containing space), don't use word boundaries
            if ' ' in target:
                pattern = re.escape(target)
            else:
                pattern = r'\b' + re.escape(target) + r'\b'
            
            result = re.sub(pattern, word_map[target], result, flags=re.IGNORECASE)
        
        logger.info(f"Original text: {text}")
        logger.info(f"Target words: {target_words}")
        logger.info(f"Exchange words: {exchange_words}")
        logger.info(f"Swapped text: {result}")
        
        return (result,)

    @classmethod
    def IS_CHANGED(cls, text, target_words, exchange_words):
        return (text, target_words, exchange_words)

NODE_CLASS_MAPPINGS = {
    "PromptSwap": PromptSwap
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptSwap": "Prompt Swap"
}
