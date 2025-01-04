# DJZ Datamosh Node

The DJZ Datamosh node creates a datamoshing effect by analyzing motion between frames and applying block-based displacement. This creates a distinctive glitch-art effect commonly seen in datamoshed videos, where motion appears to smear and blend between frames.

## Parameters

### Required Inputs

1. **images** (IMAGE)
   - Input batch of images to process
   - Requires at least 2 frames to create the datamosh effect
   - Images should be in tensor format (BCHW)

2. **block_size** (INT)
   - Size of blocks used for motion analysis
   - Default: 16
   - Range: 4 to 64 pixels
   - Step: 4 pixels
   - Larger blocks = faster processing but chunkier effects
   - Smaller blocks = slower processing but smoother effects

3. **max_shift** (INT)
   - Maximum pixel distance blocks can move
   - Default: 8
   - Range: 1 to 32 pixels
   - Step: 1 pixel
   - Controls how far the glitch effect can "stretch"
   - Higher values allow for more dramatic distortions

4. **shift_range** (INT)
   - Step size for motion search
   - Default: 2
   - Range: 1 to 4
   - Step: 1
   - Higher values = faster but less accurate motion detection
   - Lower values = slower but more precise motion detection

## How It Works

The datamoshing process involves several steps:

1. **Block Division**
   - Each frame is divided into blocks of size `block_size × block_size`
   - These blocks are the basic units for motion analysis

2. **Motion Estimation**
   - For each block in the current frame:
     - Searches for the best matching block in the previous frame
     - Search area is limited by `max_shift` parameter
     - Search precision is controlled by `shift_range`
     - Matches are found by comparing pixel differences

3. **Motion Application**
   - Detected motion vectors are used to displace blocks
   - Creates the characteristic "smearing" effect
   - Blocks wrap around frame edges for seamless transitions

## Technical Details

### Motion Search Algorithm
- Uses a fast block-matching algorithm
- Compares blocks using sum of absolute differences (SAD)
- Implements efficient search patterns with configurable step sizes
- Handles edge cases and frame boundaries with wrapping

### Processing Pipeline
1. First frame is preserved as-is
2. Each subsequent frame:
   - Analyzes motion relative to previous processed frame
   - Applies detected motion to create distortion
   - Uses result as reference for next frame

## Important Notes

1. Performance Considerations:
   - Processing time increases with:
     - Smaller block sizes
     - Larger max shift values
     - Smaller shift range values
     - Higher resolution images
     - More input frames

2. Memory Usage:
   - Processes frames sequentially to manage memory
   - Maintains only necessary frames in memory
   - Outputs full batch after processing

3. Requirements:
   - Minimum of 2 input frames required
   - Input must be a batch of images (4D tensor)
   - All frames must have the same dimensions

4. The node is categorized under "image/effects" in the ComfyUI interface

## Tips for Best Results

1. Block Size Selection:
   - Use larger blocks (32-64) for more obvious, chunky glitch effects
   - Use smaller blocks (8-16) for smoother, more subtle distortions
   - Consider image resolution when selecting block size

2. Motion Parameters:
   - Increase max_shift for more dramatic stretching effects
   - Use smaller shift_range for more accurate motion tracking
   - Balance between effect quality and processing speed

3. Input Considerations:
   - Works best with footage containing clear motion
   - High contrast areas show the effect more clearly
   - Consider frame-to-frame differences when selecting parameters
