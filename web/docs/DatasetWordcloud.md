# Dataset Wordcloud Node

## Overview
The Dataset Wordcloud node generates visual word cloud representations from prompt datasets stored in text files. It creates an image where the size of each word corresponds to its frequency in the text, using customizable color palettes and dimensions.

## Input Parameters

### text_file
- **Type**: Dropdown selection
- **Description**: Select a text file from the `prompts/` directory to generate the word cloud from
- **Format**: The file should contain text data, with each line typically representing a prompt or caption
- **Note**: Only `.txt` files from the prompts directory are shown in the dropdown

### width
- **Type**: Integer
- **Default**: 800
- **Range**: 64 to 4096
- **Description**: The width of the generated word cloud image in pixels
- **Usage**: Adjust this value to control the horizontal size of the output image

### height
- **Type**: Integer
- **Default**: 400
- **Range**: 64 to 4096
- **Description**: The height of the generated word cloud image in pixels
- **Usage**: Adjust this value to control the vertical size of the output image

### color_palette
- **Type**: Dropdown selection
- **Options**:
  - `kandinsky`: Blues, greens, oranges, and yellows
  - `warm`: Reds, oranges, and yellows
  - `cool`: Blues, greens, and grays
  - `monochrome`: Grayscale from white to dark gray
  - `vibrant`: Bright primary and secondary colors
- **Description**: Determines the color scheme used for the words in the cloud
- **Usage**: Select different palettes to match your desired aesthetic

### background_color
- **Type**: String
- **Default**: "white"
- **Description**: The background color of the word cloud
- **Format**: Can be any valid color name (e.g., "white", "black", "transparent") or hex code (e.g., "#FFFFFF")

## Output

### IMAGE
- **Type**: Tensor (B,H,W,C format)
- **Description**: A word cloud visualization where:
  - Word sizes reflect their frequency in the text
  - Colors are drawn from the selected palette
  - Image dimensions match the specified width and height
- **Usage**: Can be connected to any node that accepts image input

## Example Usage
1. Add the Dataset Wordcloud node to your workflow
2. Select a prompt file from your collection (e.g., "cyberpunk-prompts.txt")
3. Adjust the width and height to your desired dimensions
4. Choose a color palette that matches your theme
5. Set a background color that complements the palette
6. Connect the output to an image preview or processing node

## Notes
- Words appearing more frequently in the text will appear larger in the visualization
- The node automatically handles text processing and word frequency calculation
- Temporary files are cleaned up after generation
- The visualization maintains aspect ratio while fitting within specified dimensions
