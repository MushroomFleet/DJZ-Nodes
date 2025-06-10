# Depth-Based Pixelization Node

This ComfyUI custom node applies a dynamic pixelization effect to images based on their corresponding depth maps. The pixelization block size varies according to the depth values, creating an interesting visual effect where different parts of the image are pixelated at different resolutions.

## Parameters

### Required Inputs

1. **images** (IMAGE)
   - A batch of input images to be processed
   - These are the images that will receive the pixelization effect

2. **depth_maps** (IMAGE)
   - Corresponding depth maps for the input images
   - These grayscale images determine how the pixelization effect is applied
   - Can be any depth map compatible with the input image dimensions

3. **min_block_size** (INT)
   - Minimum size of pixelization blocks
   - Range: 1 to 32
   - Default: 4
   - Controls the smallest possible pixel block size

4. **max_block_size** (INT)
   - Maximum size of pixelization blocks
   - Range: 1 to 64
   - Default: 32
   - Controls the largest possible pixel block size

5. **depth_influence** (FLOAT)
   - Controls how strongly the depth map affects the pixelization
   - Range: 0.1 to 2.0
   - Default: 1.0
   - Higher values create more dramatic differences between depth levels

6. **invert_depth** (BOOLEAN)
   - Determines whether to invert the depth map interpretation
   - Default: True
   - When True, closer objects (brighter in depth map) get smaller pixels
   - When False, closer objects get larger pixels

## Output

- Returns a processed IMAGE with the depth-based pixelization effect applied
- The output maintains the same dimensions as the input image

## How It Works

1. The node takes an input image and its corresponding depth map
2. The depth map is normalized to values between 0 and 1
3. For each position in the image, the depth value determines the size of the pixelization block
4. Blocks are created by averaging the colors within each block area
5. The process is applied across the entire image, creating a dynamic pixelization effect

## Usage Tips

1. For best results, ensure your depth map accurately represents the scene's depth information
2. Adjust min_block_size and max_block_size to control the range of pixelization effects
3. Use depth_influence to fine-tune how dramatically the depth affects the pixelization
4. Experiment with invert_depth to change whether near or far objects receive more pixelization
5. The node automatically handles batch processing for multiple images

## Technical Details

- The node automatically resizes depth maps to match input image dimensions
- Processes images in batches for efficient operation
- Handles edge cases and boundary conditions automatically
- Uses torch and OpenCV for efficient image processing
