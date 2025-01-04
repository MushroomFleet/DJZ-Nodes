# StringWeights

This custom node allows you to apply numerical weights to text strings. It's particularly useful for AI image generation workflows where you need to adjust the emphasis of different prompt components. The node wraps the input text in parentheses and appends a weight value with one decimal place precision.

## Input Parameters

- **text** (Required)
  - Type: STRING
  - Multiline: Yes
  - The input text to be weighted
  - Can be a single word, phrase, or multiple lines of text

- **weight** (Required)
  - Type: FLOAT
  - Default: 1.0
  - Range: 0.0 to 10.0
  - Step: 0.1
  - The weight value to apply to the text
  - Higher values increase emphasis, lower values decrease emphasis

## Output

1. **STRING**
   - The weighted text in the format: (text:weight)
   - Weight is formatted to one decimal place
   - Example: If text is "blue sky" and weight is 1.2, output will be "(blue sky:1.2)"

## Usage Examples

1. **Basic Weighting**
   - Input text: "blue sky"
   - Weight: 1.0
   - Output: "(blue sky:1.0)"

2. **Increased Emphasis**
   - Input text: "dramatic lighting"
   - Weight: 1.5
   - Output: "(dramatic lighting:1.5)"

3. **Reduced Emphasis**
   - Input text: "subtle texture"
   - Weight: 0.7
   - Output: "(subtle texture:0.7)"

4. **Multiple Lines**
   - Input text:
     ```
     masterpiece
     high quality
     ```
   - Weight: 1.2
   - Output: "(masterpiece\nhigh quality:1.2)"

## Notes

- The node automatically formats weights to one decimal place for consistency
- Weights are clamped between 0.0 and 10.0
- The node is part of the "Custom-Nodes" category
- Changes to either text or weight will trigger node updates
- The node includes logging functionality for debugging purposes
- Commonly used in prompt engineering for fine-tuning AI image generation
