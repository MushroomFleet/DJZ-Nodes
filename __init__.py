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

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']