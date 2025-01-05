# PromptInject Node

A custom node for ComfyUI that allows you to inject text before a specific target phrase in your prompts. This is particularly useful for adding descriptive elements or modifiers to specific parts of your prompt without manually editing the entire text.

## Parameters

### Required Inputs

1. **text** (STRING, multiline)
   - The main prompt text where you want to inject additional content
   - This is your base prompt that contains the target phrase

2. **target** (STRING)
   - The phrase where you want to inject text before
   - Default: "the scene is captured"
   - This should be an exact match to a phrase in your text

3. **injection** (STRING)
   - The text you want to inject before the target phrase
   - Default: "Screeching tires."
   - Will be automatically wrapped with appropriate spacing

## How It Works

The node performs the following operations:
1. Cleans up the target and injection text by removing extra whitespace
2. Finds the target phrase in your text (case-insensitive)
3. Injects your text before the target phrase with proper spacing
4. Handles punctuation appropriately (adds correct spacing if injection ends with punctuation)

## Example Usage

### Input:
```
text: "A beautiful landscape where the scene is captured in stunning detail"
target: "the scene is captured"
injection: "during sunset"
```

### Output:
```
"A beautiful landscape where during sunset the scene is captured in stunning detail"
```

## Tips for Use

1. Make sure your target phrase exists exactly in your text
2. The injection is case-insensitive, so it will work regardless of capitalization
3. Punctuation is handled automatically - if your injection ends with '.', '!', or '?', spacing will be adjusted accordingly
4. You can use this node multiple times in sequence to inject different text at different points in your prompt

## Technical Details

- Category: Custom-Nodes
- Return Type: STRING
- The node maintains proper spacing and punctuation in the final output
- Logging is enabled for debugging purposes, showing original and modified text
