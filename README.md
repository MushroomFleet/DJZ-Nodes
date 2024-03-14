# DJZ-Nodes
Drift Johnsons Custom nodes for ComfyUI


# cascade_resizer
default maximum is 2048x2048, choose your aspect ratio.
Often there is a problem with Cascade Stage A, with pixel_unshuffle where the image dimensions no longer divide by 2.
This node fixes that problem by finding the safest values for cascade.

This is my first public node, it also supports 1.5 and SDXL.
