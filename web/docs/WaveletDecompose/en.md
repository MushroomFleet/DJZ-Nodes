# Wavelet Decomposition (Photoshop Style)

A ComfyUI custom node that performs Photoshop-style wavelet decomposition on images, breaking them down into multiple detail scales and a residual layer. This decomposition is similar to Photoshop's "Decompose" filter, which is useful for advanced image manipulation and analysis.

## Description

The WaveletDecompose node breaks down an image into different frequency bands (scales) using Gaussian blur operations. This decomposition allows you to separate an image into:
- A residual layer (containing the base image structure)
- Multiple detail scales (containing progressively finer details)
- The original image

Each scale represents different levels of detail in the image, similar to frequency bands, making it useful for:
- Texture analysis
- Detail enhancement
- Image processing
- Style transfer applications

## Parameters

### Required Inputs

1. **image** (IMAGE)
   - The input image to decompose
   - Accepts any standard image tensor in ComfyUI format

2. **scales** (INT)
   - Number of detail scales to extract
   - Default: 5
   - Range: 1-10
   - Step: 1
   - Controls how many levels of detail are extracted from the image

## Outputs

The node provides 7 output connections (from coarse to fine details):

1. **residual**
   - The base structure of the image
   - Contains the lowest frequency components

2. **scale_1**
   - First level of detail
   - Contains very coarse details

3. **scale_2**
   - Second level of detail
   - Contains medium-coarse details

4. **scale_3**
   - Third level of detail
   - Contains medium details

5. **scale_4**
   - Fourth level of detail
   - Contains medium-fine details

6. **scale_5**
   - Fifth level of detail
   - Contains the finest details

7. **original**
   - The unmodified input image
   - Useful for reference or further processing

Note: If fewer scales than outputs are requested, the remaining scale outputs will be filled with zero tensors.

## Technical Implementation

The decomposition process uses several sophisticated techniques:

1. **Gaussian Blur**
   - Implements a 2D Gaussian kernel for blurring
   - Kernel size and sigma are automatically calculated based on scale
   - Uses reflection padding to prevent edge artifacts

2. **Scale Separation**
   - Each detail scale is extracted by subtracting consecutive Gaussian blurs
   - Uses linear light blending mode for detail extraction
   - Preserves image information across scales

3. **Device Handling**
   - Automatically uses CUDA if available
   - Falls back to CPU if necessary
   - Ensures consistent tensor device placement

## Use Cases

1. **Detail Enhancement**
   - Selectively enhance specific detail scales
   - Useful for sharpening or softening specific features

2. **Style Transfer**
   - Manipulate different detail scales independently
   - Combine scales from different images

3. **Image Analysis**
   - Analyze image structure at different scales
   - Useful for understanding image composition

4. **Texture Manipulation**
   - Modify texture characteristics at specific scales
   - Create unique visual effects

## Integration

The node integrates seamlessly with ComfyUI's workflow system and can be combined with other nodes for complex image processing operations. Each output can be connected to different processing nodes for scale-specific manipulations.
