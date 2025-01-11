# DJZ-Nodes

A comprehensive collection of custom nodes for ComfyUI focused on advanced image/video processing, audio manipulation, batch operations, prompt engineering, and workflow optimization. This node pack provides powerful tools for creative media manipulation and efficient workflow management.

## 🌟 Key Features

- **Advanced Datamoshing Suite**: Seven generations of datamoshing nodes (V1-V7) for creative image manipulation and glitch art effects
- **Batch Processing Tools**: Sophisticated batch operations including offset, range insertion, swapping, and frame management
- **Prompt Engineering**: Rich set of prompt manipulation tools including ZenkaiPrompt system, wildcards, and prompt cleaning
- **Image Processing**: Various image size adjusters, aspect ratio tools, VHS effects, anamorphic effects, fractal generators, and Technicolor effects
- **Video Processing**: Tools for video frame extraction, directory management, and special effects
- **3D Generation**: Parametric mesh generation for creating 3D objects (spheres, tori, Klein bottles)
- **Dataset Tools**: Wordcloud generation and caption processing capabilities

## 🚀 Quick Links
- [Video Tutorial](https://www.youtube.com/watch?v=MnZnP0Fav8E)
- [Articles & Guides](https://civitai.com/user/driftjohnson/articles)
- [Example Workflows](https://github.com/MushroomFleet/DJZ-Workflows/tree/main/DJZ-Nodes-Examples)
- [Detailed Nodes Documentation](https://github.com/MushroomFleet/DJZ-Nodes/blob/main/DJZ-Nodes-Index.md)

## 📦 Installation

### Method 1: Git Clone (Recommended)
Clone this repository into your ComfyUI's custom_nodes directory:

```bash
cd custom_nodes
git clone https://github.com/MushroomFleet/DJZ-Nodes
cd DJZ-Nodes
pip install -r requirements.txt
```

### Method 2: Portable Installation (Windows)
For Windows users, use the provided installation batch files:
1. Download and extract the repository
2. Run `install-portable.bat` for basic installation
3. Run `pip-update-portable.bat` to update dependencies
4. Run `onnx-install-portable.bat` if you need ONNX support

## 🔧 Node Categories

### Audio Processing
- **CombineAudio** - Mix and merge audio files with customizable parameters

### Image Processing & Effects
- **Cinematic Effects**
  - AnamorphicEffect - Create cinematic anamorphic lens effects
  - PanavisionLens (V1, V2) - Simulate Panavision lens characteristics
  - Technicolor3Strip (V1, V2) - Classic Technicolor film emulation
  - KinescopeEffect - Vintage TV/film look simulation with customizable scan lines and distortion
  - VHS_Effect (V1, V2) - Retro VHS-style effects
  - VideoInterlaced - Create interlaced video effects
- **Creative Effects**
  - DjzDatamosh (V1-V7) - Advanced glitch art and datamoshing effects
  - FractalGenerator (V1-V3) - Create complex fractal patterns
  - DinskyPlus (V1, V2) - Enhanced image processing
  - TrianglesPlus (V1, V2) - Geometric pattern generation
- **Image Management**
  - AspectSize (V1, V2) - Advanced aspect ratio management
  - ImageSizeAdjuster (V1-V3) - Flexible image size manipulation

### Video & Animation Tools
- LoadVideoDirectory - Batch video file loading
- LoadVideoBatchFrame - Precise video frame extraction
- FFXFADEORAMA - Advanced video transition and fade effects
- DJZLoadLatent (V1, V2) - Advanced latent loading and manipulation

### Batch Operations
- BatchOffset - Offset batch processing operations
- BatchRangeInsert - Insert operations within batch ranges
- BatchRangeSwap - Swap elements within batch ranges
- BatchThief - Advanced batch manipulation

### Prompt Engineering & Text Tools
- **Zenkai System**
  - ZenkaiPrompt (V1, V2) - Advanced prompt enhancement system
  - ZenkaiWildcard (V1, V2) - Dynamic wildcard management
- **String Manipulation**
  - StringPainter (V1, V2) - Visual prompt editing
  - StringWeights - Manage prompt emphasis weights
  - StringChaos - Advanced string manipulation
- **Prompt Management**
  - PromptCleaner - Clean and optimize prompts
  - PromptInject - Inject modifiers into prompts
  - PromptSwap - Swap prompt components
  - CaptionsToPromptList - Convert captions to prompt lists

### File & Data Management
- LoadTextDirectory - Text file directory management
- ProjectFilePathNode - File path management
- SaveText - Text data persistence
- SequentialNumberGenerator - Generate sequential numbers
- DatasetWordcloud - Generate word clouds from datasets

### 3D Generation
- ParametricMeshGen (V1, V2) - Create 3D meshes
  - Supports: Spheres, Tori, Klein bottles, and custom parametric surfaces
  - Example outputs in `/outputs` directory

## 📚 Resources & Examples

### Example Workflows
The `examples/` directory contains ready-to-use workflow examples:
- FFX-Fade-O-Rama.json - Video transition effects
- Zenkai-System.json - Prompt engineering system showcase
- Combine-Audio-V1.json - Audio mixing and processing
- Parametric-Mesh-Gen-V2.json - Advanced 3D mesh generation

Each node has its own example workflow available in the [DJZ-Workflows repository](https://github.com/MushroomFleet/DJZ-Workflows/tree/main/DJZ-Nodes-Examples).

### Documentation
Every node includes detailed documentation in its corresponding .md file, covering:
- Input/Output specifications
- Usage instructions
- Example configurations
- Tips and best practices

Find the complete documentation index in [DJZ-Nodes-Index.md](https://github.com/MushroomFleet/DJZ-Nodes/blob/main/DJZ-Nodes-Index.md).

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
