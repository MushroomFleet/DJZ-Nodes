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

try:
    from .DatasetWordcloud import DatasetWordcloud
    NODE_CLASS_MAPPINGS["DatasetWordcloud"] = DatasetWordcloud
    NODE_DISPLAY_NAME_MAPPINGS["DatasetWordcloud"] = "Dataset Wordcloud"
except ImportError:
    print("Unable to import DatasetWordcloud. This node will not be available.")

try:
    from .LoadTextDirectory import LoadTextDirectory
    NODE_CLASS_MAPPINGS["LoadTextDirectory"] = LoadTextDirectory
    NODE_DISPLAY_NAME_MAPPINGS["LoadTextDirectory"] = "Load Text Directory"
except ImportError:
    print("Unable to import LoadTextDirectory. This node will not be available.")

try:
    from .PromptInject import PromptInject
    NODE_CLASS_MAPPINGS["PromptInject"] = PromptInject
    NODE_DISPLAY_NAME_MAPPINGS["PromptInject"] = "Prompt Inject"
except ImportError:
    print("Unable to import PromptInject. This node will not be available.")

try:
    from .PromptInjectV2 import PromptInjectV2
    NODE_CLASS_MAPPINGS["PromptInjectV2"] = PromptInjectV2
    NODE_DISPLAY_NAME_MAPPINGS["PromptInjectV2"] = "Prompt Inject V2"
except ImportError:
    print("Unable to import PromptInjectV2. This node will not be available.")

try:
    from .VHS_Effect_v1 import VHS_Effect_v1
    NODE_CLASS_MAPPINGS["VHS_Effect_v1"] = VHS_Effect_v1
    NODE_DISPLAY_NAME_MAPPINGS["VHS_Effect_v1"] = "VHS Effect v1"
except ImportError:
    print("Unable to import VHS_Effect_v1. This node will not be available.")

try:
    from .VHS_Effect_v2 import VHS_Effect_v2
    NODE_CLASS_MAPPINGS["VHS_Effect_v2"] = VHS_Effect_v2
    NODE_DISPLAY_NAME_MAPPINGS["VHS_Effect_v2"] = "VHS Effect v2"
except ImportError:
    print("Unable to import VHS_Effect_v2. This node will not be available.")

try:
    from .AnamorphicEffect import AnamorphicEffect
    NODE_CLASS_MAPPINGS["AnamorphicEffect"] = AnamorphicEffect
    NODE_DISPLAY_NAME_MAPPINGS["AnamorphicEffect"] = "Anamorphic Lens Effect"
except ImportError:
    print("Unable to import AnamorphicEffect. This node will not be available.")

try:
    from .Technicolor3Strip_v1 import Technicolor3Strip_v1
    NODE_CLASS_MAPPINGS["Technicolor3Strip_v1"] = Technicolor3Strip_v1
    NODE_DISPLAY_NAME_MAPPINGS["Technicolor3Strip_v1"] = "Technicolor 3-Strip v1"
except ImportError:
    print("Unable to import Technicolor3Strip_v1. This node will not be available.")

try:
    from .Technicolor3Strip_v2 import Technicolor3Strip_v2
    NODE_CLASS_MAPPINGS["Technicolor3Strip_v2"] = Technicolor3Strip_v2
    NODE_DISPLAY_NAME_MAPPINGS["Technicolor3Strip_v2"] = "Technicolor 3-Strip v2"
except ImportError:
    print("Unable to import Technicolor3Strip_v2. This node will not be available.")

try:
    from .PanavisionLensV2 import PanavisionLensV2
    NODE_CLASS_MAPPINGS["PanavisionLensV2"] = PanavisionLensV2
    NODE_DISPLAY_NAME_MAPPINGS["PanavisionLensV2"] = "Panavision Lens Effect V2"
except ImportError:
    print("Unable to import PanavisionLensV2. This node will not be available.")

try:
    from .KinescopeEffectV1 import KinescopeEffectV1
    NODE_CLASS_MAPPINGS["KinescopeEffectV1"] = KinescopeEffectV1
    NODE_DISPLAY_NAME_MAPPINGS["KinescopeEffectV1"] = "Kinescope Effect V1"
except ImportError:
    print("Unable to import KinescopeEffectV1. This node will not be available.")

try:
    from .VideoInterlaced import VideoInterlaced
    NODE_CLASS_MAPPINGS["VideoInterlaced"] = VideoInterlaced
    NODE_DISPLAY_NAME_MAPPINGS["VideoInterlaced"] = "Video Interlaced Upscaler"
