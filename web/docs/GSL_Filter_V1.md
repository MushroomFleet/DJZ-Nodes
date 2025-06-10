# GSL Filter v1 Node

A GPU-accelerated image processing node that applies various shader-based effects to images. This node utilizes OpenGL (via ModernGL) to perform high-performance image filtering and effects processing using GPU shaders.

## Input Parameters

### Required Inputs

1. **images** (IMAGE)
   - The input batch of images to process

2. **effect_preset** (COMBO)
   Options:
   - custom: No effect (bypass)
   - grayscale: Converts image to grayscale
   - edge_detection: Highlights edges in the image
   - gaussian_blur: Applies Gaussian blur effect
   - pixelate: Creates a pixelated effect
   - wave_distortion: Applies wave-based distortion
   - chromatic_aberration: Simulates lens color separation

3. **intensity** (FLOAT)
   - Default: 1.0
   - Range: 0.0 to 5.0
   - Step: 0.1
   - Controls the overall strength of the effect

4. **blur_radius** (FLOAT)
   - Default: 2.0
   - Range: 0.1 to 10.0
   - Step: 0.1
   - Controls the radius of the Gaussian blur effect

5. **edge_threshold** (FLOAT)
   - Default: 0.1
   - Range: 0.0 to 1.0
   - Step: 0.01
   - Threshold for edge detection sensitivity

6. **pixelate_factor** (INT)
   - Default: 4
   - Range: 1 to 64
   - Step: 1
   - Size of pixelation blocks (higher = more pixelated)

7. **wave_amplitude** (FLOAT)
   - Default: 0.1
   - Range: 0.0 to 1.0
   - Step: 0.01
   - Controls the strength of wave distortion

8. **wave_frequency** (FLOAT)
   - Default: 5.0
   - Range: 0.1 to 50.0
   - Step: 0.1
   - Controls the frequency of wave distortion

9. **chromatic_shift** (FLOAT)
   - Default: 0.01
   - Range: 0.0 to 0.1
   - Step: 0.001
   - Amount of RGB channel separation

## Effect Descriptions

### Grayscale
- Converts the image to grayscale using standard luminance weights
- Intensity controls the blend between original and grayscale
- Uses weights: R(0.299), G(0.587), B(0.114)

### Edge Detection
- Implements a simple edge detection filter
- Edge_threshold controls which edges are visible
- Higher threshold values show only strong edges
- Lower threshold values show more subtle details

### Gaussian Blur
- Applies a 2D Gaussian blur
- Blur_radius controls the spread of the blur
- Implemented as a separable convolution for better performance
- Quality scales with blur_radius parameter

### Pixelate
- Creates a blocky, pixelated effect
- Pixelate_factor determines block size
- Larger values create larger blocks
- Useful for retro-style effects

### Wave Distortion
- Applies sinusoidal distortion to the image
- Wave_amplitude controls distortion strength
- Wave_frequency controls number of waves
- Creates liquid-like or wavy effects

### Chromatic Aberration
- Simulates lens color fringing
- Shifts RGB channels separately
- Chromatic_shift controls separation amount
- Creates a "prismatic" effect

## Technical Implementation

- Uses ModernGL for GPU-accelerated processing
- Implements GLSL shaders for real-time effects
- Processes images in RGBA format
- Automatically handles color space conversion
- Supports batch processing of multiple images

## Performance Considerations

- GPU-accelerated processing for high performance
- Efficient shader-based implementations
- Automatic resource management
- Batch processing capability
- Memory-efficient texture handling

## Use Cases

- Photo and video post-processing
- Creative visual effects
- Real-time image filtering
- Artistic style transfer
- Visual glitch effects
- Retro/vintage style effects

## Tips

- For subtle effects, use lower intensity values
- Combine multiple passes for complex effects
- Adjust parameters gradually for precise control
- Monitor GPU memory usage with large batches
- Consider image resolution impact on performance

## Requirements

- Requires OpenGL-capable GPU
- ModernGL Python package
- Numpy for array operations
- OpenCV for color space conversion
