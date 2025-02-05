import logging
import re
import ast

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PromptDupeRemoverV2:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True}),
                "preserve_case": ("BOOLEAN", {
                    "default": True, 
                    "label": "Preserve Original Case"
                }),
                "whitelist": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "label": "Whitelist (comma-separated, use quotes for multi-word terms)"
                })
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "remove_duplicates"
    CATEGORY = "Custom-Nodes"

    def parse_whitelist(self, whitelist_text):
        """Parse the whitelist string into a set of terms."""
        if not whitelist_text.strip():
            return set()
        
        # Custom parser for the whitelist
        terms = []
        current_term = []
        in_quotes = False
        
        for char in whitelist_text.strip() + ',':  # Add comma to handle last term
            if char == '"':
                in_quotes = not in_quotes
            elif char == ',' and not in_quotes:
                if current_term:
                    term = ''.join(current_term).strip()
                    if term.startswith('"') and term.endswith('"'):
                        term = term[1:-1]
                    if term:
                        terms.append(term)
                    current_term = []
            else:
                current_term.append(char)
        
        # Convert to set for efficient lookup
        whitelist = {term.lower() for term in terms if term}
        logger.info(f"Parsed whitelist terms: {whitelist}")
        return whitelist

    def remove_duplicates(self, text, preserve_case=True, whitelist=""):
        # Parse the whitelist
        whitelist_terms = self.parse_whitelist(whitelist)
        
        # Split the input text into words and punctuation
        tokens = re.findall(r'\b\w+\b|\s+|[^\w\s]', text)
        
        # Keep track of seen words (case insensitive)
        seen_words = set()
        cleaned_tokens = []
        
        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            # If it's whitespace or punctuation, keep it
            if not token.strip() or not token.isalnum():
                cleaned_tokens.append(token)
                i += 1
                continue
            
            # Check for multi-word whitelist terms
            found_whitelist_term = False
            for term in whitelist_terms:
                term_words = term.split()
                if len(term_words) > 1:
                    # Try to match multi-word term
                    potential_match = []
                    for j in range(len(term_words)):
                        if (i + j) < len(tokens) and tokens[i + j].lower() == term_words[j].lower():
                            potential_match.append(tokens[i + j])
                        else:
                            break
                    
                    if len(potential_match) == len(term_words):
                        # Found a multi-word whitelist term
                        cleaned_tokens.extend(potential_match)
                        i += len(term_words)
                        found_whitelist_term = True
                        break
            
            if found_whitelist_term:
                continue
                
            # Handle single words
            word_lower = token.lower()
            
            # If word is in whitelist or hasn't been seen before
            if word_lower in whitelist_terms or word_lower not in seen_words:
                cleaned_tokens.append(token if preserve_case else word_lower)
                if word_lower not in whitelist_terms:
                    seen_words.add(word_lower)
            
            i += 1
        
        # Join the remaining tokens back together
        cleaned_text = ''.join(cleaned_tokens)
        
        logger.info(f"Original text: {text}")
        logger.info(f"Whitelist terms: {whitelist_terms}")
        logger.info(f"Duplicate words removed: {len(tokens) - len(cleaned_tokens)} tokens removed")
        logger.info(f"Cleaned text: {cleaned_text}")
        
        return (cleaned_text,)

    @classmethod
    def IS_CHANGED(cls, text, preserve_case, whitelist):
        return (text, preserve_case, whitelist)

NODE_CLASS_MAPPINGS = {
    "PromptDupeRemoverV2": PromptDupeRemoverV2
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptDupeRemoverV2": "Prompt Duplicate Remover V2"
}