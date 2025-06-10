# Project File Path Generator

A ComfyUI node that generates organized and sanitized file paths for project management. This node helps create consistent file paths with proper structure and safe characters, making it ideal for organizing outputs in a project-based hierarchy.

## Parameters

### Required Parameters

- **root** (String)
  - Default: "output"
  - The base directory for your project files
  - Example: "output", "projects", "renders"

- **project_name** (String)
  - Default: "MyProject"
  - Name of your project folder
  - Will be sanitized to remove unsafe characters
  - Spaces are converted to underscores

- **subfolder** (String)
  - Default: "images"
  - Name of the subfolder within your project
  - Useful for organizing different types of outputs
  - Example: "images", "videos", "models"

- **filename** (String)
  - Default: "image"
  - Base name for your file
  - File extension should not be included (will be removed if present)
  - Unsafe characters are automatically removed

### Optional Parameters

- **separator** (Dropdown)
  - Options: "auto", "forward_slash", "backslash"
  - Default: "auto"
  - Controls the path separator used:
    * auto: Uses system default (/ for Unix, \ for Windows)
    * forward_slash: Forces forward slashes (/)
    * backslash: Forces backslashes (\)

## Output

- **STRING**
  - A properly formatted and sanitized file path
  - Combines all components with the specified separator
  - Example: "output/MyProject/images/filename" or "output\MyProject\images\filename"

## Path Sanitization

The node automatically sanitizes all path components for safety:

1. Removes unsafe characters:
   - For paths: < > : " | ? *
   - For filenames: < > : " / \ | ? *

2. Special handling:
   - Converts spaces to underscores
   - Removes leading/trailing dots and slashes
   - Strips any file extensions from the filename

## Usage Tips

1. Project Organization:
   ```
   root/
   ├── project_name/
   │   ├── subfolder/
   │   │   └── filename
   ```

2. Common setups:
   - For image outputs:
     * root: "output"
     * project_name: "my_art_project"
     * subfolder: "images"
     * filename: "generated_image"

   - For model outputs:
     * root: "models"
     * project_name: "training_run_1"
     * subfolder: "checkpoints"
     * filename: "model_checkpoint"

3. Path separator selection:
   - Use "auto" for maximum compatibility
   - Use "forward_slash" for web/cross-platform use
   - Use "backslash" for Windows-specific applications

## Technical Details

- The node ensures path safety by:
  * Sanitizing all input components
  * Normalizing path separators
  * Removing potentially harmful characters
  * Converting spaces to underscores for better compatibility

- The IS_CHANGED method ensures the node updates whenever inputs change

- Empty components are automatically filtered out from the path
