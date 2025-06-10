# WaveletCompose Node

## Overview
The WaveletCompose node is a specialized image processing node for ComfyUI that reconstructs an image from its wavelet decomposition scales. It works in conjunction with the WaveletDecompose node, taking the decomposed frequency bands and combining them back into the original image.

## How It Works
The node performs wavelet composition by:
1. Taking a residual (base) image and multiple detail scales as input
2. Converting normalized detail coefficients back to their original difference space
3. Progressively adding each detail scale to the residual image
4. Ensuring the final output stays within valid image range (0 to 1)

## Input Parameters

### Required Inputs
- **residual**: (IMAGE) The base residual layer containing the most blurred version of the image
- **scale_1**: (IMAGE) First detail scale containing fine details
- **scale_2**: (IMAGE) Second detail scale containing medium-fine details
- **scale_3**: (IMAGE) Third detail scale containing medium details
- **scale_4**: (IMAGE) Fourth detail scale containing medium-coarse details
- **scale_5**: (IMAGE) Fifth detail scale containing coarse details

## Outputs
- **composed_image**: (IMAGE) The final reconstructed image combining all scales

## Usage
1. First use the WaveletDecompose node to break an image into its frequency components
2. Connect the corresponding outputs from WaveletDecompose to the inputs of WaveletCompose
3. The node will automatically reconstruct the original image from these components

## Technical Details
- The node automatically handles denormalization of detail coefficients
- Detail scales are converted from display space [0, 1] back to difference space [-max(abs), +max(abs)]
- Input tensors are automatically normalized if they exceed the 0-1 range
- The final output is clamped to ensure valid pixel values

## Use Cases
- Image reconstruction after frequency-based editing
- Analyzing and manipulating image frequencies
- Creating custom image processing effects by modifying specific frequency bands
- Educational purposes to understand wavelet decomposition and composition

## Example Workflow
```
[Image] → [WaveletDecompose] → [Your Processing] → [WaveletCompose] → [Final Image]
```

This node is particularly useful when you want to:
- Modify specific frequency bands of an image
- Apply effects to certain scales of detail
- Reconstruct images after frequency-based manipulations
