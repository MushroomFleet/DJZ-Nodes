# Prompt Swap

The Prompt Swap node is a utility for replacing specific words or phrases in prompt text with alternative text. It supports both single words and multi-word phrases, with special handling for quoted strings.

## Parameters

### Required Parameters

1. **text** (STRING, multiline)
   - The input text/prompt where you want to perform word swaps
   - Supports multiple lines of text
   - This is the source text where the replacements will occur

2. **target_words** (STRING)
   - A comma-separated list of words or phrases to be replaced
   - Default value: `man, woman, "no humans"`
   - Supports quoted phrases for multi-word targets
   - Case-insensitive matching
   - Each word/phrase should be separated by commas

3. **exchange_words** (STRING)
   - A comma-separated list of replacement words or phrases
   - Default value: `woman, man, "many monsters"`
   - Must have the same number of items as target_words
   - Words/phrases will replace their corresponding targets in order
   - Supports quoted phrases for multi-word replacements

## Usage

1. Connect your prompt source to the "text" input
2. Specify the words you want to replace in "target_words"
3. Provide their replacements in "exchange_words"
4. The node will process the text and output the modified version

## Example

Input text:
```
A beautiful scene with a man and woman, but no humans in the background
```

target_words: `man, woman, "no humans"`
exchange_words: `woman, man, "many monsters"`

Output:
```
A beautiful scene with a woman and man, but many monsters in the background
```

## Notes

- The swapping process is case-insensitive
- Multi-word phrases should be enclosed in quotes (e.g., `"no humans"`)
- Longer phrases are processed first to avoid partial matches
- Word boundaries are respected for single words (e.g., "man" won't match "manual")
- Phrase boundaries are not enforced for quoted multi-word phrases
- The number of target words must match the number of exchange words
- Whitespace around words and phrases is automatically trimmed