except ImportError:
    print("Unable to import VideoInterlaced. This node will not be available.")

try:
    from .StringChaos import StringChaos
    NODE_CLASS_MAPPINGS["StringChaos"] = StringChaos
    NODE_DISPLAY_NAME_MAPPINGS["StringChaos"] = "String Chaos Modes"
except ImportError:
    print("Unable to import StringChaos. This node will not be available.")

try:
    from .CombineAudio import CombineAudio
    NODE_CLASS_MAPPINGS["CombineAudio"] = CombineAudio
    NODE_DISPLAY_NAME_MAPPINGS["CombineAudio"] = "Combine Audio Tracks"
except ImportError:
    print("Unable to import CombineAudio. This node will not be available.")

try:
    from .BlackBarsV1 import BlackBarsV1
    NODE_CLASS_MAPPINGS["BlackBarsV1"] = BlackBarsV1
    NODE_DISPLAY_NAME_MAPPINGS["BlackBarsV1"] = "Black Bars V1"
except ImportError:
    print("Unable to import BlackBarsV1. This node will not be available.")

try:
    from .BlackBarsV2 import BlackBarsV2
    NODE_CLASS_MAPPINGS["BlackBarsV2"] = BlackBarsV2
    NODE_DISPLAY_NAME_MAPPINGS["BlackBarsV2"] = "Black Bars V2"
except ImportError:
    print("Unable to import BlackBarsV2. This node will not be available.")

try:
    from .VideoInterlacedV2 import VideoInterlacedV2
    NODE_CLASS_MAPPINGS["VideoInterlacedV2"] = VideoInterlacedV2
    NODE_DISPLAY_NAME_MAPPINGS["VideoInterlacedV2"] = "Video Interlaced Upscaler V2"
except ImportError:
    print("Unable to import VideoInterlacedV2. This node will not be available.")

try:
    from .VHS_Effect_V3 import VHS_Effect_V3
    NODE_CLASS_MAPPINGS["VHS_Effect_V3"] = VHS_Effect_V3
    NODE_DISPLAY_NAME_MAPPINGS["VHS_Effect_V3"] = "VHS Effect V3"
except ImportError:
    print("Unable to import VHS_Effect_V3. This node will not be available.")

try:
    from .RetroVideoText import RetroVideoText
    NODE_CLASS_MAPPINGS["RetroVideoText"] = RetroVideoText
    NODE_DISPLAY_NAME_MAPPINGS["RetroVideoText"] = "Retro Video Text"
except ImportError:
    print("Unable to import RetroVideoText. This node will not be available.")

try:
    from .NonSquarePixelsV1 import NonSquarePixelsV1
    NODE_CLASS_MAPPINGS["NonSquarePixelsV1"] = NonSquarePixelsV1
    NODE_DISPLAY_NAME_MAPPINGS["NonSquarePixelsV1"] = "Non-Square Pixels V1"
except ImportError:
    print("Unable to import NonSquarePixelsV1. This node will not be available.")

try:
    from .BlackBarsV3 import BlackBarsV3
    NODE_CLASS_MAPPINGS["BlackBarsV3"] = BlackBarsV3
    NODE_DISPLAY_NAME_MAPPINGS["BlackBarsV3"] = "Black Bars V3"
except ImportError:
    print("Unable to import BlackBarsV3. This node will not be available.")

try:
    from .VideoInterlaceGANV3 import VideoInterlaceGANV3
    NODE_CLASS_MAPPINGS["VideoInterlaceGANV3"] = VideoInterlaceGANV3
    NODE_DISPLAY_NAME_MAPPINGS["VideoInterlaceGANV3"] = "GAN Video Interlaced Upscaler V3"
except ImportError:
    print("Unable to import VideoInterlaceGANV3. This node will not be available.")


try:
    from .VideoInterlaceFastV4 import VideoInterlaceFastV4
    NODE_CLASS_MAPPINGS["VideoInterlaceFastV4"] = VideoInterlaceFastV4
    NODE_DISPLAY_NAME_MAPPINGS["VideoInterlaceFastV4"] = "Fast Video Interlaced Upscaler V4"
except ImportError:
    print("Unable to import VideoInterlaceFastV4. This node will not be available.")

