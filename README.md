# DJZ-Nodes
<p align="left"> Drift Johnsons Custom nodes for ComfyUI <br />
Video: https://www.youtube.com/watch?v=MnZnP0Fav8E <br />
Article: https://civitai.com/user/driftjohnson/articles</p> <br />
<br /><br />
<p>AspectSize and ImageSizeAdjuster both address a simple problem, for best results images benefit from having dimensions divisible by 64<br />
AspectSize allows choice of base model and Aspect Ratio, it then calculates the best height and width which is closest to the targer and /64 on both sides<br />
ImageSizeAdjuster is the same idea but with an image input, doing the same calulation and outputting adjust dimensions for a resize node <br />
Zenkai-Prompt allows you to mix text files with random line chosen with seed <br />
Zenkai-wildcards parses a string for wildcards and swap out a single word in the same way <br />
recursive wildcard examples and 5000 prompts from my Zenkai system are included in the pack <br />
StringWeights simply wraps the generated strings with comfyui prompt weighting <br /> <br />
In all workflows the V2 offer advanced controls which might be useful over the base function</p> <br />
  <br /><br />
<h3>AspectSize</h3> <br />
<p align="left"> default maximums: <br />
SD 512x512 <br />
SDXL 1024x1024 <br />
Cascade 2048x2048  <br />
Downscale factor 16 was baked into this version <br />
simply choose your aspect ratio.</p> <br />
<br /><br />
<h3>AspectSizeV2</h3> <br />
<p align="left"> default maximums: <br />
SD 512x512 <br />
SDXL 1024x1024 <br />
Cascade 2048x2048  <br />
allows customisation of the Downscale factor, 64 recommended<br />
simply choose your aspect ratio.</p> <br />
<img src="https://i.gyazo.com/b354edf9deee624fa27512da98601b36.png" />
<br /><br />
<h3>ImageSizeAdjuster</h3> <br />
<p align="left"> default maximums: <br />
SD 512x512 <br />
SDXL 1024x1024 <br />
Cascade 2048x2048  <br />
allows customisation of the Downscale factor, 64 recommended<br />
simply input your image, feed adjusted dimensions to a resize node.</p> <br />
<img src="https://i.gyazo.com/d922a13e0ba47e83405db6c2657f7c6c.png" />
<br /><br />
<h3>ImageSizeAdjusterV2</h3> <br />
<p align="left"> default maximums: <br />
SD 512x512 <br />
SDXL 1024x1024 <br />
Cascade 2048x2048  <br />
allows customisation of the Downscale factor, 64 recommended<br />
simply input your image, feed adjusted dimensions to a resize node.</p> <br />
<img src="https://i.gyazo.com/de2e50570fe2e7dd611feaffdebab929.png" />
<br /><br />
<h3>ZenkaiPrompt</h3> <br />
<p align="left"> place .txt files inside: \prompts\ <br />
choose the text file <br />
separate prompts with new lines in the .txt <br />
use seed control to control the random selection</p>  <br />
<img src="https://i.gyazo.com/bbf9a12d4f0dd819aa17d5dcd9847ffa.png" />
<br /><br />
<h3>ZenkaiPromptV2</h3> <br />
<p align="left"> place .txt files inside: \prompts\ <br />
choose the text file <br />
separate prompts with new lines in the .txt <br />
supports multi-sampled prompt <br />
use seed control to control the random selection</p>  <br />
<img src="https://i.gyazo.com/2bd40c42de4a116bbf60e4a99c131b84.png" />
<br /><br />
<h3>ZenkaiWildcard</h3> <br />
<p align="left"> place .txt files inside: \wildcards\ <br />
one or two words per line, for each wildcard file <br />
custom symbol (default $$) used to invoke the text filename <br /> 
designed for text passthrough <br /> 
use seed control to control the random selection</p>  <br />
<img src="https://i.gyazo.com/4d7831155d033618023c975f64c2c149.png" />
<br /><br />
<h3>ZenkaiWildcardV2</h3> <br />
<p align="left"> place .txt files inside: \wildcards\ <br />
one or two words per line, for each wildcard file <br />
custom symbol (default $$) used to invoke the text filename <br /> 
support recursive wilcards (wildcards inside wildcards) <br />
designed for text passthrough <br /> 
use seed control to control the random selection</p>  <br />
<img src="https://i.gyazo.com/ac056f611f1087844b051a7f68a93f7f.png" />
<br /><br />
<h3>StringWeights</h3> <br />
<p align="left"> random string weight control: <br />
text string passtrhough node<br />
wraps the string with the selected wieght <br />
string="Hello" result=(hello:0.9) with weight 0.9 selected  <br />
made for convenience <br /> </p> <br />
<img src="https://i.gyazo.com/ac056f611f1087844b051a7f68a93f7f.png" />
<br /><br />
<h3>String Painter</h3> <br />
<p align="left"> String Painting Nodes: <br />
add the string to the end of a prompt, to see the effect<br />
generates the 16/32bit Hex from seed with options <br />
chaos inpaint/variation, colaboration with @StringPaintSunday from 2022<br />
V2 offers more controls and has a seed range limiter <br /> </p> <br />
<img src="https://i.gyazo.com/261e5a8b04212cd0711d0f12cfe97e70.png" />
<br /><br />
<h3>String Painter</h3> <br />
<p align="left"> FFX Fade-O-Rama: <br />
creates a sequence of images using two images<br />
comes with a bunch of stock transition effect <br />
<img src="https://cdn.discordapp.com/attachments/1210800590955880448/1278401352975913061/9a2755de83e1825ae6cb23d0c16b433e.png" />

