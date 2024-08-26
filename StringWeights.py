import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StringWeights:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True}),
                "weight": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 10.0,
                    "step": 0.1
                })
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "apply_weight"
    CATEGORY = "Custom-Nodes"

    def apply_weight(self, text, weight):
        weighted_string = f"({text}:{weight:.1f})"  # Format weight to one decimal place
        logger.info(f"Original text: {text}")
        logger.info(f"Weighted string: {weighted_string}")
        return (weighted_string,)

    @classmethod
    def IS_CHANGED(cls, text, weight):
        # This ensures the node updates when either text or weight changes
        return (text, weight)

NODE_CLASS_MAPPINGS = {
    "StringWeights": StringWeights
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "StringWeights": "String Weights"
}