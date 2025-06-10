# LoadTextDirectory Node

A ComfyUI custom node that enables loading text content from files within a specified directory. This node is particularly useful for batch processing of text files, allowing sequential, single-file, or random access to text content.

## Parameters

- **mode** (Required)
  - `single_file`: Loads a specific text file based on the index
  - `incremental_file`: Loads files sequentially, cycling back to the beginning when reaching the end
  - `random`: Loads a random text file using the provided seed
  
- **seed** (Required)
  - Default: 0
  - Range: 0 to 18446744073709551615
  - Used for random file selection when mode is set to "random"
  
- **index** (Required)
  - Default: 0
  - Range: 0 to 150000
  - Step: 1
  - Specifies which file to load in "single_file" mode or starting point in "incremental_file" mode
  
- **label** (Required)
  - Default: 'Text Batch 001'
  - A label for the text batch being processed
  
- **path** (Required)
  - Default: '' (empty string)
  - The directory path containing the text files to be loaded
  
- **pattern** (Required)
  - Default: '*'
  - File pattern for matching text files (e.g., '*.txt', 'chapter*.md')

## Supported File Types

- `.txt` files
- `.md` files

## Outputs

The node provides two outputs:
1. **text**: The content of the loaded text file
2. **filename_text**: The name of the loaded file

## Usage Examples

### Single File Mode
Use this mode when you want to load a specific text file by its index:
1. Set `mode` to "single_file"
2. Set `path` to your text files directory
3. Set `index` to select the specific file (0 for first file, 1 for second, etc.)

### Incremental File Mode
Use this mode for sequential processing of text files:
1. Set `mode` to "incremental_file"
2. Set `path` to your text files directory
3. Set `index` to define the starting point
4. Files will be processed sequentially from the starting index

### Random File Mode
Use this mode to randomly select text files:
1. Set `mode` to "random"
2. Set `path` to your text files directory
3. Set `seed` to control random selection (same seed will always select the same file)

## Error Handling

The node includes error handling for common issues:
- Invalid directory paths
- Invalid file indices
- File reading errors

Files are automatically sorted alphabetically within the directory to ensure consistent ordering across different modes.
