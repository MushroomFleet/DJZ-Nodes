# Video Trails Effect

The Video Trails Effect node creates dynamic motion trails in video sequences by analyzing frame-to-frame motion and generating persistent afterimages. It uses optical flow detection to identify moving elements and applies configurable trail effects to these areas.

## Input Parameters

### Required

- **images**: The input batch of images/frames to process

- **persistence** (0.1 - 0.99, default: 0.85)
  - Controls how long the trails remain visible
  - Higher values make trails persist longer
  - Lower values cause trails to fade more quickly

- **fade_speed** (0.01 - 0.5, default: 0.15)
  - Controls how quickly trails fade in areas without motion
  - Higher values make trails disappear faster in static areas
  - Lower values maintain trails longer even without new motion

- **intensity** (0.1 - 2.0, default: 1.0)
  - Controls the strength of the trail effect
  - Values above 1.0 create brighter, more pronounced trails
  - Values below 1.0 create subtler, more transparent trails

- **motion_threshold** (0.01 - 0.2, default: 0.05)
  - Determines how much motion is required to generate trails
  - Higher values require more significant movement to create trails
  - Lower values make the effect more sensitive to subtle movements

- **blur_strength** (0.0 - 1.0, default: 0.0)
  - Controls the amount of motion blur applied to the trails
  - 0.0 disables motion blur completely
  - Higher values create smoother, more blended trails

## How It Works

1. The node processes frames sequentially, analyzing motion between consecutive frames using optical flow detection.
2. When motion is detected above the threshold, it creates trails by blending the current frame with the accumulated trail buffer.
3. In areas without motion, existing trails gradually fade based on the fade_speed parameter.
4. Optional motion blur can be applied to create smoother trail effects.

## Usage Tips

1. **For Smooth Trails**:
   - Use higher persistence (0.9+)
   - Set lower fade_speed (0.05-0.1)
   - Enable slight blur_strength (0.2-0.4)

2. **For Sharp, Quick Trails**:
   - Use lower persistence (0.5-0.7)
   - Set higher fade_speed (0.2-0.3)
   - Keep blur_strength at 0

3. **For Subtle Effects**:
   - Increase motion_threshold (0.1+)
   - Lower intensity (0.5-0.8)
   - Use moderate persistence (0.7-0.8)

4. **For Dramatic Effects**:
   - Lower motion_threshold (0.02-0.04)
   - Increase intensity (1.2-1.5)
   - Use high persistence (0.95+)

## Output

- Returns the processed image batch with motion trails applied
- Output maintains the same dimensions and format as the input
- Each frame contains the accumulated trails from previous frames

## Note

The effect works best with video sequences that have clear motion and good contrast. Very fast or chaotic motion might require adjusting the motion_threshold and persistence values to achieve the desired result. The effect processes frames sequentially, so the first frame won't show any trails as it needs at least two frames to detect motion.
