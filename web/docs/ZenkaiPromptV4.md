# Zenkai-Prompt V4

An advanced prompt selection node that allows filtering of prompts using a blacklist.

## Parameters

- **text_file**: Select a text file from the prompts directory containing the list of prompts
- **seed**: Random seed for prompt selection
- **num_prompts**: Number of prompts to select (1-10)
- **prefix** (optional): Text to add before each prompt
- **suffix** (optional): Text to add after each prompt
- **blacklist** (optional): Comma-separated list of words or phrases to filter out. Use quotes for multi-word phrases.

## Blacklist Examples

- Single words: `table, cat, dog`
- Phrases with spaces: `"no humans", "blue sky", table`
- Mixed: `cat, "red car", table, "green grass"`

## Notes

- The blacklist is case-insensitive
- If a prompt contains any blacklisted term, it will be excluded from selection
- If all prompts are filtered out by the blacklist, the node will return an error message
- The node maintains compatibility with previous versions' input/output format
- Random selection is performed after filtering, ensuring only valid prompts are chosen

## Example Usage

1. Load a prompt list file
2. Add blacklist terms: `cat, "no humans", table`
3. Set number of desired prompts
4. Node will return random prompts that don't contain any blacklisted terms
