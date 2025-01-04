# ZenkaiPrompt V2 Node

## Overview
ZenkaiPromptV2 is an enhanced version of the ZenkaiPrompt node that adds support for multiple prompt selection and text modification. It allows you to select multiple prompts from a text file and optionally add prefix/suffix text to each prompt.

## Parameters

### Required Parameters
- **text_file** (COMBO)
  - Options: List of available .txt files in the prompts directory, including:
    - Various themed prompt collections (e.g., cybersociety, blacksun, cogvideo)
    - Caption files (e.g., assassinKahb-captions.txt, dronecam-captions.txt)
    - Style-specific prompts (e.g., LTXV-dialogue-closeups.txt, Mochi-Photo-256.txt)
  - Description: The source text file to select prompts from

- **seed** (INT)
  - Default: 0
  - Minimum: 0
  - Maximum: 4294967295
  - Description: Random seed for reproducible prompt selection

- **num_prompts** (INT)
  - Default: 1
  - Minimum: 1
  - Maximum: 10
  - Step: 1
  - Description: Number of prompts to select from the file

### Optional Parameters
- **prefix** (STRING)
  - Default: "" (empty string)
  - Description: Text to add before each selected prompt
  - Example: Adding "masterpiece, " as prefix would make "masterpiece, [prompt]"

- **suffix** (STRING)
  - Default: "" (empty string)
  - Description: Text to add after each selected prompt
  - Example: Adding ", high quality" as suffix would make "[prompt], high quality"

## Output
- Returns a STRING type containing the selected prompts
- Multiple prompts are joined with commas
- Each prompt includes any specified prefix and suffix
- Format: "[prefix]prompt1[suffix], [prefix]prompt2[suffix], ..."

## Differences from V1
1. **Multiple Prompt Selection**
   - Can select multiple prompts in a single operation
   - Useful for batch processing or creating compound prompts

2. **Text Modification**
   - Added prefix/suffix support for easy prompt enhancement
   - Allows consistent styling across all selected prompts

3. **Improved Processing**
   - Automatically removes empty lines from source files
   - Joins multiple prompts with commas for better compatibility

## Usage Tips
- Use num_prompts > 1 to create compound prompts or batch variations
- Add common modifiers as prefix/suffix instead of editing prompt files
- Keep seed constant to maintain consistent selections across runs
- Combine with other prompt nodes for more complex processing
- Useful for:
  - Batch image generation with variations
  - Creating compound prompts from different themes
  - Adding consistent style modifiers to multiple prompts
