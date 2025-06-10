# ZenkaiWildcard V2 Node

The ZenkaiWildcard V2 node is an enhanced version of the ZenkaiWildcard node for ComfyUI that enables dynamic text replacement in prompts using a wildcard system. This version adds support for nested wildcards and provides more detailed debugging information.

## Parameters

- **prompt** (required): The input text prompt containing wildcard tokens. Each wildcard should be marked with the specified wildcard symbol (default: $$) followed by the name of a text file in the wildcards folder (without the .txt extension).

- **seed** (required): An integer value that determines the randomization of wildcard selections. Using the same seed will produce the same random selections.
  - Default: 0
  - Minimum: 0
  - Maximum: 4294967295 (0xFFFFFFFF)

- **wildcard_symbol** (required): The symbol used to identify wildcards in the prompt.
  - Default: "$$"

- **recursive_depth** (required): Maximum depth for processing nested wildcards.
  - Default: 5
  - Minimum: 1
  - Maximum: 10
  - Step: 1

## How It Works

1. The node looks for patterns in your prompt that match the format: `$$filename`
2. For each match, it looks for a corresponding `filename.txt` in the `wildcards` folder
3. If the file exists, it randomly selects one line from the file and replaces the wildcard with that content
4. If the selected content contains more wildcards, it processes them recursively up to the specified recursive_depth
5. The process continues until either:
   - No more wildcards are found
   - The maximum recursive depth is reached
   - No changes occur in an iteration

## Nested Wildcards Example

If you have these wildcard files:

`animal.txt`:
```
$$color dog
$$color cat
$$color bird
```

`color.txt`:
```
red
blue
green
```

And your prompt is:
```
a $$animal in the garden
```

The node might output:
```
a blue cat in the garden
```

## Advanced Features

1. **Nested Wildcard Processing**: Unlike V1, this version can handle wildcards within wildcards, allowing for more complex and dynamic prompt generation.

2. **Depth Control**: The recursive_depth parameter prevents infinite loops and allows you to control how deep the nested wildcard processing should go.

3. **Improved Error Handling**: More robust error handling and detailed logging for debugging purposes.

4. **Iteration-based Processing**: Uses an iterative approach to ensure all wildcards are processed properly, even in complex nested scenarios.

## Notes

- Wildcard files should be placed in the `wildcards` folder within the node's directory
- Each line in a wildcard file represents one possible replacement option
- Empty lines in wildcard files are ignored
- The node provides detailed debug logging to help track wildcard replacements and any issues
- The same seed will always produce the same random selections, allowing for reproducible results

## Error Handling

- If a referenced wildcard file doesn't exist, the original wildcard text is preserved
- If a wildcard file exists but is empty, the original wildcard text is preserved
- If the maximum recursive depth is reached, further nested wildcards will not be processed
- The node includes comprehensive logging functionality that helps track:
  - File access attempts
  - Wildcard replacements
  - Recursive processing depth
  - Iteration results
