# Zenkai-Prompt V3

A powerful prompt generation and interpolation node for ComfyUI that allows you to create dynamic prompts from text files with various interpolation methods.

## Overview

ZenkaiPromptV3 is designed to generate prompts by reading from text files in the `prompts` directory. It can create complex prompts using different interpolation modes and division methods, allowing for creative mixing of prompt content.

## Parameters

### Required Parameters

- **text_file**: Select a text file from the `prompts` directory to use as the source for prompt generation.
- **seed**: Integer value (0 to 4294967295) that determines the randomization of prompt selection and interpolation.
- **interpolation_mode**: Choose how the prompt sections will be combined:
  - `none`: Uses a single prompt without any interpolation
  - `lines`: Interpolates different lines from the same text file
  - `directory`: Interpolates lines from different text files in the prompts directory
- **division_preset**: Determines how the prompt will be divided for interpolation:
  - `words`: Treats each word individually
  - `halves`: Splits the prompt into 2 parts
  - `thirds`: Splits the prompt into 3 parts
  - `quarters`: Splits the prompt into 4 parts
  - `fifths`: Splits the prompt into 5 parts

### Optional Parameters

- **prefix**: Text to add before the generated prompt
- **suffix**: Text to add after the generated prompt

## How It Works

1. The node selects a base prompt from the chosen text file using the provided seed.
2. If interpolation is enabled (mode is not "none"):
   - The base prompt is split according to the division preset
   - Depending on the interpolation mode:
     - `lines`: Additional sections are taken from other lines in the same file
     - `directory`: Additional sections are taken from random files in the prompts directory
3. The sections are combined with any provided prefix/suffix to create the final prompt

## Usage Examples

### Basic Prompt Generation
- Set `interpolation_mode` to "none" to simply get a random prompt from your text file
- Use the `seed` parameter to get consistent results

### Creative Prompt Mixing
1. Choose "lines" interpolation to mix different prompts from the same theme/file
2. Use "directory" interpolation to create cross-theme prompts
3. Experiment with different division presets to control how much mixing occurs

### Tips
- Use consistent prompt structures in your text files for best results with interpolation
- The `seed` parameter can be used to reproduce specific prompt combinations
- Prefix and suffix can be used to add consistent elements to all generated prompts

## Output

The node outputs a single STRING containing the generated prompt, which can be connected to other nodes that accept prompt inputs in your ComfyUI workflow.
