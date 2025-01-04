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
    from .PromptCleaner import PromptCleaner
    NODE_CLASS_MAPPINGS["PromptCleaner"] = PromptCleaner
    NODE_DISPLAY_NAME_MAPPINGS["PromptCleaner"] = "Prompt Cleaner"
except ImportError:
    print("Unable to import PromptCleaner. This node will not be available.")

try:
    from .PromptSwap import PromptSwap
    NODE_CLASS_MAPPINGS["PromptSwap"] = PromptSwap
    NODE_DISPLAY_NAME_MAPPINGS["PromptSwap"] = "Prompt Swap"
except ImportError:
    print("Unable to import PromptSwap. This node will not be available.")


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

try:
    from .DjzDatamoshV5 import DjzDatamoshV5
    NODE_CLASS_MAPPINGS["DjzDatamoshV5"] = DjzDatamoshV5
    NODE_DISPLAY_NAME_MAPPINGS["DjzDatamoshV5"] = "Djz Datamosh V5 (Size Range)"
except ImportError:
    print("Unable to import DjzDatamoshV5. This node will not be available.")

try:
    from .DjzDatamoshV6 import DjzDatamoshV6
    NODE_CLASS_MAPPINGS["DjzDatamoshV6"] = DjzDatamoshV6
    NODE_DISPLAY_NAME_MAPPINGS["DjzDatamoshV6"] = "Djz Datamosh V6 (Pixel Sorting)"
except ImportError:
    print("Unable to import DjzDatamoshV6. This node will not be available.")

try:
    from .DjzDatamoshV7 import DjzDatamoshV7
    NODE_CLASS_MAPPINGS["DjzDatamoshV7"] = DjzDatamoshV7
    NODE_DISPLAY_NAME_MAPPINGS["DjzDatamoshV7"] = "Djz Pixel Sort V7 Advanced"
except ImportError:
    print("Unable to import DjzDatamoshV7. This node will not be available.")

try:
    from .BatchThief import BatchThief
    NODE_CLASS_MAPPINGS["BatchThief"] = BatchThief
    NODE_DISPLAY_NAME_MAPPINGS["BatchThief"] = "Batch Thief"
except ImportError:
    print("Unable to import BatchThief. This node will not be available.")

try:
    from .BatchRangeSwap import BatchRangeSwap
    NODE_CLASS_MAPPINGS["BatchRangeSwap"] = BatchRangeSwap
    NODE_DISPLAY_NAME_MAPPINGS["BatchRangeSwap"] = "Batch Range Swap"
except ImportError:
    print("Unable to import BatchRangeSwap. This node will not be available.")

try:
    from .LoadVideoDirectory import LoadVideoDirectory
    NODE_CLASS_MAPPINGS["LoadVideoDirectory"] = LoadVideoDirectory
    NODE_DISPLAY_NAME_MAPPINGS["LoadVideoDirectory"] = "Load Video Directory"
except ImportError:
    print("Unable to import LoadVideoDirectory. This node will not be available.")

try:
    from .BatchRangeInsert import BatchRangeInsert
    NODE_CLASS_MAPPINGS["BatchRangeInsert"] = BatchRangeInsert
    NODE_DISPLAY_NAME_MAPPINGS["BatchRangeInsert"] = "Batch Range Insert"
except ImportError:
    print("Unable to import BatchRangeInsert. This node will not be available.")

try:
    from .SequentialNumberGenerator import SequentialNumberGenerator
    NODE_CLASS_MAPPINGS["SequentialNumberGenerator"] = SequentialNumberGenerator
    NODE_DISPLAY_NAME_MAPPINGS["SequentialNumberGenerator"] = "Sequential Number Generator"
except ImportError:
    print("Unable to import SequentialNumberGenerator. This node will not be available.")

try:
    from .DinskyPlus import DinskyPlus
    NODE_CLASS_MAPPINGS["DinskyPlus"] = DinskyPlus
    NODE_DISPLAY_NAME_MAPPINGS["DinskyPlus"] = "Dinsky Plus Generator"
except ImportError:
    print("Unable to import DinskyPlus. This node will not be available.")

try:
    from .DinskyPlusV2 import DinskyPlusV2
    NODE_CLASS_MAPPINGS["DinskyPlusV2"] = DinskyPlusV2
    NODE_DISPLAY_NAME_MAPPINGS["DinskyPlusV2"] = "Dinsky Plus Generator V2"
except ImportError:
    print("Unable to import DinskyPlusV2. This node will not be available.")

try:
    from .TrianglesPlus import TrianglesPlus
    NODE_CLASS_MAPPINGS["TrianglesPlus"] = TrianglesPlus
    NODE_DISPLAY_NAME_MAPPINGS["TrianglesPlus"] = "Triangles Plus Generator"
except ImportError:
    print("Unable to import TrianglesPlus. This node will not be available.")

try:
    from .TrianglesPlusV2 import TrianglesPlusV2
    NODE_CLASS_MAPPINGS["TrianglesPlusV2"] = TrianglesPlusV2
    NODE_DISPLAY_NAME_MAPPINGS["TrianglesPlusV2"] = "Triangles Plus Generator V2"
except ImportError:
    print("Unable to import TrianglesPlusV2. This node will not be available.")

try:
    from .ParametricMeshGen import ParametricMeshGen
    NODE_CLASS_MAPPINGS["ParametricMeshGen"] = ParametricMeshGen
    NODE_DISPLAY_NAME_MAPPINGS["ParametricMeshGen"] = "Parametric Mesh Generator"
except ImportError:
    print("Unable to import ParametricMeshGen. This node will not be available.")

try:
    from .ParametricMeshGenV2 import ParametricMeshGenV2
    NODE_CLASS_MAPPINGS["ParametricMeshGenV2"] = ParametricMeshGenV2
    NODE_DISPLAY_NAME_MAPPINGS["ParametricMeshGenV2"] = "Parametric Mesh Generator V2"
except ImportError:
    print("Unable to import ParametricMeshGenV2. This node will not be available.")


try:
    from .FractalGenerator import FractalGenerator
    NODE_CLASS_MAPPINGS["FractalGenerator"] = FractalGenerator
    NODE_DISPLAY_NAME_MAPPINGS["FractalGenerator"] = "Fractal Art Generator"
except ImportError:
    print("Unable to import FractalGenerator. This node will not be available.")

try:
    from .FractalGeneratorV2 import FractalGeneratorV2
    NODE_CLASS_MAPPINGS["FractalGeneratorV2"] = FractalGeneratorV2
    NODE_DISPLAY_NAME_MAPPINGS["FractalGeneratorV2"] = "Fractal Art Generator V2"
except ImportError:
    print("Unable to import FractalGeneratorV2. This node will not be available.")

try:
    from .FractalGeneratorV3 import FractalGeneratorV3
    NODE_CLASS_MAPPINGS["FractalGeneratorV3"] = FractalGeneratorV3
    NODE_DISPLAY_NAME_MAPPINGS["FractalGeneratorV3"] = "Fractal Gen Cuda"
except ImportError:
    print("Unable to import FractalGeneratorV3. This node will not be available.")


__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
