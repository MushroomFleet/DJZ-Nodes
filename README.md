# DJZ-Nodes
Drift Johnsons Custom nodes for ComfyUI
Video: https://www.youtube.com/watch?v=MnZnP0Fav8E
Article: https://civitai.com/user/driftjohnson/articles

# AspectSize
default maximums:
SD 512x512
SDXL 1024x1024
Cascade 2048x2048 
simply choose your aspect ratio.


Often there is a problem with Cascade Stage A, with pixel_unshuffle where the image dimensions no longer divide by 2.
example is shown here:
<img>https://github.com/MushroomFleet/DJZ-Nodes/blob/main/pixel_unshuffle_Cascade_error.jpg</img>

This node fixes that problem by finding the safest values for cascade.
This is my first public node, it also supports 1.5 and SDXL.

# Installation

-- Clone this repo into /custom_nodes/

> cd custom_nodes
> git clone https://github.com/MushroomFleet/DJZ-Nodes