try:
    from .FilmGrainEffect import FilmGrainEffect
    NODE_CLASS_MAPPINGS["FilmGrainEffect"] = FilmGrainEffect
    NODE_DISPLAY_NAME_MAPPINGS["FilmGrainEffect"] = "Film Grain Effect (video)"
except ImportError:
    print("Unable to import FilmGrainEffect. This node will not be available.")

try:
    from .FilmGrainEffect_v2 import FilmGrainEffect_v2
    NODE_CLASS_MAPPINGS["FilmGrainEffect_v2"] = FilmGrainEffect_v2
    NODE_DISPLAY_NAME_MAPPINGS["FilmGrainEffect_v2"] = "Film Grain Effect V2 (video)"
except ImportError:
    print("Unable to import FilmGrainEffect_v2. This node will not be available.")

try:
    from .FishEyeEffect import FishEyeEffect
    NODE_CLASS_MAPPINGS["FishEyeEffect"] = FishEyeEffect
    NODE_DISPLAY_NAME_MAPPINGS["FishEyeEffect"] = "Fish Eye Effect"
except ImportError:
    print("Unable to import FishEyeEffect. This node will not be available.")

try:
    from .ClassicFilmEffect import ClassicFilmEffect
    NODE_CLASS_MAPPINGS["ClassicFilmEffect"] = ClassicFilmEffect
    NODE_DISPLAY_NAME_MAPPINGS["ClassicFilmEffect"] = "Classic Film Effect"
except ImportError:
    print("Unable to import ClassicFilmEffect. This node will not be available.")

try:
    from .VideoBitClamp import VideoBitClamp
    NODE_CLASS_MAPPINGS["VideoBitClamp"] = VideoBitClamp
    NODE_DISPLAY_NAME_MAPPINGS["VideoBitClamp"] = "Video Bit Clamp"
except ImportError:
    print("Unable to import VideoBitClamp. This node will not be available.")

try:
    from .ThreeToneStyler import ThreeToneStyler
    NODE_CLASS_MAPPINGS["ThreeToneStyler"] = ThreeToneStyler
    NODE_DISPLAY_NAME_MAPPINGS["ThreeToneStyler"] = "Three Tone Styler"
except ImportError:
    print("Unable to import ThreeToneStyler. This node will not be available.")

try:
    from .PromptDupeRemover import PromptDupeRemover
    NODE_CLASS_MAPPINGS["PromptDupeRemover"] = PromptDupeRemover
    NODE_DISPLAY_NAME_MAPPINGS["PromptDupeRemover"] = "Prompt Dupe-Remover"
except ImportError:
    print("Unable to import PromptDupeRemover. This node will not be available.")

try:
    from .ZenkaiPromptV3 import ZenkaiPromptV3
    NODE_CLASS_MAPPINGS["ZenkaiPromptV3"] = ZenkaiPromptV3
    NODE_DISPLAY_NAME_MAPPINGS["ZenkaiPromptV3"] = "Zenkai Prompt V3"
except ImportError:
    print("Unable to import ZenkaiPromptV3. This node will not be available.")

try:
    from .DjzDatamoshV8 import DjzDatamoshV8
    NODE_CLASS_MAPPINGS["DjzDatamoshV8"] = DjzDatamoshV8
    NODE_DISPLAY_NAME_MAPPINGS["DjzDatamoshV8"] = "Djz Pixel Sort V8 Advanced"
except ImportError:
    print("Unable to import DjzDatamoshV8. This node will not be available.")

try:
    from .ImageInterleavedUpscaler import ImageInterleavedUpscaler
    NODE_CLASS_MAPPINGS["ImageInterleavedUpscaler"] = ImageInterleavedUpscaler
    NODE_DISPLAY_NAME_MAPPINGS["ImageInterleavedUpscaler"] = "Image Interleaved Upscaler (720p to 1080i)"
except ImportError:
    print("Unable to import ImageInterleavedUpscaler. This node will not be available.")

try:
    from .WaveletDecompose import WaveletDecompose
    NODE_CLASS_MAPPINGS["WaveletDecompose"] = WaveletDecompose
    NODE_DISPLAY_NAME_MAPPINGS["WaveletDecompose"] = "Wavelet Decomposition"
except ImportError:
    print("Unable to import WaveletDecompose. This node will not be available.")

try:
    from .WaveletCompose import WaveletCompose
    NODE_CLASS_MAPPINGS["WaveletCompose"] = WaveletCompose
    NODE_DISPLAY_NAME_MAPPINGS["WaveletCompose"] = "Wavelet Composition"
