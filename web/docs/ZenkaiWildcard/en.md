# ZenkaiWildcard Node

The ZenkaiWildcard node is a custom node for ComfyUI that enables dynamic text replacement in prompts using a wildcard system. It allows you to define placeholder tokens in your prompt that will be randomly replaced with content from corresponding text files.

## Parameters

- **prompt** (required): The input text prompt containing wildcard tokens. Each wildcard should be marked with the specified wildcard symbol (default: $$) followed by the name of a text file in the wildcards folder (without the .txt extension).

- **seed** (required): An integer value that determines the randomization of wildcard selections. Using the same seed will produce the same random selections.
  - Default: 0
  - Minimum: 0
  - Maximum: 4294967295 (0xFFFFFFFF)

- **wildcard_symbol** (required): The symbol used to identify wildcards in the prompt.
  - Default: "$$"

## How It Works

1. The node looks for patterns in your prompt that match the format: `$$filename`
2. For each match, it looks for a corresponding `filename.txt` in the `wildcards` folder
3. If the file exists, it randomly selects one line from the file and replaces the wildcard with that content
4. If the file doesn't exist or is empty, the original wildcard text is left unchanged

## Usage Example

If you have a file named `color.txt` in your wildcards folder containing:
```
red
blue
green
```

And your prompt is:
```
a $$color car driving down the street
```

The node might output:
```
a blue car driving down the street
```

## Notes

- Wildcard files should be placed in the `wildcards` folder within the node's directory
- Each line in a wildcard file represents one possible replacement option
- Empty lines in wildcard files are ignored
- The node will log information about the wildcard replacement process, which can be helpful for debugging
- The same seed will always produce the same random selections, allowing for reproducible results

## Error Handling

- If a referenced wildcard file doesn't exist, the original wildcard text is preserved in the prompt
- If a wildcard file exists but is empty, the original wildcard text is preserved
- The node includes logging functionality that helps track which files it's trying to access and what replacements are being made
