# DJZ-Nodes

A comprehensive collection of custom nodes for ComfyUI that revolutionizes creative media workflows. This extensive node pack provides powerful tools for advanced image/video processing, audio manipulation, batch operations, prompt engineering, and workflow optimization. With over 50 specialized nodes, it offers one of the most complete custom node collections for ComfyUI, enabling everything from sophisticated video effects to advanced prompt engineering.

## 🌟 Key Features

- **Advanced Image Effects Suite**: Comprehensive collection of cinematic effects including Anamorphic, Panavision, Technicolor, Kinescope, and VHS simulations
- **Video Processing & Datamoshing**: Seven generations of datamoshing nodes (V1-V7) plus advanced video frame management and effects
- **Batch Processing Tools**: Sophisticated batch operations for efficient workflow management
- **Prompt Engineering**: Advanced prompt manipulation with the ZenkaiPrompt system, wildcards, and cleaning tools
- **3D Generation**: Parametric mesh generation for creating complex 3D objects
- **Dataset & File Management**: Comprehensive tools for handling datasets, files, and text processing

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
- **CombineAudio** - Professional audio mixing and merging with customizable parameters

### Image Processing & Effects
- **Cinematic Effects**
  - AnamorphicEffect - Professional cinematic lens distortion
  - PanavisionLens (V1, V2) - Authentic Panavision lens simulation
  - Technicolor3Strip (V1, V2) - Classic film color process emulation
  - KinescopeEffect - Vintage broadcast look with customizable parameters
  - VHS_Effect (V1, V2) - Authentic retro video artifacts
  - VideoInterlaced - Professional interlaced video simulation
- **Creative Effects**
  - DjzDatamosh (V1-V7) - Industry-leading glitch art suite
  - FractalGenerator (V1-V3) - High-performance fractal creation
  - DinskyPlus (V1, V2) - Advanced image processing suite
  - TrianglesPlus (V1, V2) - Geometric pattern generation
- **Image Management**
  - AspectSize (V1, V2) - Precise aspect ratio control
  - ImageSizeAdjuster (V1-V3) - Professional image scaling tools

### Video & Animation Tools
- LoadVideoDirectory - Efficient video batch processing
- LoadVideoBatchFrame - Frame-accurate video extraction
- FFXFADEORAMA - Professional transition effects
- DJZLoadLatent (V1, V2) - Advanced latent space manipulation

### Batch Operations
- BatchOffset - Precision batch timing control
- BatchRangeInsert - Smart batch content insertion
- BatchRangeSwap - Efficient batch content exchange
- BatchThief - Advanced batch data manipulation

### Prompt Engineering & Text Tools
- **Zenkai System**
  - ZenkaiPrompt (V1, V2) - Next-generation prompt enhancement
  - ZenkaiWildcard (V1, V2) - Dynamic prompt variation system
- **String Manipulation**
  - StringPainter (V1, V2) - Visual prompt composition
  - StringWeights - Precise prompt emphasis control
  - StringChaos - Creative text transformation
- **Prompt Management**
  - PromptCleaner - Intelligent prompt optimization
  - PromptInject - Dynamic prompt modification
  - PromptSwap - Smart prompt component exchange
  - CaptionsToPromptList - Efficient caption conversion

### File & Data Management
- LoadTextDirectory - Bulk text processing
- ProjectFilePathNode - Project organization
- SaveText - Data persistence
- SequentialNumberGenerator - Custom sequence generation
- DatasetWordcloud - Visual dataset analysis

### 3D Generation
- ParametricMeshGen (V1, V2) - Professional 3D mesh creation
  - Supports: Spheres, Tori, Klein bottles, and custom parametric surfaces
  - Example outputs in `/outputs` directory

## 📚 Resources & Examples

### Example Workflows
The `examples/` directory contains production-ready workflows:
- FFX-Fade-O-Rama.json - Professional video transitions
- Zenkai-System.json - Advanced prompt engineering
- Combine-Audio-V1.json - Professional audio processing
- Parametric-Mesh-Gen-V2.json - Complex 3D generation

Each node has its own example workflow available in the [DJZ-Workflows repository](https://github.com/MushroomFleet/DJZ-Workflows/tree/main/DJZ-Nodes-Examples).

### Documentation
Every node includes comprehensive documentation in its corresponding .md file, covering:
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
