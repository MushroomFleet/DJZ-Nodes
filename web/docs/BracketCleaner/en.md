# Bracket Cleaner Node README

## Overview
The **Bracket Cleaner** node is designed to remove text enclosed within parentheses, along with the parentheses themselves, from a given input text. It processes the text by splitting it into paragraphs (using blank lines as separators) and then cleaning each paragraph individually.

## Functionality
- **Paragraph Splitting:** The input text is divided into paragraphs based on blank lines.
- **Bracket Removal:** For each paragraph, the node uses a regular expression to identify and remove any content within parentheses `(` and `)`.
- **Logging:** The node logs both the original and the cleaned text for debugging and verification purposes.
- **Output:** Returns the cleaned text as a single string, preserving paragraph breaks.

## Parameters

### text (STRING, required)
- **Description:** The multiline string input that may contain unwanted bracketed information.
- **Usage:** Supply any text that you want to clean. The node will look through each paragraph and remove any text that appears within parentheses.

## Example

**Input:**
```
(Studio lights up, and I, Juan Carlos Gómez, appear on screen)

Juan Carlos Gómez: Buenas noches, amigos. Welcome to our broadcast.

(Cut to a graphic reading "URGENTE: Nuevo descubrimiento científico")

Juan Carlos Gómez: Tonight, we have groundbreaking news.
```

**Output:**
```
Juan Carlos Gómez: Buenas noches, amigos. Welcome to our broadcast.

Juan Carlos Gómez: Tonight, we have groundbreaking news.
```

## How to Use
1. **Connect the Node:** Integrate the Bracket Cleaner node into your node pipeline.
2. **Provide Input:** Attach a string source to the `text` parameter containing the content you wish to process.
3. **Execute:** Run the node to output the cleaned text. Check logs if needed for details on the cleaning process.

## Category
Custom-Nodes
