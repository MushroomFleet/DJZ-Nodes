# Think Seeker Node

A ComfyUI custom node that parses text to separate thinking sections from response sections. This node is particularly useful for processing AI-generated text that contains explicit thinking and response segments.

## Overview

The Think Seeker node analyzes input text and splits it into two parts:
1. Thinking text (content within `<think>` tags)
2. Response text (remaining content outside the tags)

This separation is useful for:
- Analyzing AI reasoning processes
- Debugging AI responses
- Separating internal processing from final outputs
- Processing structured AI communications

## Parameters

### Required Input

1. **text** (STRING)
   - Multiline text input that may contain thinking sections
   - Supports any text content with or without thinking tags
   - Thinking sections should be enclosed in `<think>` tags
   - Example format:
     ```
     <think>Analyzing user request...</think>
     Here is the response.
     <think>Processing additional info...</think>
     Final conclusion.
     ```

## Outputs

The node returns two strings:

1. **thinking_text** (STRING)
   - Contains all content found within `<think>` tags
   - Multiple thinking sections are joined with newlines
   - Returns empty string if no thinking tags are found
   - Preserves original formatting within the tags

2. **response_text** (STRING)
   - Contains all text outside of thinking tags
   - Removes the thinking sections completely
   - Preserves original formatting of non-thinking content
   - Automatically strips leading/trailing whitespace

## Technical Details

### Tag Processing
- Uses regular expressions for pattern matching
- Supports multiline thinking sections
- Case-sensitive tag matching (`<think>` must be lowercase)
- Handles nested content within thinking tags

### Logging
- Implements detailed logging for debugging
- Logs original text, extracted thinking sections, and response content
- Uses Python's logging module with INFO level

## Usage Examples

### Basic Usage
Input:
```
<think>Analyzing input parameters</think>
The result is 42.
<think>Verifying calculation</think>
Calculation confirmed.
```

Output:
- thinking_text: "Analyzing input parameters\nVerifying calculation"
- response_text: "The result is 42.\nCalculation confirmed."

### No Thinking Tags
Input:
```
This is a simple response without any thinking sections.
```

Output:
- thinking_text: "" (empty string)
- response_text: "This is a simple response without any thinking sections."

## Integration Tips

1. **Text Processing Workflows**
   - Use before text generation to analyze AI thinking patterns
   - Chain with other text processing nodes for complex workflows
   - Combine with prompt nodes for structured output analysis

2. **Debugging**
   - Monitor AI reasoning process through thinking sections
   - Track decision-making patterns in AI responses
   - Identify processing steps in complex operations

3. **Content Organization**
   - Separate internal processing notes from final output
   - Structure AI communications more clearly
   - Filter different types of content for different purposes

## Error Handling

- Gracefully handles missing or malformed tags
- Returns empty string for thinking_text when no tags are found
- Preserves original text structure in response_text
- Implements logging for troubleshooting

## Performance Considerations

- Efficient regex-based parsing
- Minimal memory footprint
- Suitable for processing large text blocks
- Real-time processing capability
