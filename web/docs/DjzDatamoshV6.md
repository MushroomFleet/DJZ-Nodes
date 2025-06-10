# DjzDatamoshV6 Node

## Description
The DjzDatamoshV6 node is an advanced image effects node that performs pixel sorting based on edge detection. It uses the Sobel operator to identify edges in the image and sorts pixels within segments defined by these edges. This creates a unique glitch aesthetic that preserves the image's major structural elements while creating flowing, sorted patterns in less detailed areas.

## Parameters

### Required Inputs

1. **images** (IMAGE)
   - The batch of images to process
   - Input must be in BHWC format (Batch, Height, Width, Channels)
   - Each image should be RGB format

2. **threshold** (FLOAT)
   - Default: 128.0
   - Range: 0.0 to 255.0
   - Step: 1.0
   - Controls the sensitivity of edge detection
   - Lower values create more edge segments (more preserved detail)
   - Higher values create fewer edge segments (more sorting areas)

## Output
- Returns a modified IMAGE sequence with pixel-sorted effects applied
- Maintains the same dimensions and format as the input

## Technical Process

### 1. Edge Detection
- Converts RGB images to luma (brightness) values using standard coefficients:
  - Red: 0.2126
  - Green: 0.7152
  - Blue: 0.0722
- Applies Sobel operator for edge detection in both horizontal and vertical directions
- Creates an edge mask based on the threshold value

### 2. Segmentation
- Divides the image into segments based on detected edges
- Each segment represents a continuous region without strong edges
- Segments are processed row by row for consistent sorting direction

### 3. Pixel Sorting
- Within each segment:
  - Calculates luma values for all pixels
  - Sorts pixels based on their luma values
  - Applies the sorting to all color channels while maintaining color relationships

## Usage Tips

### Edge Detection Threshold
- **Low threshold** (0-50):
  - More sensitive edge detection
  - Smaller sorting segments
  - More preserved detail
  - Subtle sorting effect

- **Medium threshold** (50-150):
  - Balanced edge detection
  - Medium-sized sorting segments
  - Good mix of detail and effect

- **High threshold** (150-255):
  - Less sensitive edge detection
  - Larger sorting segments
  - More dramatic sorting effect
  - May lose some image detail

### Best Practices
1. Start with the default threshold (128.0) and adjust based on your image:
   - Increase for more dramatic sorting effects
   - Decrease for more subtle effects and detail preservation

2. Consider image content:
   - High contrast images work well with higher thresholds
   - Detailed images may benefit from lower thresholds
   - Experiment with different values for different visual styles

3. Batch Processing:
   - Can process multiple images at once
   - Consistent effects across all images in the batch
   - Same threshold applies to all images

## Notes
- Processing time depends on image size and complexity
- Edge detection preserves major image features while allowing sorting in smoother areas
- Returns unmodified input if any processing step fails
- Effect is deterministic - same input and threshold will produce the same result
