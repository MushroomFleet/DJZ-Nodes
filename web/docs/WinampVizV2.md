# WinampVizV2 Node

A ComfyUI custom node that generates Winamp-style audio visualizations from audio input. This node creates dynamic visual representations of audio data, similar to the classic Winamp music player visualizations, with support for extensible visualization plugins.

## 🎯 Features

- Customizable audio visualizations through plugin system
- Multiple color schemes
- Adjustable sensitivity and smoothing
- Support for various audio input formats
- Extensible visualization system using .viz files
- Real-time FFT (Fast Fourier Transform) audio analysis

## 📝 Parameters

### Required Inputs

- **audio**: Audio input data (AUDIO type)
- **width**: Width of the output visualization (64-4096 pixels, default: 512)
- **height**: Height of the output visualization (64-4096 pixels, default: 512)
- **fps**: Frames per second (1-60 fps, default: 30)
- **max_frames**: Maximum number of frames to generate (0-9999, default: 0)
  - Set to 0 for automatic frame count based on audio length
- **visualization**: Select from available visualization plugins in the VIZ directory
- **color_scheme**: Choose from available color palettes:
  - `classic`: Blue to cyan to green
  - `rainbow`: Full spectrum color rotation
  - `fire`: Red to orange to yellow
  - `matrix`: Dark green to bright green
- **sensitivity**: Audio response sensitivity (0.1-5.0, default: 1.0)
  - Higher values amplify the audio response
  - Lower values reduce the visualization intensity
- **smoothing**: Temporal smoothing factor (0.0-0.99, default: 0.5)
  - Higher values create smoother transitions
  - Lower values provide more immediate response

## 🎨 Color Schemes

1. **classic**
   - Primary colors: Blue → Cyan → Green
   - Classic Winamp-inspired look

2. **rainbow**
   - Full spectrum of colors
   - Cycles through 12 different hues

3. **fire**
   - Warm color palette: Red → Orange → Yellow
   - Creates a flame-like effect

4. **matrix**
   - Matrix-inspired greens
   - Dark to bright green progression

## 🔧 Technical Details

### Audio Processing

The node processes audio using the following steps:

1. Chunks the audio data based on the specified FPS
2. Performs FFT (Fast Fourier Transform) analysis
3. Extracts frequency bands:
   - Bass (lowest 10% of frequencies)
   - Mids (10%-50% of frequency range)
   - Highs (50%-100% of frequency range)
4. Applies smoothing between frames
5. Adjusts response based on sensitivity setting

### Visualization System

The node uses a plugin system for visualizations:

- Visualizations are stored as `.viz` files in the `VIZ` directory
- Each visualization plugin must implement a `render` function
- Plugins can maintain state between frames
- Automatically loads all valid visualization plugins at startup

## 🔌 Creating Custom Visualizations

Custom visualizations can be added by creating a `.viz` file in the VIZ directory. Each visualization file must implement:

```python
def render(features, width, height, color_palette, state=None):
    """
    Parameters:
    - features: Dict containing 'spectrum', 'waveform', 'bass', 'mids', 'highs'
    - width: Output image width
    - height: Output image height
    - color_palette: List of RGB tuples for visualization
    - state: Optional persistent state between frames
    
    Returns:
    - frame: numpy array of shape (height, width, 3)
    - state: Optional state to persist (if needed)
    """
```

## 🎬 Output

- Returns an IMAGE type containing the generated visualization frames
- Output is normalized to float values between 0 and 1
- RGB color format (3 channels)
- Batch dimension represents frames

## 💡 Tips

1. Adjust sensitivity based on your audio input level
2. Use smoothing to control visualization stability
3. Choose color schemes that complement your project
4. Experiment with different visualizations for varied effects
5. Consider FPS and max_frames for performance optimization