except ImportError:
    print("Unable to import WaveletCompose. This node will not be available.")

try:
    from .JitterEffect import JitterEffect
    NODE_CLASS_MAPPINGS["JitterEffect"] = JitterEffect
    NODE_DISPLAY_NAME_MAPPINGS["JitterEffect"] = "Jitter Effect"
except ImportError:
    print("Unable to import JitterEffect. This node will not be available.")

try:
    from .FishEyeV2 import FishEyeV2
    NODE_CLASS_MAPPINGS["FishEyeV2"] = FishEyeV2
    NODE_DISPLAY_NAME_MAPPINGS["FishEyeV2"] = "Fish Eye Effects V2"
except ImportError:
    print("Unable to import FishEyeV2. This node will not be available.")

try:
    from .PromptDupeRemoverV2 import PromptDupeRemoverV2
    NODE_CLASS_MAPPINGS["PromptDupeRemoverV2"] = PromptDupeRemoverV2
    NODE_DISPLAY_NAME_MAPPINGS["PromptDupeRemoverV2"] = "Prompt Dupe Remover V2"
except ImportError:
    print("Unable to import PromptDupeRemoverV2. This node will not be available.")

try:
    from .ImageInterleavedUpscalerV2 import ImageInterleavedUpscalerV2
    NODE_CLASS_MAPPINGS["ImageInterleavedUpscalerV2"] = ImageInterleavedUpscalerV2
    NODE_DISPLAY_NAME_MAPPINGS["ImageInterleavedUpscalerV2"] = "Image Interleaved Upscaler V2"
except ImportError:
    print("Unable to import ImageInterleavedUpscalerV2. This node will not be available.")

try:
    from .NoiseFactory import NoiseFactory
    NODE_CLASS_MAPPINGS["NoiseFactory"] = NoiseFactory
    NODE_DISPLAY_NAME_MAPPINGS["NoiseFactory"] = "Noise Factory"
except ImportError:
    print("Unable to import NoiseFactory. This node will not be available.")

try:
    from .NoiseFactoryV2 import NoiseFactoryV2
    NODE_CLASS_MAPPINGS["NoiseFactoryV2"] = NoiseFactoryV2
    NODE_DISPLAY_NAME_MAPPINGS["NoiseFactoryV2"] = "Noise Factory V2"
except ImportError:
    print("Unable to import NoiseFactoryV2. This node will not be available.")

try:
    from .NoiseFactoryV3 import NoiseFactoryV3
    NODE_CLASS_MAPPINGS["NoiseFactoryV3"] = NoiseFactoryV3
    NODE_DISPLAY_NAME_MAPPINGS["NoiseFactoryV3"] = "Noise Factory V3"
except ImportError:
    print("Unable to import NoiseFactoryV3. This node will not be available.")

try:
    from .WinampViz import WinampViz
    NODE_CLASS_MAPPINGS["WinampViz"] = WinampViz
    NODE_DISPLAY_NAME_MAPPINGS["WinampViz"] = "🦙 Winamp Viz"
except ImportError:
    print("Unable to import WinampViz. This node will not be available.")

try:
    from .WinampVizV2 import WinampVizV2
    NODE_CLASS_MAPPINGS["WinampVizV2"] = WinampVizV2
    NODE_DISPLAY_NAME_MAPPINGS["WinampVizV2"] = "🦙 Winamp Viz V2"
except ImportError:
    print("Unable to import WinampVizV2. This node will not be available.")

try:
    from .VideoNoiseFactory import VideoNoiseFactory
    NODE_CLASS_MAPPINGS["VideoNoiseFactory"] = VideoNoiseFactory
    NODE_DISPLAY_NAME_MAPPINGS["VideoNoiseFactory"] = "Video Noise Factory"
except ImportError:
    print("Unable to import VideoNoiseFactory. This node will not be available.")

try:
    from .ZenkaiPromptV4 import ZenkaiPromptV4
    NODE_CLASS_MAPPINGS["ZenkaiPromptV4"] = ZenkaiPromptV4
    NODE_DISPLAY_NAME_MAPPINGS["ZenkaiPromptV4"] = "Zenkai Prompt V4"
except ImportError:
    print("Unable to import ZenkaiPromptV4. This node will not be available.")

try:
    from .VideoTimecode import VideoTimecode
    NODE_CLASS_MAPPINGS["VideoTimecode"] = VideoTimecode
    NODE_DISPLAY_NAME_MAPPINGS["VideoTimecode"] = "Video Timecode"
