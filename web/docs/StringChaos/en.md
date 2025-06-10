# StringChaos Node

A custom node for ComfyUI that provides various text transformation modes to add creative chaos to your text inputs.

## Description

StringChaos is a versatile text transformation node that can apply different stylistic effects to your input text. It's useful for creating unique text variations for prompts or any text-based workflows in ComfyUI.

## Parameters

- **text** (STRING): The input text to transform
- **mode** (SELECT): The transformation mode to apply
- **seed** (INT): Random seed for deterministic output (0 to 18446744073709551615)
- **intensity** (FLOAT): Controls the strength of certain effects (0.0 to 1.0, default: 0.5)

## Transformation Modes

### 1. L33T
Converts text to "leet speak" by replacing letters with numbers and symbols.
```
Example:
Input: "Hello World"
Output: "H3110 W0r1d"
```

### 2. aLtErNaTiNg
Alternates between uppercase and lowercase letters.
```
Example:
Input: "Hello World"
Output: "HeLlO wOrLd"
```

### 3. SCRAMBLED
Scrambles the middle letters of each word while keeping the first and last letters intact.
```
Example:
Input: "Hello World"
Output: "Hlelo Wlrod"
```

### 4. EMOJI
Adds relevant emojis after certain keywords based on a predefined mapping.
```
Example:
Input: "Hello world I love coding"
Output: "Hello 👋 world 🌍 I love ❤️ coding"
```

### 5. ZALGO
Adds combining characters to create a glitch/corrupted text effect. The intensity parameter controls the amount of corruption.
```
Example:
Input: "Hello World"
Output: "H̷̪̓e̸̢̛l̴̘̐l̷͎̒o̶̼͝ W̶̭̄ǫ̷͝r̶̙̈́l̵͙̔d̶̰̕"
```

### 6. REDACTED
Randomly replaces characters with █ blocks. The intensity parameter controls how many characters are redacted.
```
Example:
Input: "Hello World"
Output: "He█lo █or█d"
```

## Usage Tips

1. The **seed** parameter ensures consistent results when using the same input and settings. Change it to get different variations.

2. The **intensity** parameter affects:
   - ZALGO: Controls how many corrupting characters are added
   - REDACTED: Controls what percentage of characters get redacted

3. Some modes (L33T, aLtErNaTiNg, SCRAMBLED) ignore the intensity parameter as they don't need it.

4. The EMOJI mode has a predefined set of word-to-emoji mappings and will only add emojis for recognized words.

## Output

The node outputs a single STRING containing the transformed text, which can be connected to other text-processing nodes in your ComfyUI workflow.
