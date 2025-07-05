# Zenkai Ambience Audio

A node for ComfyUI that randomly selects audio files from predefined ambience categories based on a seed value.

## Description

This node allows you to incorporate ambient soundscapes into your ComfyUI workflows. It creates a dropdown list of available ambience categories (subdirectories within the "ambience" folder) and randomly selects an audio file from the chosen category based on the provided seed value. This deterministic selection ensures reproducible results when using the same seed.

## Inputs

- **ambience_folder**: Select the category of ambience audio to use (dropdown menu showing subdirectories within the ambience folder)
- **seed**: Integer value used for random selection of the audio file (any change will result in a different audio file being selected)

## Outputs

- **AUDIO**: Output in ComfyUI's audio format, ready to be processed by other audio nodes or saved to disk

## Usage

1. Add audio files to subdirectories within the "ambience" folder
   - Supported formats: .wav, .mp3, .ogg, .flac
   - Create meaningful subdirectory names for different types of ambience (e.g., "nature", "urban", "indoor")
2. Add the Zenkai Ambience Audio node to your workflow
3. Select the desired ambience category from the dropdown
4. Set a seed value (or connect a seed generator)
5. Connect the output to other audio processing nodes or a save node

## Example

To create a natural environment soundscape for your AI-generated scenes:
1. Place forest sounds, bird calls, water streams, etc. in the "nature" subfolder
2. Select "nature" from the node's dropdown
3. Adjust the seed to get different nature sounds
4. Connect to output or processing nodes

## Notes

- If no audio files are found in the selected directory, an empty audio tensor will be returned
- For deterministic behavior, use the same seed value
- To add more categories, simply create new subdirectories in the "ambience" folder