except ImportError:
    print("Unable to import VideoTimecode. This node will not be available.")

try:
    from .UncleanSpeech import UncleanSpeech
    NODE_CLASS_MAPPINGS["UncleanSpeech"] = UncleanSpeech
    NODE_DISPLAY_NAME_MAPPINGS["UncleanSpeech"] = "Unclean Speech"
except ImportError:
    print("Unable to import UncleanSpeech. This node will not be available.")

try:
    from .LoadVideoDirectoryV2 import LoadVideoDirectoryV2
    NODE_CLASS_MAPPINGS["LoadVideoDirectoryV2"] = LoadVideoDirectoryV2
    NODE_DISPLAY_NAME_MAPPINGS["LoadVideoDirectoryV2"] = "Load Video Directory V2"
except ImportError:
    print("Unable to import LoadVideoDirectoryV2. This node will not be available.")

try:
    from .VGA_Effect_v1 import VGA_Effect_v1
    NODE_CLASS_MAPPINGS["VGA_Effect_v1"] = VGA_Effect_v1
    NODE_DISPLAY_NAME_MAPPINGS["VGA_Effect_v1"] = "VGA Effect v1"
except ImportError:
    print("Unable to import VGA_Effect_v1. This node will not be available.")

try:
    from .VideoChromaticAberration import VideoChromaticAberration
    NODE_CLASS_MAPPINGS["VideoChromaticAberration"] = VideoChromaticAberration
    NODE_DISPLAY_NAME_MAPPINGS["VideoChromaticAberration"] = "Video Chromatic Aberration"
except ImportError:
    print("Unable to import VideoChromaticAberration. This node will not be available.")

try:
    from .CRT_Effect_v1 import CRT_Effect_v1
    NODE_CLASS_MAPPINGS["CRT_Effect_v1"] = CRT_Effect_v1
    NODE_DISPLAY_NAME_MAPPINGS["CRT_Effect_v1"] = "CRT Effect v1"
except ImportError:
    print("Unable to import CRT_Effect_v1. This node will not be available.")

try:
    from .MotionBlending import MotionBlending
    NODE_CLASS_MAPPINGS["MotionBlending"] = MotionBlending
    NODE_DISPLAY_NAME_MAPPINGS["MotionBlending"] = "Motion Blending"
except ImportError:
    print("Unable to import MotionBlending. This node will not be available.")

try:
    from .HalationBloom import HalationBloom
    NODE_CLASS_MAPPINGS["HalationBloom"] = HalationBloom
    NODE_DISPLAY_NAME_MAPPINGS["HalationBloom"] = "Halation Bloom"
except ImportError:
    print("Unable to import HalationBloom. This node will not be available.")

try:
    from .VideoFilmDamage import VideoFilmDamage
    NODE_CLASS_MAPPINGS["VideoFilmDamage"] = VideoFilmDamage
    NODE_DISPLAY_NAME_MAPPINGS["VideoFilmDamage"] = "Video Film Damage"
except ImportError:
    print("Unable to import VideoFilmDamage. This node will not be available.")

try:
    from .FilmGateWeave import FilmGateWeave
    NODE_CLASS_MAPPINGS["FilmGateWeave"] = FilmGateWeave
    NODE_DISPLAY_NAME_MAPPINGS["FilmGateWeave"] = "Film Gate Weave"
except ImportError:
    print("Unable to import FilmGateWeave. This node will not be available.")

try:
    from .VideoVignettingV1 import VideoVignettingV1
    NODE_CLASS_MAPPINGS["VideoVignettingV1"] = VideoVignettingV1
    NODE_DISPLAY_NAME_MAPPINGS["VideoVignettingV1"] = "Video VignettingV1"
except ImportError:
    print("Unable to import VideoVignettingV1. This node will not be available.")

try:
    from .VideoTemperatureV1 import VideoTemperatureV1
    NODE_CLASS_MAPPINGS["VideoTemperatureV1"] = VideoTemperatureV1
    NODE_DISPLAY_NAME_MAPPINGS["VideoTemperatureV1"] = "Video Temperature V1"
except ImportError:
    print("Unable to import VideoTemperatureV1. This node will not be available.")

try:
    from .KeyframeBasedUpscalerV1 import KeyframeBasedUpscalerV1
    NODE_CLASS_MAPPINGS["KeyframeBasedUpscalerV1"] = KeyframeBasedUpscalerV1
    NODE_DISPLAY_NAME_MAPPINGS["KeyframeBasedUpscalerV1"] = "Keyframe Based Upscaler V1"
