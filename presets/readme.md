# UncleanSpeech Presets

This directory contains preset configurations for the UncleanSpeech node. Each preset is stored as a `.preset` file containing JSON configuration data that defines a specific audio processing effect chain.

## Preset File Format

Each `.preset` file is a JSON document with the following structure:

```json
{
    "name": "Preset Name",
    "description": "Description of the audio effect",
    
    "compression_ratio": 1.0,
    "compression_threshold": -20.0,
    
    "low_cut": 20.0,
    "high_cut": 20000.0,
    
    "distortion_amount": 0.0,
    
    "noise_level": 0.0,
    "noise_color": "white",
    
    "reverb_amount": 0.0,
    "room_size": 0.5,
    
    "metadata": {
        "category": "Category",
        "era": "Time period",
        "quality": "Quality level",
        "characteristics": [
            "characteristic 1",
            "characteristic 2"
        ],
        "technical_specs": {
            "spec1": "value1",
            "spec2": "value2"
        }
    }
}
```

## Parameter Descriptions

### Required Parameters
- **name**: Display name of the preset
- **description**: Brief description of the audio effect

### Audio Processing Parameters
- **compression_ratio** (1.0 - 20.0)
  - Controls dynamic range compression intensity
  - Higher values = more aggressive compression
  - 1.0 = no compression

- **compression_threshold** (-60.0 - 0.0 dB)
  - Level where compression begins
  - Lower values affect more of the signal

- **low_cut** (20.0 - 2000.0 Hz)
  - Low-frequency cutoff point
  - Frequencies below this are attenuated

- **high_cut** (1000.0 - 20000.0 Hz)
  - High-frequency cutoff point
  - Frequencies above this are attenuated

- **distortion_amount** (0.0 - 1.0)
  - Controls harmonic distortion intensity
  - 0.0 = clean, 1.0 = maximum distortion

- **noise_level** (0.0 - 1.0)
  - Amount of added noise
  - 0.0 = no noise, 1.0 = maximum noise

- **noise_color** ("white", "pink", "brown")
  - Spectral character of the noise
  - white: Equal energy per frequency
  - pink: -3dB/octave slope
  - brown: -6dB/octave slope

- **reverb_amount** (0.0 - 1.0)
  - Wet/dry mix of reverb effect
  - 0.0 = dry, 1.0 = fully wet

- **room_size** (0.1 - 1.0)
  - Simulated room size for reverb
  - Affects reverb length and density

### Optional Metadata
- **category**: Type of effect (e.g., "Analog", "Digital", "Environment")
- **era**: Time period the effect represents
- **quality**: Quality level description
- **characteristics**: Array of key sound characteristics
- **technical_specs**: Technical specifications object
- **variants**: Alternative parameter sets for the preset

## Creating New Presets

1. Create a new `.preset` file with your preset name (e.g., `my_effect.preset`)
2. Define the required parameters and any optional metadata
3. Use valid JSON format with the structure shown above
4. Place the file in this directory

### Tips for Creating Presets

1. Start with all parameters at default values and adjust one at a time
2. Test with various types of audio input
3. Consider the historical accuracy for vintage equipment emulation
4. Use metadata to document the effect's characteristics
5. Include technical specifications when emulating real equipment
6. Consider adding variants for different quality levels or conditions
7. Keep descriptions clear and specific

## Example Preset

Here's a simple example that creates a low-quality telephone effect:

```json
{
    "name": "Old Telephone",
    "description": "Simulates an old telephone connection with limited bandwidth and noise",
    
    "compression_ratio": 4.0,
    "compression_threshold": -15.0,
    
    "low_cut": 300.0,
    "high_cut": 3400.0,
    
    "distortion_amount": 0.2,
    
    "noise_level": 0.05,
    "noise_color": "white",
    
    "reverb_amount": 0.1,
    "room_size": 0.3,
    
    "metadata": {
        "category": "Communication",
        "era": "1950s",
        "quality": "Telephone Network",
        "characteristics": [
            "bandwidth limited",
            "line noise",
            "slight distortion"
        ],
        "technical_specs": {
            "frequency_response": "300Hz-3.4kHz",
            "dynamic_range": "~30dB"
        }
    }
}
```

## Available Presets

- `cassette.preset`: Emulates analog cassette tape characteristics
- `film.preset`: Simulates optical film sound recording
- `intercom.preset`: Recreates intercom system audio
- `phone.preset`: Simulates telephone connection
- `radio.preset`: Emulates AM/FM radio reception
- `tv.preset`: Recreates vintage television audio
- `vinyl.preset`: Simulates vinyl record playback
- `walkie_talkie.preset`: Emulates two-way radio communication
