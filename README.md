# DJZ-Nodes

A comprehensive collection of custom nodes for ComfyUI focused on advanced image processing, batch operations, prompt engineering, and workflow optimization. This node pack provides powerful tools for creative image manipulation, video processing, and efficient workflow management.

## 🌟 Key Features

- **Advanced Datamoshing Suite**: Multiple versions of datamoshing nodes (V1-V7) for creative image manipulation and glitch art effects
- **Batch Processing Tools**: Sophisticated batch operations including offset, range insertion, swapping, and frame management
- **Prompt Engineering**: Rich set of prompt manipulation tools including ZenkaiPrompt system, wildcards, and prompt cleaning
- **Image Processing**: Various image size adjusters, aspect ratio tools, VHS effects, anamorphic effects, and fractal generators
- **Video Processing**: Tools for video frame extraction, directory management, and special effects
- **3D Generation**: Parametric mesh generation for creating 3D objects (spheres, tori, Klein bottles)
- **Dataset Tools**: Wordcloud generation and caption processing capabilities

## 🚀 Quick Links
- [Video Tutorial](https://www.youtube.com/watch?v=MnZnP0Fav8E)
- [Articles & Guides](https://civitai.com/user/driftjohnson/articles)
- [Detailed Nodes Documentation](https://github.com/MushroomFleet/DJZ-Nodes/blob/main/DJZ-Nodes-Index.md)

## 📦 Installation

Clone this repository into your ComfyUI's custom_nodes directory:

```bash
cd custom_nodes
git clone https://github.com/MushroomFleet/DJZ-Nodes
```

## 🔧 Node Categories

### Image Processing & Effects
- AnamorphicEffect - Create cinematic anamorphic lens effects
- AspectSize (V1, V2) - Advanced aspect ratio management
- ImageSizeAdjuster (V1-V3) - Flexible image size manipulation
- FractalGenerator (V1-V3) - Create complex fractal patterns
- DjzDatamosh (V1-V7) - Advanced glitch art and datamoshing effects
- VHS_Effect (V1, V2) - Retro VHS-style effects
- DinskyPlus (V1, V2) - Enhanced image processing
- TrianglesPlus (V1, V2) - Geometric pattern generation

### Batch Operations
- BatchOffset - Offset batch processing operations
- BatchRangeInsert - Insert operations within batch ranges
- BatchRangeSwap - Swap elements within batch ranges
- BatchThief - Advanced batch manipulation
- LoadVideoBatchFrame - Load video frames for batch processing

### Prompt Engineering
- ZenkaiPrompt (V1, V2) - Advanced prompt enhancement system
- ZenkaiWildcard (V1, V2) - Dynamic wildcard management
- PromptCleaner - Clean and optimize prompts
- PromptInject - Inject modifiers into prompts
- PromptSwap - Swap prompt components
- StringWeights - Manage prompt emphasis weights
- StringPainter (V1, V2) - Visual prompt editing
- CaptionsToPromptList - Convert captions to prompt lists

### Video & Directory Tools
- LoadVideoDirectory - Batch video file loading
- LoadTextDirectory - Text file directory management
- ProjectFilePathNode - File path management
- FFXFADEORAMA - Video transition effects
- DJZLoadLatent (V1, V2) - Advanced latent loading

### 3D & Creative Tools
- ParametricMeshGen (V1, V2) - Create 3D meshes (spheres, tori, Klein bottles)
  - Example outputs in `/outputs` directory include sphere, torus, and Klein bottle models

### Data Processing
- DatasetWordcloud - Generate word clouds from datasets
- SaveText - Text data persistence
- SequentialNumberGenerator - Generate sequential numbers

## 📚 Resources & Examples

### Example Workflows
The `examples/` directory contains ready-to-use workflow examples:
- FFX-Fade-O-Rama.json - Demonstrates video transition effects
- Zenkai-System.json - Shows prompt engineering capabilities

### Prompt Templates
The `prompts/` directory includes a vast collection of prompt templates for various styles and use cases:
- Video generation prompts (CogVideo series)
- Character descriptions and styles
- Scene compositions (cyberpunk, fantasy, sci-fi)
- Special effects and artistic styles
- Automotive and action sequences
- Professional and workplace scenes
- Nature and landscape descriptions
- Emotional and dialogue-focused prompts

Find more example workflows and detailed usage instructions in the [DJZ-Nodes-Index.md](https://github.com/MushroomFleet/DJZ-Nodes/blob/main/DJZ-Nodes-Index.md) file.

# About the Creator

### Hi 👋, I'm Drift Johnson

### Data Scientist & Diffusion Designer from England

[![Twitter Follow](https://img.shields.io/twitter/follow/mushroomfleet?logo=twitter&style=for-the-badge)](https://twitter.com/mushroomfleet)

- 🔭 I'm currently working on **Zenkai XL Diffusion**
- 🌱 I'm currently learning **LLM's & Applied Diffusion**
- 👨‍💻 All of my projects are available at [https://civitai.com/user/driftjohnson/models](https://civitai.com/user/driftjohnson/models)
- 📝 I rarely write articles on [https://mushroomfleet.substack.com/](https://mushroomfleet.substack.com/)
- 💬 Ask me about **Diffusion Models**
- 📫 How to reach me **mushroomfleet@gmail.com**
- ⚡ Fun fact **When i'm not Drafting I'm Drifting.**

### Connect with me:

[![Twitter](https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/twitter.svg)](https://twitter.com/mushroomfleet)
[![LinkedIn](https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/linked-in-alt.svg)](https://linkedin.com/in/mushroomfleet)
[![Instagram](https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/instagram.svg)](https://instagram.com/mushroomfleet)
[![YouTube](https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/youtube.svg)](https://www.youtube.com/@FiveBelowFiveUK)
[![Discord](https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/discord.svg)](https://discord.gg/DtMXKqD5bT)

### Languages and Tools:

[![IFTTT](https://www.vectorlogo.zone/logos/ifttt/ifttt-ar21.svg)](https://ifttt.com/)
[![Linux](https://raw.githubusercontent.com/devicons/devicon/master/icons/linux/linux-original.svg)](https://www.linux.org/)
[![MySQL](https://raw.githubusercontent.com/devicons/devicon/master/icons/mysql/mysql-original-wordmark.svg)](https://www.mysql.com/)
[![Nginx](https://raw.githubusercontent.com/devicons/devicon/master/icons/nginx/nginx-original.svg)](https://www.nginx.com)
[![Photoshop](https://raw.githubusercontent.com/devicons/devicon/master/icons/photoshop/photoshop-line.svg)](https://www.photoshop.com/en)
[![PHP](https://raw.githubusercontent.com/devicons/devicon/master/icons/php/php-original.svg)](https://www.php.net)
[![Python](https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg)](https://www.python.org)
[![PyTorch](https://www.vectorlogo.zone/logos/pytorch/pytorch-icon.svg)](https://pytorch.org/)
[![Unreal Engine](https://raw.githubusercontent.com/kenangundogan/fontisto/036b7eca71aab1bef8e6a0518f7329f13ed62f6b/icons/svg/brand/unreal-engine.svg)](https://unrealengine.com/)

### Support:

[![Ko-Fi](https://cdn.ko-fi.com/cdn/kofi3.png?v=3)](https://ko-fi.com/driftjohnson)
