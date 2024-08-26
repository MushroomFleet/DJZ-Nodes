NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

try:
    from .AspectSize import AspectSize
    NODE_CLASS_MAPPINGS["AspectSize"] = AspectSize
    NODE_DISPLAY_NAME_MAPPINGS["AspectSize"] = "Aspect Size"
except ImportError:
    print("Unable to import AspectSize. This node will not be available.")

try:
    from .AspectSizeV2 import AspectSizeV2
    NODE_CLASS_MAPPINGS["AspectSizeV2"] = AspectSizeV2
    NODE_DISPLAY_NAME_MAPPINGS["AspectSizeV2"] = "Aspect Size V2"
except ImportError:
    print("Unable to import AspectSizeV2. This node will not be available.")

try:
    from .ImageSizeAdjuster import ImageSizeAdjuster
    NODE_CLASS_MAPPINGS["ImageSizeAdjuster"] = ImageSizeAdjuster
    NODE_DISPLAY_NAME_MAPPINGS["ImageSizeAdjuster"] = "Image Size Adjuster"
except ImportError:
    print("Unable to import ImageSizeAdjuster. This node will not be available.")

try:
    from .ImageSizeAdjusterV2 import ImageSizeAdjusterV2
    NODE_CLASS_MAPPINGS["ImageSizeAdjusterV2"] = ImageSizeAdjusterV2
    NODE_DISPLAY_NAME_MAPPINGS["ImageSizeAdjusterV2"] = "Image Size Adjuster V2"
except ImportError:
    print("Unable to import ImageSizeAdjusterV2. This node will not be available.")

try:
    from .ZenkaiPrompt import ZenkaiPrompt
    NODE_CLASS_MAPPINGS["ZenkaiPrompt"] = ZenkaiPrompt
    NODE_DISPLAY_NAME_MAPPINGS["ZenkaiPrompt"] = "Zenkai-Prompt"
except ImportError:
    print("Unable to import ZenkaiPrompt. This node will not be available.")

try:
    from .ZenkaiPromptV2 import ZenkaiPromptV2
    NODE_CLASS_MAPPINGS["ZenkaiPromptV2"] = ZenkaiPromptV2
    NODE_DISPLAY_NAME_MAPPINGS["ZenkaiPromptV2"] = "Zenkai-Prompt V2"
except ImportError:
    print("Unable to import ZenkaiPromptV2. This node will not be available.")

try:
    from .ZenkaiWildcard import ZenkaiWildcard
    NODE_CLASS_MAPPINGS["ZenkaiWildcard"] = ZenkaiWildcard
    NODE_DISPLAY_NAME_MAPPINGS["ZenkaiWildcard"] = "Zenkai-Wildcard"
except ImportError:
    print("Unable to import ZenkaiWildcard. This node will not be available.")

try:
    from .ZenkaiWildcardV2 import ZenkaiWildcardV2
    NODE_CLASS_MAPPINGS["ZenkaiWildcardV2"] = ZenkaiWildcardV2
    NODE_DISPLAY_NAME_MAPPINGS["ZenkaiWildcardV2"] = "Zenkai-Wildcard V2"
except ImportError:
    print("Unable to import ZenkaiWildcardV2. This node will not be available.")

try:
    from .StringWeights import StringWeights
    NODE_CLASS_MAPPINGS["StringWeights"] = StringWeights
    NODE_DISPLAY_NAME_MAPPINGS["StringWeights"] = "String Weights"
except ImportError:
    print("Unable to import StringWeights. This node will not be available.")

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']