# DJZ-Nodes
Drift Johnsons Custom nodes for ComfyUI


# AspectSize
default maximum is 2048x2048, choose your aspect ratio.
Often there is a problem with Cascade Stage A, with pixel_unshuffle where the image dimensions no longer divide by 2.
example is shown here https://github.com/MushroomFleet/DJZ-Nodes/blob/main/pixel_unshuffle_Cascade_error.jpg

This node fixes that problem by finding the safest values for cascade.
This is my first public node, it also supports 1.5 and SDXL.

Currently this is not a full fledged custom node pack, cloning will not work yet ;)
just put the .py files in the main comfyui customnodes folder, then restart to use them.
