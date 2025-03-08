# Zenkai Prompt V5

## Overview
Zenkai Prompt V5 is a custom node for ComfyUI that generates prompts from text files. It allows you to select prompts either sequentially or randomly from a text file, with options to add prefix and suffix text to each prompt. This node is particularly useful for batch processing or when you want to experiment with different prompts using a consistent seed value.

## Installation
This node is part of the DJZ-Nodes collection. No additional installation is required if you already have DJZ-Nodes installed in your ComfyUI environment.

Make sure you have a `prompts` directory in your DJZ-Nodes folder containing text files with prompts (one prompt per line).

## Features
- Load prompts from text files in the `prompts` directory
- Generate one or multiple prompts in a single operation
- Choose between sequential or random prompt selection
- Add custom prefix and suffix text to each prompt
- Seed-based generation for reproducible results

## Parameters

### Required Parameters

#### text_file
Select a text file from the `prompts` directory. Each file should contain prompts with one prompt per line.

#### seed
An integer value that determines which prompts are selected. 
- In sequential mode, the seed determines the starting position in the file
- In random mode, the seed ensures reproducible random selections
- Range: 0 to 4294967295 (0xFFFFFFFF)

#### num_prompts
The number of prompts to generate from the selected text file.
- Range: 1 to 10
- Default: 1

#### mode
Determines how prompts are selected from the text file:
- **sequential**: Selects prompts in order starting from the position determined by the seed value. If the seed plus the number of prompts exceeds the total number of prompts in the file, it will loop back to the beginning.
- **random**: Uses the seed value to randomly select the specified number of prompts from the file.

### Optional Parameters

#### prefix
Text to add before each prompt. This can be useful for adding consistent styling elements or modifiers to all prompts.
- Default: empty string

#### suffix
Text to add after each prompt. This can be useful for adding consistent styling elements or modifiers to all prompts.
- Default: empty string

## Output
The node outputs a single STRING containing all selected prompts joined with commas.

## Usage Examples

### Basic Usage
1. Add the Zenkai Prompt V5 node to your workflow
2. Select a text file containing prompts
3. Set the seed value (e.g., 42)
4. Set the number of prompts to generate (e.g., 1)
5. Choose the mode (e.g., "sequential")
6. Connect the output to a text input of another node (such as a KSampler or CLIP Text Encode node)

### Using Prefix and Suffix
You can use prefix and suffix to add consistent elements to all prompts:

- **Prefix example**: "masterpiece, best quality, "
- **Suffix example**: ", 8k, detailed"

If your text file contains a prompt like "a cat sitting on a windowsill", the final output would be:
"masterpiece, best quality, a cat sitting on a windowsill, 8k, detailed"

### Batch Processing
To create variations using different prompts:
1. Set num_prompts to the number of variations you want
2. Connect the output to a node that supports batch processing
3. Use the same seed for reproducible results or change it for different selections

## Tips and Best Practices

1. **Organizing Prompt Files**: Create different text files for different themes or styles of prompts.

2. **Seed Management**: 
   - Use the same seed value to get consistent prompt selections across different runs
   - Change the seed to get different prompt selections
   - Note the seed value of particularly good results for future reference

3. **Sequential vs Random**:
   - Use sequential mode when you want to systematically work through a list of prompts
   - Use random mode when you want variety but still need reproducibility

4. **Prefix and Suffix**:
   - Use prefix for quality boosters and style settings
   - Use suffix for resolution specifications and additional details

5. **Prompt File Structure**:
   - Keep one prompt per line in your text files
   - Empty lines in the text file are ignored

## Troubleshooting

- If the node returns "No valid prompts found in the file", check that your text file contains non-empty lines.
- If you're not seeing the expected prompts, verify that the seed value is what you expect and that you're using the correct mode.
- Make sure your text files are saved with UTF-8 encoding to support special characters.
