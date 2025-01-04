# FFX FADE-O-RAMA Node

The FFX FADE-O-RAMA node is a powerful animation tool that creates transition sequences between two images. It offers a variety of transition effects, from simple fades to complex glitch-style transitions and directional wipes.

## Parameters

### Required Parameters

- **image1**: The first input image that the transition will start from.
- **image2**: The second input image that the transition will end with.
- **num_frames**: The number of frames to generate for the transition sequence.
  - Default: 30
  - Minimum: 2
  - Maximum: 120
  - Step: 1

- **transition_type**: The type of transition effect to apply. Available options:
  - `fade`: Standard cross-fade between images
  - `glitchA`: Horizontal glitch effect from left to right
  - `glitchB`: Horizontal glitch effect from right to left
  - `wipeR`: Vertical wipe from top to bottom
  - `wipeL`: Vertical wipe from bottom to top
  - `smoothright`: Smooth transition moving right with cosine interpolation
  - `smoothleft`: Smooth transition moving left with cosine interpolation
  - `openglitchdoors`: Center-out glitch effect
  - `closeglitchdoors`: Outside-in circular transition
  - `openchanneldoors`: Center-out circular transition
  - `rgbbandright`: Diagonal RGB band transition moving right
  - `rgbdoubleright`: Double diagonal RGB transition moving right
  - `rgbdoubleleft`: Double diagonal RGB transition moving left
  - `rgbdoubleleft2`: Alternative double diagonal RGB transition moving left
  - `fadeblack`: Fade through black transition
  - `fadewhite`: Fade through white transition

- **filename_prefix**: The prefix to use for the output files.
  - Default: "FFXFADE"

## Outputs

1. **IMAGE**: Returns the complete sequence of transition frames as a tensor.
2. **UI Images**: Saves each frame as a separate PNG file in the output directory.

## Functionality

The node performs the following operations:

1. Validates that both input images have the same dimensions
2. Generates a sequence of transition frames based on the selected transition type
3. Saves each frame as a PNG file with sequential numbering
4. Returns the complete sequence for further processing

## Transition Types Explained

### Basic Transitions
- **fade**: Simple cross-fade between the two images
- **fadeblack**: Fades out to black, then fades in to the second image
- **fadewhite**: Fades out to white, then fades in to the second image

### Directional Wipes
- **wipeR**: Clean vertical wipe from top to bottom
- **wipeL**: Clean vertical wipe from bottom to top
- **smoothright**: Smooth transition with cosine interpolation moving right
- **smoothleft**: Smooth transition with cosine interpolation moving left

### Glitch Effects
- **glitchA**: Creates a horizontal glitch effect moving left to right
- **glitchB**: Creates a horizontal glitch effect moving right to left
- **openglitchdoors**: Glitch effect that spreads from the center outward
- **closeglitchdoors**: Circular transition that closes from the edges inward

### RGB Effects
- **rgbbandright**: Diagonal RGB band transition moving right
- **rgbdoubleright**: Double diagonal RGB transition moving right
- **rgbdoubleleft**: Double diagonal RGB transition moving left
- **rgbdoubleleft2**: Alternative double diagonal RGB transition moving left

## Use Cases

- Creating smooth transitions between generated images
- Building animation sequences with various effects
- Producing glitch art animations
- Creating professional-looking video transitions
- Experimenting with different transition styles for creative effects
