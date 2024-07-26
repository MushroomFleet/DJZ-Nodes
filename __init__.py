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



__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']