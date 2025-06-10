# Combine Audio Tracks Node

A ComfyUI custom node that allows you to mix two audio tracks together with volume control for each track.

## Description

The Combine Audio node takes two audio inputs and merges them into a single audio track while providing independent volume control for each input. This is particularly useful for:
- Adding background music to voice recordings
- Mixing multiple audio tracks
- Creating layered audio effects

## Parameters

### Required Inputs
- **audio1**: First audio input track (AUDIO type)
- **audio2**: Second audio input track (AUDIO type)
- **volume1**: Volume multiplier for the first audio track
  - Default: 1.0
  - Range: 0.0 to 2.0
  - Step: 0.1
- **volume2**: Volume multiplier for the second audio track
  - Default: 1.0
  - Range: 0.0 to 2.0
  - Step: 0.1

### Output
- Returns a combined AUDIO track

## How It Works

1. The node loads both input audio tracks using pydub
2. Applies volume adjustments to each track independently
   - Volume is converted from linear scale to decibels (dB)
   - A volume of 1.0 means no change
   - Values below 1.0 decrease volume
   - Values above 1.0 increase volume (up to 2.0x)
3. Automatically matches the length of both tracks
   - If one track is longer, the shorter track is padded with silence
4. Overlays the tracks together while preserving both audio streams
5. Exports the result as a new audio file

## Technical Details

- Output Format: MP4 audio
- Volume Conversion: Uses 20 * log10(volume) for dB conversion
- Length Matching: Automatic padding with silence
- Error Handling: Returns the first audio track if combination fails

## Dependencies

- pydub: Audio processing library

## Usage Example

1. Connect two audio sources to the node's audio1 and audio2 inputs
2. Adjust volume1 and volume2 to balance the audio levels
3. The combined audio will be available at the output

Note: The node automatically handles different length audio files by padding the shorter one with silence to match the longer track's duration.
