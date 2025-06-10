# Batch Offset Node

The Batch Offset node is designed to reorder images within a batch by shifting their positions by a specified offset. This is particularly useful for creating animation sequences or adjusting the order of batch-processed images.

## Parameters

### Required Inputs

- **images** (IMAGE)
  - A batch of input images
  - Must contain multiple images (batch size > 1)
  - Input shape should be [batch_size, height, width, channels]

- **offset** (Integer)
  - Default: -1
  - Range: -100 to 100
  - Controls how many positions to shift the images
  - Positive values shift images forward in the sequence
  - Negative values shift images backward in the sequence
  - The shift wraps around (circular shift)

## Outputs

- **images** (IMAGE)
  - The reordered batch of images
  - Same shape as input, but with images shifted to new positions

## How It Works

1. The node takes a batch of images and an offset value
2. Calculates the effective offset using modulo operation to handle wrapping
3. Performs a circular shift of the images by the specified offset
4. For example, with offset = -1:
   - Image 1 → moves to last position
   - Image 2 → moves to position 1
   - Image 3 → moves to position 2
   - And so on...

## Common Use Cases

1. **Animation Frame Adjustment**
   - Shift animation frames to adjust timing
   - Create loop points in animated sequences
   - Fix frame order issues in batch-generated animations

2. **Batch Processing Order**
   - Reorder batch-processed images without regenerating
   - Adjust sequence alignment in multi-batch operations
   - Create variations in image sequence patterns

3. **Creative Effects**
   - Create interesting transitions between images
   - Generate rhythmic patterns in image sequences
   - Experiment with different ordering effects

## Notes

- The node requires a batch of multiple images to function
- If a single image is provided, the node will pass it through unchanged with a warning
- The offset wraps around the batch size, so an offset of the batch size (or its negative) results in no change
- Useful for post-processing adjustments without needing to regenerate images
