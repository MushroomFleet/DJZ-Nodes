# Zenkai Depth Prompt

## Description
The Zenkai Depth Prompt node allows you to load depth maps and their associated prompts from a directory structure. It supports filtering prompts using a whitelist feature, which only selects prompts containing specific words or phrases.

## Inputs

### Required
- **prompt_folder**: Select which subfolder in the "depthprompts" directory to use.
- **seed**: Seed value for random or sequential selection.
- **mode**: Choose between "sequential" or "random" selection modes.
- **num_images**: Number of depth maps to load (1-10).

### Optional
- **whitelist**: A comma-separated list of words or phrases that should be present in the prompts to include them. Phrases with multiple words should be enclosed in quotes.
  - Example: `photo, man, "man holding", landscape`

## Outputs
- **IMAGE**: The selected depth map(s) as an image tensor.
- **STRING**: The associated text prompt(s) joined with " | " as separators.

## Usage
1. Create a subfolder in the "depthprompts" directory.
2. Add depth map files (.jpg, .jpeg, or .png) with matching .txt files containing prompt descriptions.
   - Example: If you have `depth001.png`, create `depth001.txt` with the prompt text.
3. Use the whitelist parameter to filter which prompts are selected based on content.

## Whitelist Feature
The whitelist filtering allows you to specify words or phrases that must appear in a prompt for it to be selected:
- Simple words: `photo, man, landscape`
- Phrases (use quotes): `"man holding", "depth map of landscape"`

If no whitelist is specified, all depth map/prompt pairs will be considered for selection.
