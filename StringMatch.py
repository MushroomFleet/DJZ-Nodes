import csv
import io

class StringMatch:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text_input": ("STRING", {
                    "multiline": True,
                    "default": ""
                }),
                "match_words": ("STRING", {
                    "multiline": False,
                    "default": ""
                }),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("matched_words",)
    FUNCTION = "match_strings"
    CATEGORY = "text"

    def match_strings(self, text_input, match_words):
        """
        Find matching words/phrases from match_words in text_input.
        Returns comma-separated string of found matches.
        """
        if not text_input or not match_words:
            return ("",)
        
        # Parse comma-separated match_words, handling quoted phrases
        try:
            # Use CSV reader to properly handle quoted strings
            reader = csv.reader(io.StringIO(match_words))
            words_to_match = next(reader)
            # Strip whitespace from each word/phrase
            words_to_match = [word.strip() for word in words_to_match if word.strip()]
        except:
            # Fallback to simple split if CSV parsing fails
            words_to_match = [word.strip() for word in match_words.split(",") if word.strip()]
        
        # Convert input text to lowercase for case-insensitive matching
        text_lower = text_input.lower()
        
        # Find matches
        found_matches = []
        for word in words_to_match:
            word_clean = word.strip()
            if word_clean and word_clean.lower() in text_lower:
                found_matches.append(word_clean)
        
        # Return comma-separated string of matches
        result = ", ".join(found_matches)
        return (result,)

# Node mappings for ComfyUI
NODE_CLASS_MAPPINGS = {
    "StringMatch": StringMatch
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "StringMatch": "String Match"
}