# Dead Pixel Effect Node

A specialized image effect node that simulates various types of pixel defects commonly found in digital cameras and displays. This node can create realistic screen artifacts including dead pixels, stuck pixels, hot pixels, and subpixel defects.

## Input Parameters

### Required Inputs

1. **images** (IMAGE)
   - The input batch of images to apply the effect to

2. **defect_mode** (COMBO)
   - Options: ["DEAD_BLACK", "DEAD_WHITE", "STUCK_COLOR", "HOT_PIXEL", "SUBPIXEL", "CLUSTER"]
   - Determines the type of pixel defect to simulate:
     - DEAD_BLACK: Pixels that don't light up (appear black)
     - DEAD_WHITE: Pixels stuck at maximum brightness (appear white)
     - STUCK_COLOR: Pixels stuck at a random color value
     - HOT_PIXEL: Bright pixels that appear brighter than surrounding pixels
     - SUBPIXEL: Defects affecting specific RGB subpixels
     - CLUSTER: Groups of defective pixels

3. **seed** (INT)
   - Default: 0
   - Range: 0 to 0xffffffffffffffff
   - Controls the random generation of defects
   - Same seed will produce consistent results

4. **defect_rate** (FLOAT)
   - Default: 0.001 (0.1%)
   - Range: 0.0001 to 0.1 (0.01% to 10%)
   - Step: 0.0001
   - Percentage of pixels that will be affected by defects

5. **cluster_size** (INT)
   - Default: 1
   - Range: 1 to 10
   - Step: 1
   - Size of defect clusters (in pixels)
   - Higher values create groups of adjacent defective pixels

6. **color_intensity** (FLOAT)
   - Default: 1.0
   - Range: 0.0 to 1.0
   - Step: 0.1
   - Controls the intensity of color defects
   - Affects STUCK_COLOR, HOT_PIXEL, and CLUSTER modes

7. **flicker_rate** (FLOAT)
   - Default: 0.0
   - Range: 0.0 to 1.0
   - Step: 0.1
   - Proportion of defects that change between frames
   - 0.0 = static defects, 1.0 = all defects flicker

8. **subpixel_mode** (COMBO)
   - Options: ["RED", "GREEN", "BLUE", "RANDOM"]
   - Determines which color channel is affected in SUBPIXEL mode
   - RANDOM will choose a random channel for each defect

## Output

- Returns a single IMAGE output
- Same dimensions and format as input
- Contains the original image with simulated pixel defects

## How It Works

1. **Defect Generation**
   - Creates a mask of defective pixel locations based on defect_rate
   - Applies cluster_size to group defects together
   - Generates both static (permanent) and flickering defects based on flicker_rate

2. **Defect Application**
   - DEAD_BLACK: Sets pixels to 0 (black)
   - DEAD_WHITE: Sets pixels to 1 (white)
   - STUCK_COLOR: Assigns random color values scaled by color_intensity
   - HOT_PIXEL: Creates bright spots with random color variation
   - SUBPIXEL: Affects individual RGB channels
   - CLUSTER: Creates groups of related defects

3. **Batch Processing**
   - Processes each image in the batch independently
   - Maintains consistent static defects across frames
   - Generates new random defects for flickering pixels

## Use Cases

- Simulating damaged camera sensors
- Creating realistic screen defect effects
- Adding character to digital display simulations
- Creating glitch art effects
- Testing image processing algorithms' robustness

## Tips

- Use low defect_rate values (0.001-0.005) for realistic camera sensor defects
- Increase cluster_size for LCD/LED display defect simulation
- Combine with other effects like bloom or blur for more realistic results
- Use flicker_rate to create dynamic, animated defects
- Experiment with subpixel_mode for LCD-specific artifacts
