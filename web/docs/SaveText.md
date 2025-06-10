# Save Text

The Save Text node is a utility for saving text content to files. It provides flexible options for file handling, including appending to existing files or creating new ones, with support for different output directories.

## Parameters

### Required Parameters

1. **root_dir** (COMBO)
   - Selection of valid ComfyUI directories where the file can be saved
   - Options include:
     - Output directory
     - Input directory
     - Temp directory

2. **file** (STRING)
   - The name of the file to save
   - Default value: "file.txt"
   - Can include subdirectories (e.g., "subfolder/file.txt")

3. **append** (COMBO)
   - Determines how the file should be handled
   - Options:
     - "append": Add text to the end of an existing file
     - "overwrite": Replace existing file content
     - "new only": Only create new files, error if file exists

4. **insert** (BOOLEAN)
   - Only active when "append" mode is selected
   - Controls whether to add a new line before appended text
   - Options:
     - "new line" (True): Insert newline before appending
     - "none" (False): Append directly without newline
   - Default: True

5. **text** (STRING, multiline)
   - The text content to save
   - Supports multiple lines
   - Required input connection from another node

## Outputs

The node returns two values:
1. **text**: The text that was written (same as input)
2. **file_path**: The full path to the saved file

## Usage

1. Select the appropriate output directory from root_dir
2. Specify the target filename
3. Choose the file handling mode (append/overwrite/new only)
4. If appending, decide whether to insert a new line
5. Connect the text input to your text source
6. The node will save the text and return both the text and the file path

## Examples

### Creating a New File
- root_dir: "output"
- file: "prompt.txt"
- append: "new only"
- text: "A beautiful landscape with mountains"

Result: Creates new file "prompt.txt" in the output directory

### Appending to Existing File
- root_dir: "output"
- file: "prompt.txt"
- append: "append"
- insert: True (new line)
- text: "Additional prompt text"

Result: Adds text on a new line to existing prompt.txt

## Notes

- Parent directories in the file path are automatically created if they don't exist
- Files are saved with UTF-8 encoding
- The node will raise an exception if:
  - "new only" mode is selected and the file already exists
  - The directory is not writable
  - Any other file operation errors occur
- The insert option is automatically disabled when not in append mode
