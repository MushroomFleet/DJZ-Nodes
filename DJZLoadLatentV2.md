# DJZ Load Latent V2 Node

The DJZ Load Latent V2 node is an enhanced version of the original DJZ Load Latent node. It loads latent tensors from ComfyUI's output directory with additional features for seed-based selection and a numbered reference list of available latents.

## Parameters

### Required Parameters

- **latent_index**: A dropdown menu showing a numbered list of all available .latent files in the ComfyUI output directory and its subdirectories. The files are sorted alphabetically and displayed with index numbers for reference (e.g., "[0] filename.latent"). This list serves as a reference to see what files are available.

- **seed**: An integer value that determines which latent file to load. The seed value is used to select a position in the latent file list using modulo operation (seed % number_of_files). This allows for deterministic selection of latent files based on the seed value.
  - Default: 0
  - Min: 0
  - Max: 18446744073709551615 (0xffffffffffffffff)

## Functionality

The node performs the following operations:

1. Scans the ComfyUI output directory recursively for .latent files
2. Creates a numbered list of all available latent files for reference
3. Uses the provided seed value to deterministically select a file from the list
4. Loads the selected latent file using safetensors
5. Applies the appropriate scaling factor based on the latent format version:
   - For version 0 format: multiplier = 1.0
   - For other formats: multiplier = 1.0 / 0.18215
6. Returns both the formatted latent tensor and the filename of the loaded file

## Outputs

The node provides two outputs:

1. **samples**: The LATENT tensor that can be used with other nodes in your ComfyUI workflow
2. **current_file**: A STRING containing the filename of the currently loaded latent file

## Error Handling

The node includes several safety features:

- If no latent files are found, displays "No latents found" in the dropdown
- Validates that the seed value is an integer
- If there's an error loading the latent, returns a zero tensor (1, 4, 8, 8) to prevent workflow crashes
- Prints informative messages about which file is being loaded (position and filename)

## Use Cases

- Deterministic loading of latent files using seed values
- Creating workflows that cycle through available latents systematically
- Easy reference of available latent files with numbered list
- Tracking which file is currently being used via the filename output
- Batch processing of multiple latent files using seed iteration