except ImportError:
    print("Unable to import KeyframeBasedUpscalerV1. This node will not be available.")

try:
    from .VideoRingPainter import VideoRingPainter
    NODE_CLASS_MAPPINGS["VideoRingPainter"] = VideoRingPainter
    NODE_DISPLAY_NAME_MAPPINGS["VideoRingPainter"] = "Video Ring Painter"
except ImportError:
    print("Unable to import VideoRingPainter. This node will not be available.")

try:
    from .LensLeaks import LensLeaks
    NODE_CLASS_MAPPINGS["LensLeaks"] = LensLeaks
    NODE_DISPLAY_NAME_MAPPINGS["LensLeaks"] = "Lens Leaks"
except ImportError:
    print("Unable to import LensLeaks. This node will not be available.")

try:
    from .ScreensaverGenerator import ScreensaverGenerator
    NODE_CLASS_MAPPINGS["ScreensaverGenerator"] = ScreensaverGenerator
    NODE_DISPLAY_NAME_MAPPINGS["ScreensaverGenerator"] = "Screensaver Generator"
except ImportError:
    print("Unable to import ScreensaverGenerator. This node will not be available.")

try:
    from .DjzDatabendingV1 import DjzDatabendingV1
    NODE_CLASS_MAPPINGS["DjzDatabendingV1"] = DjzDatabendingV1
    NODE_DISPLAY_NAME_MAPPINGS["DjzDatabendingV1"] = "Djz Databending V1"
except ImportError:
    print("Unable to import DjzDatabendingV1. This node will not be available.")

try:
    from .VideoTrails import VideoTrails
    NODE_CLASS_MAPPINGS["VideoTrails"] = VideoTrails
    NODE_DISPLAY_NAME_MAPPINGS["VideoTrails"] = "Video Trails"
except ImportError:
    print("Unable to import VideoTrails. This node will not be available.")

try:
    from .VideoTrailsV2 import VideoTrailsV2
    NODE_CLASS_MAPPINGS["VideoTrailsV2"] = VideoTrailsV2
    NODE_DISPLAY_NAME_MAPPINGS["VideoTrailsV2"] = "Video Trails V2"
except ImportError:
    print("Unable to import VideoTrailsV2. This node will not be available.")

try:
    from .ScreensaverGeneratorV2 import ScreensaverGeneratorV2
    NODE_CLASS_MAPPINGS["ScreensaverGeneratorV2"] = ScreensaverGeneratorV2
    NODE_DISPLAY_NAME_MAPPINGS["ScreensaverGeneratorV2"] = "Screensaver Generator V2"
except ImportError:
    print("Unable to import ScreensaverGeneratorV2. This node will not be available.")

try:
    from .VideoMazeV1 import VideoMazeV1
    NODE_CLASS_MAPPINGS["VideoMazeV1"] = VideoMazeV1
    NODE_DISPLAY_NAME_MAPPINGS["VideoMazeV1"] = "Video Maze V1"
except ImportError:
    print("Unable to import VideoMazeV1. This node will not be available.")

try:
    from .VideoMazeV2 import VideoMazeV2
    NODE_CLASS_MAPPINGS["VideoMazeV2"] = VideoMazeV2
    NODE_DISPLAY_NAME_MAPPINGS["VideoMazeV2"] = "Video Maze V2"
except ImportError:
    print("Unable to import VideoMazeV2. This node will not be available.")

try:
    from .VideoCubeV1 import VideoCubeV1
    NODE_CLASS_MAPPINGS["VideoCubeV1"] = VideoCubeV1
    NODE_DISPLAY_NAME_MAPPINGS["VideoCubeV1"] = "Video Cube V1"
except ImportError:
    print("Unable to import VideoCubeV1. This node will not be available.")

try:
    from .VideoCorridorV1 import VideoCorridorV1
    NODE_CLASS_MAPPINGS["VideoCorridorV1"] = VideoCorridorV1
    NODE_DISPLAY_NAME_MAPPINGS["VideoCorridorV1"] = "Video Corridor V1"
except ImportError:
    print("Unable to import VideoCorridorV1. This node will not be available.")

