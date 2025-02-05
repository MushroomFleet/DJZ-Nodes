# VGA Effect v1 Node

A ComfyUI node that simulates the distinctive visual characteristics of VGA (Video Graphics Array) displays. This node recreates various artifacts and limitations of VGA monitor technology, including resolution constraints, scan lines, phosphor persistence, and signal interference.

## Parameters

### Resolution Settings

- **horizontal_resolution** (320 - 1024, default: 640)
  - Sets the horizontal pixel count
  - Must be divisible by 8
  - Common values: 640, 800, 1024

- **vertical_resolution** (240 - 768, default: 480)
  - Sets the vertical pixel count
  - Must be divisible by 8
  - Common values: 480, 600, 768

- **refresh_rate** (30 - 75, default: 60)
  - Monitor refresh rate in Hz
  - Affects temporal artifacts
  - Common values: 60, 72, 75

### Display Artifacts

- **scan_line_intensity** (0.0 - 1.0, default: 0.15)
  - Darkness of horizontal scan lines
  - Higher values create more visible lines
  - Lower values create subtle effect

- **phosphor_persistence** (0.0 - 1.0, default: 0.2)
  - Simulates phosphor afterglow
  - Higher values create longer trails
  - Affects vertical motion blur

- **color_bleed** (0.0 - 1.0, default: 0.3)
  - Controls color spreading
  - Higher values increase bleeding
  - Affects color separation

### Signal Effects

- **signal_noise** (0.0 - 0.5, default: 0.05)
  - Adds random noise to image
  - Simulates interference
  - Higher values increase noise

- **horizontal_sync_jitter** (0.0 - 5.0, default: 0.5)
  - Horizontal image stability
  - Higher values increase wobble
  - Affects line alignment

- **vertical_sync_jitter** (0.0 - 2.0, default: 0.2)
  - Vertical image stability
  - Higher values increase bounce
  - Affects frame alignment

## Technical Details

### Resolution Processing
- Downscaling to VGA resolution
- Nearest-neighbor upscaling
- Maintains pixel grid alignment
- Proper aspect ratio handling

### Scan Line Implementation
- Alternating intensity pattern
- Even/odd line differentiation
- Proper vertical spacing
- Intensity modulation

### Color Processing
- Channel-specific blur
- Directional color bleeding
- RGB channel separation
- Signal noise integration

### Sync Effects
- Per-line horizontal jitter
- Per-column vertical jitter
- Gaussian distribution
- Edge handling

## Common Resolutions

1. Standard VGA (640x480)
   - Most compatible
   - 4:3 aspect ratio
   - Classic PC resolution

2. SVGA (800x600)
   - Higher quality
   - Still maintains VGA characteristics
   - Good for detailed content

3. Extended VGA (1024x768)
   - Maximum supported resolution
   - Sharper image quality
   - Less pronounced artifacts

## Usage Tips

1. For Classic VGA Look:
   - Use 640x480 resolution
   - 60Hz refresh rate
   - Moderate scan line intensity (0.15-0.25)
   - Example settings:
     - scan_line_intensity: 0.15
     - phosphor_persistence: 0.2
     - color_bleed: 0.3

2. For Poor Signal Quality:
   - Increase jitter values
   - Add more signal noise
   - Enhance color bleed
   - Example settings:
     - horizontal_sync_jitter: 2.0-3.0
     - vertical_sync_jitter: 1.0-1.5
     - signal_noise: 0.2-0.3

3. For High-Quality VGA:
   - Higher resolution (800x600 or 1024x768)
   - Minimal signal noise
   - Subtle scan lines
   - Example settings:
     - scan_line_intensity: 0.1
     - signal_noise: 0.02
     - color_bleed: 0.1

4. For Motion Effects:
   - Increase phosphor persistence
   - Add moderate sync jitter
   - Example settings:
     - phosphor_persistence: 0.4-0.6
     - horizontal_sync_jitter: 1.0
     - vertical_sync_jitter: 0.5

## Common Applications

1. Retro PC Aesthetics:
   - Emulate old computer displays
   - Create period-appropriate graphics
   - Simulate software interfaces

2. Video Game Nostalgia:
   - Recreate classic game visuals
   - Add authenticity to pixel art
   - Simulate arcade monitors

3. Technical Malfunction:
   - Create interference effects
   - Simulate poor connections
   - Add digital artifacts

4. Artistic Effects:
   - Creative use of scan lines
   - Motion trail effects
   - Color separation art

## Technical Considerations

1. Performance Impact:
   - Higher resolutions increase processing time
   - Multiple effects compound processing load
   - Batch processing considerations

2. Resolution Handling:
   - Input images are resized to match VGA specs
   - Maintain aspect ratio awareness
   - Consider final output size

3. Quality Control:
   - Monitor color accuracy
   - Check for unwanted artifacts
   - Verify temporal consistency

4. Compatibility:
   - Works with both still images and video
   - Supports batch processing
   - Resolution-independent output
