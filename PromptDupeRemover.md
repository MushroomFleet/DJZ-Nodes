# Prompt Duplicate Remover

A ComfyUI custom node that removes duplicate words from prompt text while preserving punctuation and optionally maintaining the original case of words.

## Description

The Prompt Duplicate Remover node is designed to clean up prompts by removing redundant words that might appear multiple times. This can be particularly useful when:
- Combining multiple prompts together
- Working with long, complex prompts
- Cleaning up AI-generated or concatenated prompt strings

## Parameters

### Required Inputs

1. **text** (STRING, multiline)
   - The input prompt text that needs to be processed
   - Can contain multiple lines
   - Preserves punctuation and spacing

2. **preserve_case** (BOOLEAN)
   - Default: True
   - When enabled, maintains the original capitalization of words
   - When disabled, converts all words to lowercase in the output

## How It Works

The node processes text through the following steps:
1. Splits the input text into individual words while preserving punctuation
2. Identifies duplicate words (case-insensitive comparison)
3. Removes subsequent occurrences of duplicate words
4. Maintains the first occurrence of each word
5. Preserves all punctuation and spacing
6. Rejoins the cleaned text while maintaining word order

## Example Usage

### Input Text:
```
A beautiful sunset, beautiful clouds, beautiful sky, beautiful landscape
```

### Output with preserve_case = True:
```
A beautiful sunset, clouds, sky, landscape
```

Note: The node removes the duplicate instances of "beautiful" while maintaining the original case and punctuation.

## Technical Details

- The node performs case-insensitive comparison to identify duplicates
- Punctuation marks are preserved in their original positions
- The first occurrence of each word is kept, subsequent duplicates are removed
- Logging is implemented to track:
  - Original text
  - Number of words removed
  - Final cleaned text

## Integration

This node can be particularly useful when:
- Processing large prompt collections
- Cleaning up concatenated prompts
- Removing unintended duplicates from workflow outputs
- Optimizing prompt length while maintaining meaning
