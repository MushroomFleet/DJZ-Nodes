# DJZ-Nodes
<p align="left"> Drift Johnsons Custom nodes for ComfyUI <br />
Video: https://www.youtube.com/watch?v=MnZnP0Fav8E <br />
Article: https://civitai.com/user/driftjohnson/articles</p> <br />
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
allows customisation of the Downscale factor<br />
simply choose your aspect ratio.</p> <br />

<br /><br />
<p align="left"> Often there is a problem with Cascade Stage A, with pixel_unshuffle where the image dimensions no longer divide by 2.
example is shown here: <br />
<img src="https://github.com/MushroomFleet/DJZ-Nodes/blob/main/pixel_unshuffle_Cascade_error.jpg" />
<br />
This node fixes that problem by finding the safest values for cascade.
This is my first public node, it also supports 1.5 and SDXL.</p>
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