try:
    from .CathodeRayEffect import CathodeRayEffect
    NODE_CLASS_MAPPINGS["CathodeRayEffect"] = CathodeRayEffect
    NODE_DISPLAY_NAME_MAPPINGS["CathodeRayEffect"] = "Cathode Ray Effect"
except ImportError:
    print("Unable to import CathodeRayEffect. This node will not be available.")

try:
    from .GSL_Filter_V1 import GSL_Filter_V1
    NODE_CLASS_MAPPINGS["GSL_Filter_V1"] = GSL_Filter_V1
    NODE_DISPLAY_NAME_MAPPINGS["GSL_Filter_V1"] = "GSL Filter v1"
except ImportError:
    print("Unable to import GSL_Filter_V1. This node will not be available.")

try:
    from .BatchAlphaComposite import BatchAlphaComposite
    NODE_CLASS_MAPPINGS["BatchAlphaComposite"] = BatchAlphaComposite
    NODE_DISPLAY_NAME_MAPPINGS["BatchAlphaComposite"] = "Batch Alpha Composite"
except ImportError:
    print("Unable to import BatchAlphaComposite. This node will not be available.")

try:
    from .DeadPixelEffect import DeadPixelEffect
    NODE_CLASS_MAPPINGS["DeadPixelEffect"] = DeadPixelEffect
    NODE_DISPLAY_NAME_MAPPINGS["DeadPixelEffect"] = "Dead Pixel Effect"
except ImportError:
    print("Unable to import DeadPixelEffect. This node will not be available.")

try:
    from .ScreensaverGeneratorV3 import ScreensaverGeneratorV3
    NODE_CLASS_MAPPINGS["ScreensaverGeneratorV3"] = ScreensaverGeneratorV3
    NODE_DISPLAY_NAME_MAPPINGS["ScreensaverGeneratorV3"] = "Screensaver Generator V3"
except ImportError:
    print("Unable to import ScreensaverGeneratorV3. This node will not be available.")

try:
    from .VideoPyramidV1 import VideoPyramidV1
    NODE_CLASS_MAPPINGS["VideoPyramidV1"] = VideoPyramidV1
    NODE_DISPLAY_NAME_MAPPINGS["VideoPyramidV1"] = "🎆 Video Pyramid Generator"
except ImportError:
    print("Unable to import VideoPyramidV1. This node will not be available.")

try:
    from .DepthBasedPixelization import DepthBasedPixelization
    NODE_CLASS_MAPPINGS["DepthBasedPixelization"] = DepthBasedPixelization
    NODE_DISPLAY_NAME_MAPPINGS["DepthBasedPixelization"] = "Depth-Based Pixelization"
except ImportError:
    print("Unable to import DepthBasedPixelization. This node will not be available.")

try:
    from .ThinkSeeker import ThinkSeeker
    NODE_CLASS_MAPPINGS["ThinkSeeker"] = ThinkSeeker
    NODE_DISPLAY_NAME_MAPPINGS["ThinkSeeker"] = "Think Tag Seeker"
except ImportError:
    print("Unable to import ThinkSeeker. This node will not be available.")

try:
    from .BracketCleaner import BracketCleaner
    NODE_CLASS_MAPPINGS["BracketCleaner"] = BracketCleaner
    NODE_DISPLAY_NAME_MAPPINGS["BracketCleaner"] = "BracketCleaner"
except ImportError:
    print("Unable to import BracketCleaner. This node will not be available.")

try:
    from .PromptCleanerV2 import PromptCleanerV2
    NODE_CLASS_MAPPINGS["PromptCleanerV2"] = PromptCleanerV2
    NODE_DISPLAY_NAME_MAPPINGS["PromptCleanerV2"] = "Prompt Cleaner V2"
except ImportError:
    print("Unable to import PromptCleanerV2. This node will not be available.")

try:
    from .ZenkaiPoseMap import ZenkaiPoseMap
    NODE_CLASS_MAPPINGS["ZenkaiPoseMap"] = ZenkaiPoseMap
    NODE_DISPLAY_NAME_MAPPINGS["ZenkaiPoseMap"] = "Zenkai Pose Map"
except ImportError:
    print("Unable to import ZenkaiPoseMap. This node will not be available.")

try:
    from .VoiceEffects import VoiceEffects
    NODE_CLASS_MAPPINGS["VoiceEffects"] = VoiceEffects
    NODE_DISPLAY_NAME_MAPPINGS["VoiceEffects"] = "🎤 Voice Effects"
except ImportError:
    print("Unable to import VoiceEffects. This node will not be available.")

