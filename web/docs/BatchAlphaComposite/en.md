# Batch Alpha Composite Node

The Batch Alpha Composite node is an image processing node that allows you to combine two batches of images using alpha compositing. This is particularly useful when you want to overlay images that have transparency (RGBA) on top of background images (RGB).

## Inputs

### Required Inputs

1. **bottom_images** (IMAGE)
   - The bottom layer batch of images
   - Format: RGB (3 channels)
   - Shape: (Batch, Height, Width, 3)
   - Value range: [0, 1]
   - This serves as the background layer

2. **top_images** (IMAGE)
   - The top layer batch of images
   - Format: RGBA (4 channels)
   - Shape: (Batch, Height, Width, 4)
   - Value range: [0, 1]
   - This serves as the foreground layer with transparency

## Output

- Returns a single IMAGE output
- Format: RGB (3 channels)
- Shape: Same as input (Batch, Height, Width, 3)
- Value range: [0, 1]

## How It Works

The node performs alpha compositing using the standard alpha blending formula:

```
result = (alpha * foreground) + ((1 - alpha) * background)
```

For each image in the batch:
1. The alpha channel is extracted from the top image
2. The RGB channels from both images are blended according to the alpha values
3. Areas where alpha = 1 will show the top image completely
4. Areas where alpha = 0 will show the bottom image completely
5. Values between 0 and 1 create a proportional blend

## Use Cases

- Overlaying transparent PNG images onto backgrounds
- Combining multiple layers with transparency
- Creating composite images with smooth blending
- Batch processing of image overlays

## Error Handling

The node includes validation to ensure:
- Bottom layer images must be in RGB format (3 channels)
- Top layer images must be in RGBA format (4 channels)
- Both batches must have compatible dimensions

If these conditions are not met, the node will raise an appropriate error message.