<br /><br />
<p align="left"> Zenkai-Prompt and Zenkai-Wildcard, with StringWeights for control.
examples folder, contains example workflows. </p><br />
<img src="https://i.gyazo.com/e1431b0412590806f0fb388c337f59cf.png" />
<br />


<br /><br />
<h2>Installation</h2>

-- Clone this repo into /custom_nodes/ <br />

> cd custom_nodes <br />
> git clone https://github.com/MushroomFleet/DJZ-Nodes <br />

<br /><br />
<h1 align="center">Hi 👋, I'm Drift Johnson</h1>
<h3 align="center">Data Scientist & Diffusion Designer from England</h3>

<p align="left"> <a href="https://twitter.com/mushroomfleet" target="blank"><img src="https://img.shields.io/twitter/follow/mushroomfleet?logo=twitter&style=for-the-badge" alt="mushroomfleet" /></a> </p>

- 🔭 I’m currently working on **Zenkai XL Diffusion**

- 🌱 I’m currently learning **LLM's & Applied Diffusion**

- 👨‍💻 All of my projects are available at [https://civitai.com/user/driftjohnson/models](https://civitai.com/user/driftjohnson/models)

- 📝 I rarely write articles on [https://mushroomfleet.substack.com/](https://mushroomfleet.substack.com/)

- 💬 Ask me about **Diffusion Models**

- 📫 How to reach me **mushroomfleet@gmail.com**

- ⚡ Fun fact **When i'm not Drafting I'm Drifting.**

<h3 align="left">Connect with me:</h3>
<p align="left">
<a href="https://twitter.com/mushroomfleet" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/twitter.svg" alt="mushroomfleet" height="30" width="40" /></a>
<a href="https://linkedin.com/in/mushroomfleet" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/linked-in-alt.svg" alt="mushroomfleet" height="30" width="40" /></a>
<a href="https://instagram.com/mushroomfleet" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/instagram.svg" alt="mushroomfleet" height="30" width="40" /></a>
<a href="https://www.youtube.com/@FiveBelowFiveUK" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/youtube.svg" alt="mushroomfleet" height="30" width="40" /></a>
<a href="https://discord.gg/https://discord.gg/DtMXKqD5bT" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/discord.svg" alt="https://discord.gg/DtMXKqD5bT" height="30" width="40" /></a>
</p>

<h3 align="left">Languages and Tools:</h3>
<p align="left"> <a href="https://ifttt.com/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/ifttt/ifttt-ar21.svg" alt="ifttt" width="40" height="40"/> </a> <a href="https://www.linux.org/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/linux/linux-original.svg" alt="linux" width="40" height="40"/> </a> <a href="https://www.mysql.com/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/mysql/mysql-original-wordmark.svg" alt="mysql" width="40" height="40"/> </a> <a href="https://www.nginx.com" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/nginx/nginx-original.svg" alt="nginx" width="40" height="40"/> </a> <a href="https://www.photoshop.com/en" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/photoshop/photoshop-line.svg" alt="photoshop" width="40" height="40"/> </a> <a href="https://www.php.net" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/php/php-original.svg" alt="php" width="40" height="40"/> </a> <a href="https://www.python.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a> <a href="https://pytorch.org/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/pytorch/pytorch-icon.svg" alt="pytorch" width="40" height="40"/> </a> <a href="https://unrealengine.com/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/kenangundogan/fontisto/036b7eca71aab1bef8e6a0518f7329f13ed62f6b/icons/svg/brand/unreal-engine.svg" alt="unreal" width="40" height="40"/> </a> </p>

<h3 align="left">Support:</h3>
<p><a href="https://ko-fi.com/driftjohnson"> <img align="left" src="https://cdn.ko-fi.com/cdn/kofi3.png?v=3" height="50" width="210" alt="driftjohnson" /></a></p><br><br>
