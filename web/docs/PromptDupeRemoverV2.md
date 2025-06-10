# Prompt Duplicate Remover V2

A ComfyUI custom node that intelligently removes duplicate words from your prompts while preserving specified terms and maintaining text structure.

## Description

The Prompt Duplicate Remover V2 is an advanced text processing node that removes duplicate words from your prompts while offering fine control over case sensitivity and the ability to preserve specific terms. It's particularly useful for cleaning up and optimizing prompts that may contain unintended word repetitions.

## Parameters

### 1. Text (Required)
- Type: String (Multiline)
- The input text/prompt that you want to process and remove duplicates from
- Preserves punctuation and spacing in the original text

### 2. Preserve Original Case (Required)
- Type: Boolean
- Default: True
- When enabled, maintains the original capitalization of words in the output
- When disabled, converts all non-whitelisted words to lowercase

### 3. Whitelist (Optional)
- Type: String (Multiline)
- Default: Empty string
- A comma-separated list of terms that should be allowed to repeat in the text
- Supports both single words and multi-word phrases
- For multi-word phrases, enclose them in quotes (e.g., "red hair", "blue eyes")

## Features

- **Intelligent Word Processing**: Maintains text structure while removing duplicate words
- **Case-Sensitive Options**: Flexibility to preserve or normalize text case
- **Whitelist Support**: Allows specific terms to repeat even when duplicate removal is active
- **Multi-word Phrase Protection**: Preserves specified multi-word phrases as single units
- **Punctuation Preservation**: Maintains original punctuation and spacing

## Usage Examples

### Basic Usage
```
Input Text:
A beautiful beautiful girl with blue eyes and blue hair

Result:
A beautiful girl with blue eyes and hair
```

### Using Whitelist
```
Input Text:
A beautiful beautiful girl with blue eyes and blue hair

Whitelist:
blue, "beautiful girl"

Result:
A beautiful girl with blue eyes and blue hair
```

### Case Preservation
```
Input Text:
The Blue BLUE blue Bird flies

With Preserve Case = True:
The Blue Bird flies

With Preserve Case = False:
the blue bird flies
```

## Tips
1. Use the whitelist for important repeating terms in your style or subject matter
2. Enclose multi-word phrases in quotes in the whitelist to keep them together
3. The node preserves spacing and punctuation, making it safe for complex prompts
4. Case-sensitivity can be toggled based on your specific needs

## Output
- Returns a single string with duplicates removed according to the specified parameters
- Maintains the original text structure and formatting while removing unnecessary repetitions
