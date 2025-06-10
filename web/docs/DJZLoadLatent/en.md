# DJZ Load Latent Node

The DJZ Load Latent node is designed to load previously saved latent tensors directly from ComfyUI's output directory. This node is particularly useful when you want to reuse latent representations from previous generations or load pre-computed latents into your workflow.

## Parameters

### Required Parameters

- **latent_file**: A dropdown menu that displays all available .latent files found in the ComfyUI output directory and its subdirectories. The files are sorted alphabetically for easy navigation.

## Functionality

The node performs the following operations:

1. Scans the ComfyUI output directory recursively for .latent files
2. Loads the selected latent file using safetensors
3. Applies the appropriate scaling factor based on the latent format version:
   - For version 0 format: multiplier = 1.0
   - For other formats: multiplier = 1.0 / 0.18215
4. Returns the properly formatted latent tensor for use in your workflow

## Error Handling

The node includes several safety features:

- If no latent files are found, an empty option is provided in the dropdown
- If an invalid file is selected, appropriate error messages are displayed
- If there's an error loading the latent, it returns a zero tensor (1, 4, 8, 8) to prevent workflow crashes
- File validation is performed to ensure the selected file exists before attempting to load it

## Output

The node outputs a LATENT type that can be used with other nodes that accept latent inputs in your ComfyUI workflow.

## Use Cases

- Loading previously generated latents for further processing
- Reusing latent representations across different workflows
- Experimenting with saved latent spaces
- Creating workflows that build upon previously generated results
