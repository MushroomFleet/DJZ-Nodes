# WinampViz V2 Visualizations

This directory contains visualization modules for the WinampViz V2 node. Each visualization is stored as a `.viz` file containing Python code that implements the visualization.

## Visualization File Format

Each `.viz` file must implement a `render` function with the following signature:

```python
def render(features, width, height, color_palette, state=None):
    """
    Renders a frame of the visualization.
    
    Args:
        features (dict): Audio features including:
            - 'waveform': numpy array of raw audio samples
            - 'spectrum': numpy array of frequency spectrum
            - 'bass': float value representing bass intensity (0-1)
            - 'mids': float value representing mids intensity (0-1)
            - 'highs': float value representing highs intensity (0-1)
        width (int): Output image width
        height (int): Output image height
        color_palette (list): List of (R,G,B) tuples for colors
        state (dict, optional): State dictionary for maintaining visualization state
            between frames. If provided, the function should return (image, state)
    
    Returns:
        numpy.ndarray or tuple: RGB image of the visualization, or (image, state) tuple
        if state management is needed
    """
```

## Creating New Visualizations

1. Create a new `.viz` file with your visualization name (e.g., `my_visualization.viz`)
2. Import required libraries (numpy and cv2 are commonly used)
3. Implement the `render` function following the signature above
4. Place the file in this directory

### State Management

If your visualization needs to maintain state between frames (e.g., particle systems), use the optional `state` parameter:

```python
def render(features, width, height, color_palette, state=None):
    if state is None:
        state = {'my_state_var': initial_value}
    
    # Use and update state
    state['my_state_var'] = new_value
    
    return image, state
```

### Audio Features

The `features` dictionary provides several audio analysis values:
- `waveform`: Raw audio samples for oscilloscope-style visualizations
- `spectrum`: Frequency spectrum data for spectrum analyzers
- `bass`: Low frequency intensity (0-1)
- `mids`: Mid frequency intensity (0-1)
- `highs`: High frequency intensity (0-1)

### Color Palettes

The `color_palette` parameter provides a list of RGB tuples. Common palettes include:
- Classic: Blue, cyan, green
- Rainbow: Full spectrum of colors
- Fire: Red, orange, yellow
- Matrix: Dark green to bright green

## Example Visualization

Here's a simple example that creates a pulsing circle:

```python
import numpy as np
import cv2

def render(features, width, height, color_palette):
    image = np.zeros((height, width, 3), dtype=np.uint8)
    center = (width // 2, height // 2)
    radius = int(100 * (1 + features['bass']))
    color = color_palette[0]
    cv2.circle(image, center, radius, color, -1)
    return image
```

## Tips for Creating Visualizations

1. Use NumPy operations where possible for better performance
2. Consider using cv2's drawing functions for efficient rendering
3. Normalize and clamp values to prevent visual artifacts
4. Use audio features creatively - combine them for interesting effects
5. Add motion blur or glow effects for smoother animations
6. Consider both low and high intensity audio scenarios
7. Test with different types of audio input

## Available Visualizations

- `oscilloscope.viz`: Classic waveform display
- `spectrum.viz`: Frequency spectrum analyzer
- `particle_storm.viz`: Particle system reacting to audio
- `plasma_wave.viz`: Plasma effect modulated by audio
- `milkdrop_bars.viz`: Milkdrop-style spectrum bars
- `circular_wave.viz`: Concentric circles reacting to audio
- `butterfly.viz`: Parametric butterfly curve visualization
- `tunnel_beat.viz`: Beat-reactive tunnel effect
