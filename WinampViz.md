# WinampViz Node

A ComfyUI custom node that generates Winamp-style visualizations from audio input, offering various classic visualization styles reminiscent of the golden age of media players.

## 🎵 Description

WinampViz transforms audio input into dynamic visual representations, offering 8 different visualization styles with customizable parameters. Each visualization style reacts to different aspects of the audio (bass, mids, highs) to create engaging visual effects.

## 📊 Parameters

- **audio**: Audio input tensor (Required)
- **width**: Width of the output visualization
  - Default: 512
  - Range: 64-4096
  - Step: 64
- **height**: Height of the output visualization
  - Default: 512
  - Range: 64-4096
  - Step: 64
- **fps**: Frames per second for the visualization
  - Default: 30
  - Range: 1-60
  - Step: 1
- **max_frames**: Maximum number of frames to generate (0 = unlimited)
  - Default: 0
  - Range: 0-9999
  - Step: 1
- **viz_type**: Visualization style to use
  - Options:
    - oscilloscope: Classic waveform display
    - spectrum: Frequency spectrum analyzer
    - particle_storm: Dynamic particle system
    - plasma_wave: Plasma-style wave effects
    - milkdrop_bars: MilkDrop-inspired frequency bars
    - circular_wave: Circular waveform visualization
    - butterfly: Butterfly curve animation
    - tunnel_beat: Beat-reactive tunnel effect
- **color_scheme**: Color palette for the visualization
  - Options:
    - classic: Blue and cyan theme
    - rainbow: Full spectrum colors
    - fire: Red and yellow heat colors
    - matrix: Green digital theme
- **sensitivity**: Audio reactivity sensitivity
  - Default: 1.0
  - Range: 0.1-5.0
  - Step: 0.1
- **smoothing**: Smoothing factor between frames
  - Default: 0.5
  - Range: 0.0-0.99
  - Step: 0.01

## 🎨 Visualization Types

### 1. Oscilloscope
Classic waveform display showing the audio amplitude over time. Perfect for visualizing the raw audio waveform.

### 2. Spectrum
Frequency spectrum analyzer displaying the audio frequency components as vertical bars. Great for visualizing the frequency distribution of the audio.

### 3. Particle Storm
Dynamic particle system that reacts to audio intensity. Particles emanate from the center with properties influenced by the audio features.

### 4. Plasma Wave
Generates a plasma-like effect modulated by audio features, creating organic, flowing patterns.

### 5. MilkDrop Bars
Inspired by Winamp's MilkDrop visualizer, featuring enhanced frequency bars with glow effects and bass reactivity.

### 6. Circular Wave
Audio-reactive circular waves that expand and contract based on audio features, creating a hypnotic circular pattern.

### 7. Butterfly
Generates a butterfly curve animation that morphs and changes based on the audio input, creating complex geometric patterns.

### 8. Tunnel Beat
Beat-reactive tunnel effect that pulses and glows with the music, creating an immersive tunnel visualization.

## 🎨 Color Schemes

- **Classic**: Blue and cyan theme reminiscent of classic audio visualizers
- **Rainbow**: Full spectrum of colors for vibrant visualizations
- **Fire**: Warm colors ranging from red to yellow, creating a heat-map effect
- **Matrix**: Digital green theme inspired by The Matrix

## 💡 Usage Tips

1. **For Best Results**:
   - Use higher FPS (30-60) for smoother animations
   - Adjust sensitivity based on your audio input level
   - Use smoothing to reduce jitter in the visualization

2. **Performance Considerations**:
   - Higher resolutions and FPS will require more processing power
   - Consider using max_frames to limit the output length for preview purposes

3. **Visualization Selection**:
   - Use oscilloscope or spectrum for traditional audio analysis
   - Choose particle_storm or plasma_wave for more dynamic effects
   - Select tunnel_beat or butterfly for geometric patterns
   - Use milkdrop_bars for classic music visualizer feel

## 🔄 Output

Returns a tensor of image frames that can be further processed or saved as a video.
