# Black Bars V1

A ComfyUI custom node that adds letterboxing or pillarboxing effects to images. This node allows you to add professional-looking black bars to your images with optional feathered edges for a smoother transition.

## Description

The Black Bars V1 node provides two types of black bar effects:
- **Letterboxing**: Adds horizontal black bars at the top and bottom of the image
- **Pillarboxing**: Adds vertical black bars at the left and right sides of the image

Both effects can be customized with adjustable bar size and edge feathering for professional-looking results.

## Parameters

### Box Mode
- Type: Dropdown Selection
- Options: 
  - `letterbox`: Adds horizontal bars (top and bottom)
  - `pillarbox`: Adds vertical bars (left and right)
- Default: `letterbox`
- Description: Determines the orientation of the black bars

### Bar Size
- Type: Integer Slider
- Range: 0 to 500 pixels
- Default: 100
- Step: 1
- Description: Controls the thickness of the black bars. A value of 0 means no bars, while higher values create thicker bars.

### Bar Feather
- Type: Integer Slider
- Range: 0 to 50 pixels
- Default: 0
- Step: 1
- Description: Creates a soft gradient edge between the image and the black bars. A value of 0 creates sharp edges, while higher values create smoother transitions.

## Usage Examples

1. **Classic Cinematic Look**
   - Box Mode: letterbox
   - Bar Size: 100
   - Bar Feather: 0
   - Result: Creates the classic movie theater aspect ratio look

2. **Soft Letterboxing**
   - Box Mode: letterbox
   - Bar Size: 80
   - Bar Feather: 20
   - Result: Adds gentle horizontal bars with soft edges

3. **Vertical Format**
   - Box Mode: pillarbox
   - Bar Size: 150
   - Bar Feather: 10
   - Result: Creates a vertical-oriented frame with slightly feathered edges

## Technical Details

- Input: Accepts image tensors of shape (B, H, W, C)
- Output: Returns processed images with the same dimensions
- Processing: Performed on GPU if available, falls back to CPU if necessary
- Implementation: Uses PyTorch for efficient tensor operations

## Notes

- The bar size is applied to both sides (top/bottom for letterbox, left/right for pillarbox)
- Feathering creates a gradient effect that transitions from full transparency to full black
- The node preserves the original image dimensions while adding the black bar effect
- Processing is done in place without changing the image resolution
