# Prompt Cleaner

The Prompt Cleaner node is a utility for cleaning up prompt text by removing specified words. This can be useful for refining prompts by eliminating unwanted terms or standardizing prompt content.

## Parameters

### Required Parameters

1. **text** (STRING, multiline)
   - The input text/prompt that you want to clean
   - Supports multiple lines of text
   - This is the source text from which specified words will be removed

2. **words_to_remove** (STRING)
   - A comma-separated list of words that should be removed from the input text
   - Default value: "man, woman, world"
   - Case-insensitive matching (e.g., "Man" will match "man")
   - Each word should be separated by commas
   - Leading and trailing whitespace around words is automatically trimmed

## Usage

1. Connect your prompt source to the "text" input
2. Specify the words you want to remove in the "words_to_remove" field
3. The node will process the text and output a cleaned version with the specified words removed

## Example

Input text:
```
A beautiful world with a man and woman walking
```

words_to_remove: "man, woman, world"

Output:
```
A beautiful with a and walking
```

## Notes

- The cleaning process is case-insensitive
- Punctuation is preserved in the output
- Words are matched as whole words only (e.g., "man" won't match "manual")
- Multiple consecutive spaces that may result from word removal are automatically condensed to single spaces
