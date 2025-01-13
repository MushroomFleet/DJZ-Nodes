# Film Grain Effect Node

A ComfyUI custom node that adds dynamic film grain effects to images or video frames. This node simulates various types of film grain patterns, from subtle analog-like noise to more complex temporal variations.

## Overview

The Film Grain Effect node applies procedural noise patterns to images while allowing for temporal variations, making it particularly suitable for video applications. It supports multiple presets and customizable parameters to achieve different grain styles and intensities.

## Parameters

### Required Inputs

- **images**: The input images to process (accepts batch input for video frames)
- **preset**: Choose from predefined grain patterns:
  - `subtle`: Minimal, consistent grain suitable for modern film looks
  - `vintage`: Classic film stock simulation with periodic variations
  - `unstable_signal`: Dynamic grain with signal-like fluctuations
  - `dip`: Creates periodic intensity dips in the grain pattern
  - `ebb`: Smooth, wave-like variations in grain intensity
  - `flow`: Fluid, continuous changes in grain pattern
- **base_intensity**: (0.0 - 1.0, default: 0.1)
  - Controls the overall strength of the grain effect
  - Lower values create more subtle grain
  - Higher values produce more pronounced grain
- **time_scale**: (0.1 - 10.0, default: 1.0)
  - Affects the speed of temporal variations in the grain pattern
  - Higher values create faster changes
  - Lower values result in slower, more gradual variations
- **noise_scale**: (0.0 - 1.0, default: 0.2)
  - Controls the scale/size of the grain particles
  - Lower values create finer grain
  - Higher values produce more coarse, visible grain
- **seed**: (Integer, default: 0)
  - Random seed for reproducible grain patterns
  - Same seed will generate identical grain patterns given the same parameters

## Preset Descriptions

1. **subtle**
   - Minimal grain effect with gentle temporal variations
   - Best for modern digital film simulation
   - Ideal for adding slight texture without being noticeable

2. **vintage**
   - Classic film stock simulation
   - Includes periodic intensity variations and temporal decay
   - Suitable for achieving retro or period-appropriate looks

3. **unstable_signal**
   - Dynamic, fluctuating grain pattern
   - Simulates analog video signal instability
   - Includes multiple layered temporal variations

4. **dip**
   - Creates periodic dips in grain intensity
   - Simulates film degradation or processing artifacts
   - Useful for creating rhythmic visual texture

5. **ebb**
   - Smooth, wave-like variations in grain intensity
   - Creates a natural, organic feel
   - Good for dreamlike or atmospheric effects

6. **flow**
   - Fluid, continuous changes in grain pattern
   - Multiple overlapping temporal variations
   - Suitable for creating dynamic, living textures

## Technical Details

- The node processes images in the range 0-1 (float32)
- Grain patterns are generated using Gaussian noise
- Temporal variations are achieved through sinusoidal functions
- All grain patterns are clipped to maintain valid pixel values
- Supports batch processing for video frames
- GPU-compatible through PyTorch tensor operations

## Usage Tips

1. For subtle film simulation:
   - Use the "subtle" preset
   - Keep base_intensity around 0.1
   - Set noise_scale to 0.15-0.2

2. For vintage film looks:
   - Use the "vintage" preset
   - Increase base_intensity to 0.2-0.3
   - Adjust time_scale to 0.5-2.0 depending on desired variation speed

3. For experimental effects:
   - Try "unstable_signal" or "flow" presets
   - Increase time_scale for more rapid variations
   - Experiment with higher base_intensity values

4. For consistent grain across frames:
   - Use the same seed value
   - Keep time_scale low
   - Use "subtle" or "vintage" presets
