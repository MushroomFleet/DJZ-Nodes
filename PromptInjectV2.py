import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PromptInjectV2:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True}),
                "target": ("STRING", {
                    "multiline": False,
                    "default": "the scene is captured"
                }),
                "injection": ("STRING", {
                    "multiline": False,
                    "default": "Screeching tires."
                }),
                "inject_after": ("BOOLEAN", {
                    "default": False,
                    "label": "Inject After Target"
                })
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "inject_text"
    CATEGORY = "Custom-Nodes"

    def inject_text(self, text, target, injection, inject_after):
        import re
        
        # Clean up target and injection
        target_clean = target.strip()
        injection_clean = injection.strip()
        
        # Create pattern for target phrase
        pattern = re.escape(target_clean)
        
        # Wrap injection with spaces, ensuring single space if it ends with punctuation
        if injection_clean[-1] in '.!?':
            injection_wrapped = f" {injection_clean} "
        else:
            injection_wrapped = f" {injection_clean}  "
        
        # Inject the wrapped text before or after target based on inject_after parameter
        if inject_after:
            result = re.sub(pattern, f"{target_clean}{injection_wrapped}", text, flags=re.IGNORECASE)
        else:
            result = re.sub(pattern, f"{injection_wrapped}{target_clean}", text, flags=re.IGNORECASE)
        
        logger.info(f"Original text: {text}")
        logger.info(f"Target phrase: {target}")
        logger.info(f"Injection text: {injection}")
        logger.info(f"Inject after target: {inject_after}")
        logger.info(f"Modified text: {result}")
        
        return (result,)

    @classmethod
    def IS_CHANGED(cls, text, target, injection, inject_after):
        return (text, target, injection, inject_after)

NODE_CLASS_MAPPINGS = {
    "PromptInjectV2": PromptInjectV2
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptInjectV2": "Prompt Inject V2"
}
