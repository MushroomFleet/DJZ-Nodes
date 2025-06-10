# Prompt Cleaner Node README

## Overview
The **Prompt Cleaner** node processes input text by removing specified words, helping to sanitize or simplify textual prompts. It is designed to filter out unwanted words while preserving punctuation and the overall structure of the text.

## Functionality
- **Word Removal:** The node receives a list of words (as a comma-separated string) that should be removed from the input text. It performs a case-insensitive match against each word.
- **Text Tokenization:** It splits the input text into individual words and punctuation tokens using regular expressions. This ensures that punctuation is preserved in the final output.
- **Filtering:** Each token in the input text is examined. If a token (in lowercase) matches any of the words in the removal list, it is excluded from the final output.
- **Logging:** The node logs the original text, the words designated for removal, and the cleaned text for verification and debugging purposes.
- **Output:** Returns the cleaned text as a single string, with tokens rejoined and separated by spaces.

## Parameters

### text (STRING, required)
- **Description:** The multiline string input representing the prompt that needs cleaning.
- **Usage:** Provide the full prompt from which you want certain words removed. The node will process the text token by token.

### words_to_remove (STRING, required)
- **Description:** A comma-separated list of words that should be removed from the input text.
- **Default Value:** `"man, woman, world"`
- **Usage:** Specify the words to filter out. The node splits this string by commas, trims white spaces, and converts each word to lowercase for comparisons.

## Example

**Input:**
```
The world is an amazing place.
Man cannot comprehend all its wonders.
```
_With the default words to remove (`"man, woman, world"`), the node processes the text as follows._

**Output:**
```
The is an amazing place. cannot comprehend all its wonders.
```

## How to Use
1. **Integrate the Node:** Add the Prompt Cleaner node into your processing pipeline.
2. **Provide Input:** Connect a text source to the `text` parameter and optionally modify the `words_to_remove` parameter with your custom list.
3. **Execute:** Run the node to produce the cleaned text. Check the logs if you need to verify which words were removed and inspect the output.

## Category
Custom-Nodes