try:
    from .VoiceEffects2 import VoiceEffects2
    NODE_CLASS_MAPPINGS["VoiceEffects2"] = VoiceEffects2
    NODE_DISPLAY_NAME_MAPPINGS["VoiceEffects2"] = "🎤 Voice Effects 2"
except ImportError:
    print("Unable to import VoiceEffects2. This node will not be available.")

try:
    from .ZenkaiImagePromptV1 import ZenkaiImagePromptV1
    NODE_CLASS_MAPPINGS["ZenkaiImagePromptV1"] = ZenkaiImagePromptV1
    NODE_DISPLAY_NAME_MAPPINGS["ZenkaiImagePromptV1"] = "Zenkai Image Prompt V1"
except ImportError:
    print("Unable to import ZenkaiImagePromptV1. This node will not be available.")

try:
    from .PromptInjectV2 import PromptInjectV2
    NODE_CLASS_MAPPINGS["PromptInjectV2"] = PromptInjectV2
    NODE_DISPLAY_NAME_MAPPINGS["PromptInjectV2"] = "Prompt Inject V2"
except ImportError:
    print("Unable to import PromptInjectV2. This node will not be available.")

try:
    from .ZenkaiPromptV5 import ZenkaiPromptV5
    NODE_CLASS_MAPPINGS["ZenkaiPromptV5"] = ZenkaiPromptV5
    NODE_DISPLAY_NAME_MAPPINGS["ZenkaiPromptV5"] = "Zenkai Prompt V5"
except ImportError:
    print("Unable to import ZenkaiPromptV5. This node will not be available.")

try:
    from .ZenkaiImagePromptV2 import ZenkaiImagePromptV2
    NODE_CLASS_MAPPINGS["ZenkaiImagePromptV2"] = ZenkaiImagePromptV2
    NODE_DISPLAY_NAME_MAPPINGS["ZenkaiImagePromptV2"] = "Zenkai Image Prompt V2"
except ImportError:
    print("Unable to import ZenkaiImagePromptV2. This node will not be available.")

try:
    from .ProjectFolderPathNode import ProjectFolderPathNode
    NODE_CLASS_MAPPINGS["ProjectFolderPathNode"] = ProjectFolderPathNode
    NODE_DISPLAY_NAME_MAPPINGS["ProjectFolderPathNode"] = "Project Folder Path Node"
except ImportError:
    print("Unable to import ProjectFolderPathNode. This node will not be available.")

try:
    from .Zenkai_IMPv1 import Zenkai_IMPv1
    NODE_CLASS_MAPPINGS["Zenkai_IMPv1"] = Zenkai_IMPv1
    NODE_DISPLAY_NAME_MAPPINGS["Zenkai_IMPv1"] = "Zenkai IMP v1"
except ImportError:
    print("Unable to import Zenkai_IMPv1. This node will not be available.")

try:
    from .ZenkaiControlPromptV1 import ZenkaiControlPromptV1
    NODE_CLASS_MAPPINGS["ZenkaiControlPromptV1"] = ZenkaiControlPromptV1
    NODE_DISPLAY_NAME_MAPPINGS["ZenkaiControlPromptV1"] = "Zenkai Control Prompt V1"
except ImportError:
    print("Unable to import ZenkaiControlPromptV1. This node will not be available.")

try:
    from .ZenkaiDepthPrompt import ZenkaiDepthPrompt
    NODE_CLASS_MAPPINGS["ZenkaiDepthPrompt"] = ZenkaiDepthPrompt
    NODE_DISPLAY_NAME_MAPPINGS["ZenkaiDepthPrompt"] = "Zenkai Depth Prompt"
except ImportError:
    print("Unable to import ZenkaiDepthPrompt. This node will not be available.")

try:
    from .VideoText import VideoText
    NODE_CLASS_MAPPINGS["VideoText"] = VideoText
    NODE_DISPLAY_NAME_MAPPINGS["VideoText"] = "Video Text"
except ImportError:
    print("Unable to import VideoText. This node will not be available.")

try:
    from .BorderCompositeAlpha import BorderCompositeAlpha
    NODE_CLASS_MAPPINGS["BorderCompositeAlpha"] = BorderCompositeAlpha
    NODE_DISPLAY_NAME_MAPPINGS["BorderCompositeAlpha"] = "Border Composite Alpha"
except ImportError:
    print("Unable to import BorderCompositeAlpha. This node will not be available.")


__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
