# PromptInject Node

The PromptInject node is a custom node for ComfyUI that allows you to inject additional text before a specific target phrase in your prompts. This is particularly useful for adding descriptive elements or modifiers to specific parts of your prompt without manually editing the entire text.

## Parameters

### Required Inputs

1. **text** (STRING, multiline)
   - The main prompt text where you want to inject additional content
   - Can be multiple lines of text
   - This is your base prompt that contains the target phrase

2. **target** (STRING)
   - The phrase where you want to inject text before
   - Default value: "the scene is captured"
   - Should be an exact match to what's in your text
   - Case-insensitive matching

3. **injection** (STRING)
   - The text you want to inject before the target phrase
   - Default value: "Screeching tires."
   - Will be automatically wrapped with spaces
   - If ends with punctuation (., !, ?), will be followed by a single space

## How It Works

1. The node takes your input text and looks for the specified target phrase
2. It automatically adds appropriate spacing around your injection text
3. The injection is placed immediately before the target phrase
4. The result maintains proper spacing and punctuation

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

1. Choose unique target phrases to ensure precise injection
2. Make sure your target phrase exists in the text exactly as written
3. The injection will maintain proper spacing, so you don't need to add extra spaces
4. Punctuation at the end of your injection will be handled automatically

## Technical Details

- The node uses regular expressions for text matching and replacement
- Matching is case-insensitive for better flexibility
- Automatic space handling ensures clean text integration
- Logging is implemented for debugging purposes

## Return Value

The node returns a single STRING containing the modified prompt with the injected text.
