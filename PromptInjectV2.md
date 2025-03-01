# Prompt Inject V2

This node allows you to inject text before or after a target phrase in a prompt.

## Inputs

- **text**: The original prompt text
- **target**: The phrase to target for injection
- **injection**: The text to inject before or after the target
- **inject_after**: Boolean option to place the injection after the target instead of before it

## Output

- A modified string with the injection placed before or after the target phrase.

## Usage

This node is useful for:
- Adding context or details to specific parts of a prompt
- Inserting descriptive elements before or after key phrases
- Modifying existing prompts without rewriting them entirely

### Examples

**With inject_after = False (default behavior):**
- Original text: "The photo shows a landscape where the scene is captured at sunset."
- Target: "the scene is captured"
- Injection: "with dramatic lighting"
- Result: "The photo shows a landscape where with dramatic lighting the scene is captured at sunset."

**With inject_after = True (new behavior):**
- Original text: "The photo shows a landscape where the scene is captured at sunset."
- Target: "the scene is captured"
- Injection: "with dramatic lighting"
- Result: "The photo shows a landscape where the scene is captured with dramatic lighting at sunset."

This is an enhanced version of the original PromptInject node, adding the ability to choose where the injection is placed.
