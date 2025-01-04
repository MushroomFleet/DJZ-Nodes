# DJZ-Nodes

Drift Johnsons Custom nodes for ComfyUI  
Video: https://www.youtube.com/watch?v=MnZnP0Fav8E  
Article: https://civitai.com/user/driftjohnson/articles

- [Detailed Nodes Index](https://github.com/MushroomFleet/DJZ-Nodes/blob/main/DJZ-Nodes-Index.md)

## Installation

Clone this repo into /custom_nodes/

```bash
cd custom_nodes
git clone https://github.com/MushroomFleet/DJZ-Nodes
```

AspectSize and ImageSizeAdjuster both address a simple problem, for best results images benefit from having dimensions divisible by 64  
AspectSize allows choice of base model and Aspect Ratio, it then calculates the best height and width which is closest to the targer and /64 on both sides  
ImageSizeAdjuster is the same idea but with an image input, doing the same calulation and outputting adjust dimensions for a resize node  
Zenkai-Prompt allows you to mix text files with random line chosen with seed  
Zenkai-wildcards parses a string for wildcards and swap out a single word in the same way  
recursive wildcard examples and 5000 prompts from my Zenkai system are included in the pack  
StringWeights simply wraps the generated strings with comfyui prompt weighting  

In all workflows the V2 offer advanced controls which might be useful over the base function

### AspectSize

default maximums:  
SD 512x512  
SDXL 1024x1024  
Cascade 2048x2048  
Downscale factor 16 was baked into this version  
simply choose your aspect ratio.

### AspectSizeV2

default maximums:  
SD 512x512  
SDXL 1024x1024  
Cascade 2048x2048  
allows customisation of the Downscale factor, 64 recommended  
simply choose your aspect ratio.

![AspectSizeV2](https://i.gyazo.com/b354edf9deee624fa27512da98601b36.png)

### ImageSizeAdjuster

default maximums:  
SD 512x512  
SDXL 1024x1024  
Cascade 2048x2048  
allows customisation of the Downscale factor, 64 recommended  
simply input your image, feed adjusted dimensions to a resize node.

![ImageSizeAdjuster](https://i.gyazo.com/d922a13e0ba47e83405db6c2657f7c6c.png)

### ImageSizeAdjusterV2

default maximums:  
SD 512x512  
SDXL 1024x1024  
Cascade 2048x2048  
allows customisation of the Downscale factor, 64 recommended  
simply input your image, feed adjusted dimensions to a resize node.

![ImageSizeAdjusterV2](https://i.gyazo.com/de2e50570fe2e7dd611feaffdebab929.png)

### ZenkaiPrompt

place .txt files inside: \prompts\  
choose the text file  
separate prompts with new lines in the .txt  
use seed control to control the random selection

![ZenkaiPrompt](https://i.gyazo.com/bbf9a12d4f0dd819aa17d5dcd9847ffa.png)

### ZenkaiPromptV2

place .txt files inside: \prompts\  
choose the text file  
separate prompts with new lines in the .txt  
supports multi-sampled prompt  
use seed control to control the random selection

![ZenkaiPromptV2](https://i.gyazo.com/2bd40c42de4a116bbf60e4a99c131b84.png)

### ZenkaiWildcard

place .txt files inside: \wildcards\  
one or two words per line, for each wildcard file  
custom symbol (default $$) used to invoke the text filename  
designed for text passthrough  
use seed control to control the random selection

![ZenkaiWildcard](https://i.gyazo.com/4d7831155d033618023c975f64c2c149.png)

### ZenkaiWildcardV2

place .txt files inside: \wildcards\  
one or two words per line, for each wildcard file  
custom symbol (default $$) used to invoke the text filename  
support recursive wilcards (wildcards inside wildcards)  
designed for text passthrough  
use seed control to control the random selection

![ZenkaiWildcardV2](https://i.gyazo.com/ac056f611f1087844b051a7f68a93f7f.png)

### StringWeights

random string weight control:  
text string passtrhough node  
wraps the string with the selected wieght  
string="Hello" result=(hello:0.9) with weight 0.9 selected  
made for convenience

![StringWeights](https://i.gyazo.com/ac056f611f1087844b051a7f68a93f7f.png)

### String Painter

String Painting Nodes:  
add the string to the end of a prompt, to see the effect  
generates the 16/32bit Hex from seed with options  
chaos inpaint/variation, colaboration with @StringPaintSunday from 2022  
V2 offers more controls and has a seed range limiter

![String Painter](https://i.gyazo.com/261e5a8b04212cd0711d0f12cfe97e70.png)

### FFX Fade-O-Rama

creates a sequence of images using two images  
comes with a bunch of stock transition effect

![FFX Fade-O-Rama](https://i.gyazo.com/9a2755de83e1825ae6cb23d0c16b433e.png)

Zenkai-Prompt and Zenkai-Wildcard, with StringWeights for control.  
examples folder, contains example workflows.

![Example Workflow](https://i.gyazo.com/e1431b0412590806f0fb388c337f59cf.png)

# Hi 👋, I'm Drift Johnson

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
