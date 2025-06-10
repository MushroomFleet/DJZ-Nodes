# ZenkaiPrompt Node

## Overview
ZenkaiPrompt is a ComfyUI node that randomly selects and returns a line from a specified text file in the prompts directory. It's designed to provide variety and inspiration by selecting from curated collections of prompts.

## Parameters

### Required Parameters
- **text_file** (COMBO)
  - Options: List of available .txt files in the prompts directory, including:
    - Various themed prompt collections (e.g., cybersociety, blacksun, cogvideo)
    - Caption files (e.g., assassinKahb-captions.txt, dronecam-captions.txt)
    - Style-specific prompts (e.g., LTXV-dialogue-closeups.txt, Mochi-Photo-256.txt)
  - Description: The source text file to select a prompt from

- **seed** (INT)
  - Default: 0
  - Minimum: 0
  - Maximum: 4294967295
  - Description: Random seed for reproducible prompt selection. Using the same seed with the same text file will always return the same prompt.

## Output
- Returns a STRING type containing a single line selected from the chosen text file
- The selected line can be used as input for other nodes that accept text/prompts

## Available Prompt Collections
The node comes with various prompt collections organized by themes:

1. **Traditional Narratives**
   - 01-trad-ahab.txt through 09-trad-secondSpear.txt
   - Contains narrative-focused prompts

2. **Sci-Fi and Fantasy**
   - cybersociety (v0-v6)
   - blacksun (v0-v4)
   - cogvideo-scifi.txt, cogvideo-fantasy.txt

3. **Character and Scene Descriptions**
   - LTXV series (dialogue-closeups, emotional-moments, etc.)
   - Various character-specific collections (assassinKahb, darkExecutioner, etc.)

4. **Style-Specific**
   - Mochi-Photo series
   - hologram-style-flux
   - NeonMutation-tagged

5. **Environmental and Scene Settings**
   - paradistro series
   - dronecam-captions
   - HYV-Drift series

## Usage Tips
- Use different text files to target specific themes or styles
- Keep the seed value constant to maintain consistent prompt selection across multiple runs
- Combine with other prompt-processing nodes for more complex prompt generation
- Useful for batch processing where you want variety but reproducibility
