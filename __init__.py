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

try:
    from .StringPainter import StringPainter
    NODE_CLASS_MAPPINGS["StringPainter"] = StringPainter
    NODE_DISPLAY_NAME_MAPPINGS["StringPainter"] = "String Painter"
except ImportError:
    print("Unable to import StringPainter. This node will not be available.")

try:
    from .StringPainterV2 import StringPainterV2
    NODE_CLASS_MAPPINGS["StringPainterV2"] = StringPainterV2
    NODE_DISPLAY_NAME_MAPPINGS["StringPainterV2"] = "String Painter V2"
except ImportError:
    print("Unable to import StringPainterV2. This node will not be available.")

try:
    from .FFXFADEORAMA import FFXFADEORAMA
    NODE_CLASS_MAPPINGS["FFXFADEORAMA"] = FFXFADEORAMA
    NODE_DISPLAY_NAME_MAPPINGS["FFXFADEORAMA"] = "FFX Fade-O-Rama"
except ImportError:
    print("Unable to import FFXFADEORAMA. This node will not be available.")

try:
    from .ProjectFilePathNode import ProjectFilePathNode
    NODE_CLASS_MAPPINGS["ProjectFilePathNode"] = ProjectFilePathNode
    NODE_DISPLAY_NAME_MAPPINGS["ProjectFilePathNode"] = "Project File Path Generator"
except ImportError:
    print("Unable to import ProjectFilePathNode. This node will not be available.")

try:
    from .CaptionsToPromptList import CaptionsToPromptList
    NODE_CLASS_MAPPINGS["CaptionsToPromptList"] = CaptionsToPromptList
    NODE_DISPLAY_NAME_MAPPINGS["CaptionsToPromptList"] = "Captions To Prompt List"
except ImportError:
    print("Unable to import CaptionsToPromptList. This node will not be available.")

try:
    from .ImageSizeAdjusterV3 import ImageSizeAdjusterV3
    NODE_CLASS_MAPPINGS["ImageSizeAdjusterV3"] = ImageSizeAdjusterV3
    NODE_DISPLAY_NAME_MAPPINGS["ImageSizeAdjusterV3"] = "Image Size Adjuster V3"
except ImportError:
    print("Unable to import ImageSizeAdjusterV3. This node will not be available.")

try:
    from .DJZLoadLatent import DJZLoadLatent
    NODE_CLASS_MAPPINGS["DJZ-LoadLatent"] = DJZLoadLatent
    NODE_DISPLAY_NAME_MAPPINGS["DJZ-LoadLatent"] = "DJZ Load Latent"
except ImportError:
    print("Unable to import DJZ-LoadLatent. This node will not be available.")

try:
    from .DJZLoadLatentV2 import DJZLoadLatentV2
    NODE_CLASS_MAPPINGS["DJZ-LoadLatentV2"] = DJZLoadLatentV2
    NODE_DISPLAY_NAME_MAPPINGS["DJZ-LoadLatentV2"] = "DJZ Load Latent V2"
except ImportError:
    print("Unable to import DJZ-LoadLatentV2. This node will not be available.")

try:
    from .SaveText import SaveText
    NODE_CLASS_MAPPINGS["SaveText"] = SaveText
    NODE_DISPLAY_NAME_MAPPINGS["SaveText"] = "Save Text"
except ImportError:
    print("Unable to import SaveText. This node will not be available.")

try:
    from .LoadVideoBatchFrame import LoadVideoBatchFrame
    NODE_CLASS_MAPPINGS["LoadVideoBatchFrame"] = LoadVideoBatchFrame
    NODE_DISPLAY_NAME_MAPPINGS["LoadVideoBatchFrame"] = "Load Video Batch Frame"
except ImportError:
    print("Unable to import LoadVideoBatchFrame. This node will not be available.")

try:
    from .BatchOffset import BatchOffset
    NODE_CLASS_MAPPINGS["BatchOffset"] = BatchOffset
    NODE_DISPLAY_NAME_MAPPINGS["BatchOffset"] = "Batch Offset"
except ImportError:
    print("Unable to import BatchOffset. This node will not be available.")
    
try:
    from .DjzDatamosh import DJZDatamosh
    NODE_CLASS_MAPPINGS["DJZDatamosh"] = DJZDatamosh
    NODE_DISPLAY_NAME_MAPPINGS["DJZDatamosh"] = "DJZ Datamosh"
except ImportError:
    print("Unable to import DJZDatamosh. This node will not be available.")
    
try:
    from .DJZDatamoshV2 import DJZDatamoshV2
    NODE_CLASS_MAPPINGS["DJZDatamoshV2"] = DJZDatamoshV2
    NODE_DISPLAY_NAME_MAPPINGS["DJZDatamoshV2"] = "DJZ Datamosh V2"
except ImportError:
    print("Unable to import DJZDatamoshV2. This node will not be available.")

try:
    from .DjzDatamoshV3 import DjzDatamoshV3
    NODE_CLASS_MAPPINGS["DjzDatamoshV3"] = DjzDatamoshV3
    NODE_DISPLAY_NAME_MAPPINGS["DjzDatamoshV3"] = "Djz Datamosh V3"
except ImportError:
    print("Unable to import DjzDatamoshV3. This node will not be available.")

try:
    from .DjzDatamoshV4 import DjzDatamoshV4
    NODE_CLASS_MAPPINGS["DjzDatamoshV4"] = DjzDatamoshV4
    NODE_DISPLAY_NAME_MAPPINGS["DjzDatamoshV4"] = "Djz Datamosh V4 (Style Transfer)"
except ImportError:
    print("Unable to import DjzDatamoshV4. This node will not be available.")

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']