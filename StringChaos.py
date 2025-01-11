import logging
import random
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StringChaos:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True}),
                "mode": (["L33T", "aLtErNaTiNg", "SCRAMBLED", "EMOJI", "ZALGO", "REDACTED"],),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 0xffffffffffffffff
                }),
                "intensity": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.1
                })
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "transform_text"
    CATEGORY = "Custom-Nodes"

    def __init__(self):
        # L33T speak mapping
        self.leet_map = {
            'a': ['4', '@'],
            'b': ['8', '|3'],
            'e': ['3'],
            'g': ['6', '9'],
            'i': ['1', '!'],
            'l': ['1', '|'],
            'o': ['0'],
            's': ['5', '$'],
            't': ['7', '+'],
            'z': ['2']
        }
        
        # Emoji mapping
        self.emoji_map = {
            'hello': ['👋', '💫'],
            'world': ['🌍', '🌎', '🌏'],
            'love': ['❤️', '💕', '💗'],
            'happy': ['😊', '😃', '🌟'],
            'sad': ['😢', '😔'],
            'good': ['👍', '✨'],
            'bad': ['👎', '💢'],
            'yes': ['✅', '👍'],
            'no': ['❌', '👎'],
            'time': ['⌚', '⏰'],
            'money': ['💰', '💵'],
            'work': ['💼', '💪'],
            'home': ['🏠', '🏡']
        }

        # Zalgo characters
        self.zalgo_chars = [
            '\u0300', '\u0301', '\u0302', '\u0303', '\u0304', '\u0305', '\u0306',
            '\u0307', '\u0308', '\u0309', '\u030A', '\u030B', '\u030C', '\u030D',
            '\u030E', '\u030F', '\u0310', '\u0311', '\u0312', '\u0313', '\u0314',
            '\u0315', '\u0316', '\u0317', '\u0318', '\u0319', '\u031A', '\u031B',
            '\u031C', '\u031D', '\u031E', '\u031F', '\u0320', '\u0321', '\u0322',
            '\u0323', '\u0324', '\u0325', '\u0326', '\u0327', '\u0328', '\u0329',
            '\u032A', '\u032B', '\u032C', '\u032D', '\u032E', '\u032F', '\u0330'
        ]

    def transform_text(self, text, mode, seed, intensity):
        # Set the random seed for deterministic output
        random.seed(seed)
        
        if mode == "L33T":
            return (self._convert_to_leet(text),)
        elif mode == "aLtErNaTiNg":
            return (self._convert_to_alternating(text),)
        elif mode == "SCRAMBLED":
            return (self._scramble_text(text),)
        elif mode == "EMOJI":
            return (self._add_emojis(text),)
        elif mode == "ZALGO":
            return (self._zalgofy(text, intensity),)
        elif mode == "REDACTED":
            return (self._redact_text(text, intensity),)
        
        # Default fallback
        return (text,)

    def _convert_to_leet(self, text):
        result = []
        for char in text:
            char_lower = char.lower()
            if char_lower in self.leet_map:
                leet_char = random.choice(self.leet_map[char_lower])
                result.append(leet_char.upper() if char.isupper() else leet_char)
            else:
                result.append(char)
        return ''.join(result)

    def _convert_to_alternating(self, text):
        return ''.join(c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(text))

    def _scramble_text(self, text):
        # Preserve words and punctuation
        words = re.findall(r'\b\w+\b|[^\w\s]|\s+', text)
        result = []
        
        for word in words:
            if len(word) <= 1 or not word.isalpha():
                result.append(word)
            else:
                # Keep first and last letters, scramble middle
                middle = list(word[1:-1])
                random.shuffle(middle)
                result.append(word[0] + ''.join(middle) + word[-1])
        
        return ''.join(result)

    def _add_emojis(self, text):
        words = text.split()
        result = []
        
        for word in words:
            result.append(word)
            word_lower = word.lower()
            
            # Check if the word has an associated emoji
            if word_lower in self.emoji_map:
                result.append(random.choice(self.emoji_map[word_lower]))
            
        return ' '.join(result)

    def _zalgofy(self, text, intensity):
        result = []
        for char in text:
            result.append(char)
            
            # Add random zalgo characters based on intensity
            zalgo_count = int(random.uniform(1, 15) * intensity)
            for _ in range(zalgo_count):
                result.append(random.choice(self.zalgo_chars))
                
        return ''.join(result)

    def _redact_text(self, text, intensity):
        result = []
        for char in text:
            if char.isspace():
                result.append(char)
            elif random.random() < intensity:
                result.append('█')
            else:
                result.append(char)
        return ''.join(result)

    @classmethod
    def IS_CHANGED(cls, text, mode, seed, intensity):
        return (text, mode, seed, intensity)

NODE_CLASS_MAPPINGS = {
    "StringChaos": StringChaos
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "StringChaos": "String Chaos Modes"
}