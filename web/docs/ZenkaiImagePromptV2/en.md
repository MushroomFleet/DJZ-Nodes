# Zenkai Image Prompt V2

## Overview
The Zenkai Image Prompt V2 node provides functionality for loading images and their associated text prompts from predefined folders. This node is designed to streamline workflows that require pairing visual references with text prompts, making it ideal for text-to-image generation pipelines, controlled image sampling, and prompt engineering experiments.

## Features
- Load image-text pairs from organized folders
- Select images sequentially or randomly based on a seed value
- Filter prompts using a blacklist feature
- Return both images and combined prompt text for further processing
- Support for multiple image selection in a single node operation

## Setup

### Folder Structure
The node uses a specific folder structure to organize image-text pairs:

```
ComfyUI/custom_nodes/DJZ-Nodes/imageprompts/
├── category1/
│   ├── image1.png
│   ├── image1.txt
│   ├── image2.jpg
│   ├── image2.txt
│   └── ...
├── category2/
│   ├── image1.jpg
│   ├── image1.txt
│   └── ...
└── ...
```

- The node automatically creates the `imageprompts` folder if it doesn't exist
- Each subfolder under `imageprompts` represents a different category of image-text pairs
- If no subfolders exist, a `default` folder is created automatically

### Image-Text Pairs
For each image file, create a corresponding text file with the same base name:
- Image file: `example.png`
- Text file: `example.txt`

The text file should contain the prompt text associated with the image.

**Supported Image Formats:**
- JPEG (.jpg, .jpeg)
- PNG (.png)

## Parameters

### Required Parameters

#### `prompt_folder`
A dropdown menu that lists all available subfolders within the `imageprompts` directory. Each subfolder contains a collection of image-text pairs. Select the folder containing the image-text pairs you want to use.

#### `seed`
- **Type:** Integer
- **Default:** 0
- **Range:** 0 to 4294967295 (0xFFFFFFFF)

The seed value determines which images are selected. In sequential mode, it determines the starting index. In random mode, it sets the random number generator seed for reproducible results.

#### `mode`
- **Options:** "sequential", "random"
- **Default:** "sequential"

Determines how images are selected from the folder:
- **sequential:** Images are selected in order (sorted by filename), starting from the index determined by the seed value
- **random:** Images are selected randomly, but consistently for the same seed value

#### `num_images`
- **Type:** Integer
- **Default:** 1
- **Range:** 1 to 10
- **Step:** 1

The number of image-text pairs to select and return as a batch.

### Optional Parameters

#### `blacklist`
- **Type:** String
- **Default:** Empty string
- **Format:** Comma-separated list of terms or quoted phrases

Filters out prompts containing any of the specified terms. Terms can be:
- Single words: `cat, dog, table`
- Quoted phrases: `"no humans", "low quality"`

Any image-text pair whose text contains any blacklisted term will be excluded from selection.

## Return Values

The node returns two outputs:

1. **IMAGE:** A batched tensor containing the selected images
2. **STRING:** The combined text from all selected prompts, joined with " | " separators

## Usage Examples

### Basic Usage
1. Create a folder under `imageprompts/` (e.g., `imageprompts/landscapes/`)
2. Add image files and corresponding text files with the same names
3. In the ComfyUI workflow, select "landscapes" from the `prompt_folder` dropdown
4. Set the seed, mode, and number of images as needed
5. Connect the output to other nodes in your workflow

### Sequential Image Selection
- Set `mode` to "sequential"
- Set `seed` to 0 and `num_images` to 3
  - This will select the first 3 images from the folder (sorted by filename)
- Changing the seed to 5 will start selection from the 6th image (wrapping around if needed)

### Random Image Selection
- Set `mode` to "random"
- Set `seed` to any value and `num_images` to desired count
  - This will randomly select the specified number of images
- Using the same seed will always select the same images, providing reproducible results

### Filtering Prompts
- Set `blacklist` to "cat, dog, \"low quality\""
  - This will exclude any prompts containing "cat", "dog", or the phrase "low quality"

### Batch Processing
1. Set `num_images` to 4
2. Connect the IMAGE output to a model that supports batch processing
3. The output will contain 4 images processed as a batch

## Tips and Best Practices

### Naming Conventions
- Use consistent naming patterns for easy sorting (e.g., `image01.png`, `image02.png`)
- The node uses natural sorting, so `image2.png` comes before `image10.png`

### Prompt Writing
- Keep prompts in text files concise and focused
- Use consistent formatting across prompts for better results when combining

### Performance Considerations
- Large image libraries might slow down loading time
- Organize images into logical categories using separate subfolders for better management

### Handling Image Sizes
- The node automatically handles images of different sizes by padding to match the largest dimension
- For best results, use images with consistent dimensions within a folder

### Debugging
- If no images appear, check that:
  1. Your image-text pairs exist in the selected folder
  2. The text files have the exact same base names as the image files
  3. Your blacklist isn't excluding all available prompts

## Limitations
- Maximum 10 images can be selected in a single operation
- Image padding to match sizes may affect composition for significantly different image dimensions
- Only supports RGB images (automatically converts other formats to RGB)
