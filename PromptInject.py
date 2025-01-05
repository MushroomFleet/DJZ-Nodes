import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PromptInject:
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
                })
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "inject_text"
    CATEGORY = "Custom-Nodes"

    def inject_text(self, text, target, injection):
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
        
        # Inject the wrapped text before target
        result = re.sub(pattern, f"{injection_wrapped}{target_clean}", text, flags=re.IGNORECASE)
        
        logger.info(f"Original text: {text}")
        logger.info(f"Target phrase: {target}")
        logger.info(f"Injection text: {injection}")
        logger.info(f"Modified text: {result}")
        
        return (result,)

    @classmethod
    def IS_CHANGED(cls, text, target, injection):
        return (text, target, injection)

NODE_CLASS_MAPPINGS = {
    "PromptInject": PromptInject
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptInject": "Prompt Inject"
}
