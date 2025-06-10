# Captions To Prompt List Node

The Captions To Prompt List node is designed to combine multiple caption text files from a directory into a single consolidated list. This node is particularly useful when working with datasets that contain multiple caption files and you need to merge them into a single prompt list.

## Parameters

### Required Inputs

1. **directory_path** (STRING)
   - The path to the directory containing caption text files
   - Default value: "/path/to/dataset"
   - Should point to a directory containing .txt files with captions

### Optional Inputs

1. **reload** (BOOLEAN)
   - Controls when the node should reload and reprocess the files
   - Default value: False
   - Two modes:
     - "if file changed" (True): Reloads when file contents change
     - "if value changed" (False): Reloads only when the directory path changes

## Functionality

The node performs the following operations:
1. Walks through the specified directory and its subdirectories
2. Reads all .txt files found in the directory structure
3. Combines all captions from these files into a single list
4. Generates an output filename based on the input directory name

### File Processing Rules
- Only processes files with .txt extension
- Ignores .png files silently
- Logs when it ignores other file types
- Handles UTF-8 encoded text files
- Processes each caption file line by line

## Outputs

The node returns two values:

1. **combined_captions** (STRING)
   - All captions combined into a single string
   - Each caption is separated by a newline
   - Maintains the original order of captions within each file

2. **output_filename** (STRING)
   - Generated filename for the combined captions
   - Created by taking the last directory name from the path and adding .txt extension
   - Example: If path is "/data/my_dataset", output filename will be "my_dataset.txt"

## Important Notes

1. Error Handling:
   - The node will attempt to process each .txt file independently
   - If an error occurs while processing a specific file, it will:
     - Print an error message with the file path and error details
     - Continue processing remaining files
   - UTF-8 encoding is required for text files

2. Reload Behavior:
   - When reload is False: Only reprocesses when directory path changes
   - When reload is True: Uses MD5 hashing to detect changes in file contents
   - Hash calculation includes both filenames and file contents
   - Ensures efficient processing by only reloading when necessary

3. The node is categorized under "custom/text" in the ComfyUI interface
