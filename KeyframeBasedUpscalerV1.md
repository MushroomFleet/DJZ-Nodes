# KeyframeBasedUpscaler v1

A smart video upscaling node that efficiently processes video sequences by identifying and upscaling key frames while using temporal blending for intermediate frames. This approach provides a balance between quality and processing speed.

## Parameters

### Scale Factor
- **Type:** Float
- **Default:** 2.0
- **Range:** 1.0 to 4.0
- **Step:** 0.5
- **Description:** Determines how much to upscale the video. A value of 2.0 will double both width and height, 3.0 will triple them, etc.

### Keyframe Threshold
- **Type:** Float
- **Default:** 30.0
- **Range:** 0.0 to 100.0
- **Step:** 1.0
- **Description:** Controls how sensitive the system is to detecting new keyframes. Lower values create more keyframes, resulting in higher quality but slower processing. Higher values create fewer keyframes, prioritizing speed over quality.

### Temporal Window
- **Type:** Integer
- **Default:** 5
- **Range:** 1 to 15
- **Step:** 1
- **Description:** Specifies how many surrounding frames to consider when blending intermediate frames. A larger window can create smoother transitions but may blur motion. A smaller window preserves more detail but may show more artifacts in high-motion scenes.

### Quality Preservation
- **Type:** Float
- **Default:** 0.8
- **Range:** 0.0 to 1.0
- **Step:** 0.1
- **Description:** Controls the balance between temporal smoothing and frame sharpness:
- Values closer to 1.0 preserve more detail and apply additional sharpening
- Values closer to 0.0 prioritize smooth transitions between frames
- The default of 0.8 provides a good balance between detail and smoothness

### Motion Sensitivity
- **Type:** Float
- **Default:** 0.5
- **Range:** 0.0 to 1.0
- **Step:** 0.1
- **Description:** Determines how much motion influences keyframe detection:
- Higher values make the system more sensitive to motion, creating more keyframes in high-motion scenes
- Lower values focus more on structural changes in the image
- At 0.0, motion is ignored entirely and only structural changes trigger keyframes

### Interpolation Method
- **Type:** Integer
- **Default:** 0
- **Range:** 0 to 2
- **Step:** 1
- **Description:** Selects the algorithm used for upscaling keyframes:
- 0: Linear interpolation (fastest, lower quality)
- 1: Cubic interpolation (balanced speed/quality)
- 2: Lanczos interpolation (slowest, highest quality)

## Usage Tips

1. **For High-Motion Content:**
   - Increase Motion Sensitivity (0.7-0.9)
   - Lower Keyframe Threshold (15-25)
   - Use smaller Temporal Window (3-5)

2. **For Static/Slow Content:**
   - Lower Motion Sensitivity (0.2-0.4)
   - Increase Keyframe Threshold (35-45)
   - Use larger Temporal Window (7-10)

3. **For Maximum Quality:**
   - Set Quality Preservation to 1.0
   - Use Interpolation Method 2 (Lanczos)
   - Lower Keyframe Threshold
   - Use smaller Temporal Window

4. **For Faster Processing:**
   - Set Quality Preservation to 0.5-0.7
   - Use Interpolation Method 0 (Linear)
   - Increase Keyframe Threshold
   - Use larger Temporal Window

## How It Works

The node uses a sophisticated frame analysis system that:
1. Analyzes frames using multi-scale features and edge detection
2. Identifies key frames based on structural changes and motion
3. Applies high-quality upscaling to keyframes
4. Uses temporal blending with gaussian weighting for intermediate frames
5. Processes frames in parallel for improved performance

This approach allows for efficient upscaling while maintaining visual quality, particularly useful for longer video sequences where processing every frame at high quality would be time-consuming.
