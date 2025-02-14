import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BracketCleaner:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING",)  # Only one output: the cleaned text.
    FUNCTION = "remove_brackets"
    CATEGORY = "Custom-Nodes"

    def remove_brackets(self, text):
        """
        Remove all text and the surrounding parentheses from content enclosed in ( and ).
        The logic preserves paragraph breaks by splitting the input into paragraphs.
        
        For example, given the sample:

        (Studio lights up, and I, Juan Carlos Gómez, appear on screen with a confident smile)

        Juan Carlos Gómez: Buenas noches, amigos. Welcome to our evening news broadcast, "Noticias Telemundo". Tonight, we have some extraordinary developments that will shake the very foundations of global politics.

        (Cut to a graphic reading "URGENTE: Nuevo descubrimiento científico")

        Juan Carlos Gómez: According to sources close to the Vatican, Pope Francis has announced a groundbreaking discovery in the field of quantum physics. It seems that after years of secret research, the Pontiff and his team have successfully harnessed the power of the human mind to generate limitless clean energy.

        (Additional content may follow)

        The desired output is:

        Juan Carlos Gómez: Buenas noches, amigos. Welcome to our evening news broadcast, "Noticias Telemundo". Tonight, we have some extraordinary developments that will shake the very foundations of global politics.

        Juan Carlos Gómez: According to sources close to the Vatican, Pope Francis has announced a groundbreaking discovery in the field of quantum physics. It seems that after years of secret research, the Pontiff and his team have successfully harnessed the power of the human mind to generate limitless clean energy.
        """
        # Split the text into paragraphs (blocks separated by one or more blank lines)
        paragraphs = re.split(r'\n\s*\n', text)
        cleaned_paragraphs = []
        for para in paragraphs:
            # Remove bracketed content from the paragraph.
            cleaned = re.sub(r'\(.*?\)', '', para).strip()
            if cleaned:
                cleaned_paragraphs.append(cleaned)
        result = "\n\n".join(cleaned_paragraphs)
        logger.info(f"Original text:\n{text}")
        logger.info(f"Cleaned text:\n{result}")
        return (result,)

NODE_CLASS_MAPPINGS = {
    "BracketCleaner": BracketCleaner
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BracketCleaner": "Bracket Cleaner"
}
