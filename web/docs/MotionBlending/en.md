# Motion Blending Node

A ComfyUI node that creates realistic motion blur and frame blending effects. This node can simulate both camera shutter-based motion blur and temporal frame blending, offering various ways to add motion effects to images and video frames.

## Modes and Styles

### Modes
- **Motion Blur**: Creates directional blur simulating camera or subject movement
- **Frame Blending**: Combines multiple frames for smooth motion transitions

### Styles
- **Simulated Shutter**: Emulates camera shutter motion blur
- **Temporal Blend**: Creates smooth transitions between frames

## Parameters

### Motion Controls

- **intensity** (0.0 - 1.0, default: 0.5)
  - Controls the strength of the motion effect
  - Higher values create more pronounced motion
  - Lower values create subtle movement

- **angle** (-180.0 - 180.0, default: 0.0)
  - Direction of the motion blur in degrees
  - 0° is horizontal right
  - 90° is vertical down
  - -90° is vertical up

- **kernel_size** (3 - 99, default: 15)
  - Size of the motion blur kernel
  - Must be an odd number
  - Larger values create longer motion trails
  - Smaller values create tighter blur

### Blending Controls

- **frames_to_blend** (2 - 10, default: 2)
  - Number of frames to combine in temporal effects
  - Higher values create smoother transitions
  - Also increases processing time

- **decay_factor** (0.0 - 1.0, default: 0.5)
  - Controls how quickly frame influence decreases
  - Higher values maintain frame intensity longer
  - Lower values create faster falloff

## Technical Details

### Motion Blur Implementation
- Custom kernel generation based on angle
- Directional blur using 2D convolution
- Intensity-based kernel weighting
- Proper edge handling

### Frame Blending Implementation
- Progressive frame weight decay
- Spatial offset compensation
- Normalized blending weights
- Temporal coherence preservation

### Processing Pipeline
1. **Kernel Generation**
   - Dynamic kernel creation
   - Angle-based direction vector
   - Intensity-weighted distribution
   - Proper normalization

2. **Shutter Simulation**
   - Convolution-based blur
   - Direction-aware processing
   - Intensity modulation
   - Edge artifact prevention

3. **Temporal Blending**
   - Progressive frame mixing
   - Decay-based weighting
   - Spatial alignment
   - Color accuracy preservation

## Usage Tips

1. For Camera Motion Blur:
   - Use "Motion Blur" mode
   - Select "Simulated Shutter" style
   - Set appropriate angle for movement direction
   - Adjust kernel_size based on speed
   - Example settings:
     - intensity: 0.6-0.8
     - kernel_size: 15-31
     - angle: based on motion direction

2. For Smooth Transitions:
   - Use "Frame Blending" mode
   - Select "Temporal Blend" style
   - Higher frames_to_blend
   - Moderate decay_factor
   - Example settings:
     - frames_to_blend: 3-4
     - decay_factor: 0.7-0.8
     - intensity: 0.4-0.6

3. For Action Shots:
   - Use "Motion Blur" mode
   - Larger kernel_size
   - Higher intensity
   - Angle aligned with action
   - Example settings:
     - kernel_size: 31-51
     - intensity: 0.8-1.0
     - angle: match subject movement

4. For Dreamy Effects:
   - Use "Frame Blending" mode
   - Both styles combined
   - Higher frames_to_blend
   - Lower decay_factor
   - Example settings:
     - frames_to_blend: 5-7
     - decay_factor: 0.3-0.4
     - intensity: 0.7-0.9

## Common Applications

1. Action Photography:
   - Simulate motion blur for static shots
   - Add dynamism to still images
   - Create speed effects

2. Video Transitions:
   - Smooth frame interpolation
   - Creative transition effects
   - Motion-based blending

3. Special Effects:
   - Ghosting effects
   - Speed ramping simulation
   - Motion trails

4. Creative Blur:
   - Directional emphasis
   - Motion suggestion
   - Abstract effects

## Technical Considerations

1. Performance Impact:
   - Larger kernel_size increases processing time
   - More frames_to_blend increases memory usage
   - Consider batch size when processing multiple frames

2. Quality Control:
   - Monitor edge artifacts
   - Check for color accuracy
   - Verify temporal consistency

3. Resolution Handling:
   - Effects scale with image resolution
   - Adjust kernel_size for different resolutions
   - Consider final output format
