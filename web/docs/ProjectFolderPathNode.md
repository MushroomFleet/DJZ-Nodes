# Project Folder Path Generator

This node generates a folder path based on specified components: root, project name, and subfolder.

## Parameters

### Required

- **root**: The base directory for the path (defaults to "output")
- **project_name**: The name of the project folder (defaults to "MyProject")
- **subfolder**: A subfolder within the project (defaults to "images")

### Optional

- **separator**: The path separator to use
  - "auto" (uses system default)
  - "forward_slash" (/)
  - "backslash" (\)

## Output

- **STRING**: The generated folder path

## Example Output

With default settings:
```
output/MyProject/images
```

## Notes

- The node sanitizes inputs to ensure they're safe for use in file paths
- All spaces in inputs are converted to underscores
- The output is a normalized path according to the system's standards
