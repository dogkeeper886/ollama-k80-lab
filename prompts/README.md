# Prompts

This directory contains LLM prompt templates and example contexts for workflow automation in the Ollama K80 Lab environment.

## Structure

```
prompts/
├── templates/          # Reusable prompt templates
│   └── professional-communication-assistant.md
├── examples/           # Context examples for testing prompts
│   └── deadline-extension-request.md
└── responses/          # Model responses organized by example
    └── deadline-extension-request/
        ├── qwen2.5-vl.md
        ├── gemma-3-12b.md
        ├── phi4-14b.md
        └── deepseek-r1-32b.md
```

## Usage

### Templates
Prompt templates are structured prompts designed for specific use cases. They include:
- Clear instructions and guidelines
- Configurable parameters (marked with placeholders)
- Multiple tone/style variations where applicable

### Examples
Example contexts provide sample inputs to test and demonstrate prompt templates:
- Real-world scenarios
- Edge cases
- Different complexity levels

### Responses
Model responses are organized by example scenario, with each model's output saved separately:
- Compare different models on the same prompt/context
- Track model performance over time
- Analyze response quality and consistency
- Use kebab-case filenames matching model names

## Integration

These prompts integrate with:
- **Dify workflows** - For automated LLM-powered QA tasks
- **VS Code Continue plugin** - For development assistance
- **Ollama API** - Running on K80-optimized containers

## Adding New Prompts

1. Create template in `templates/` with descriptive kebab-case naming
2. Add corresponding examples in `examples/`
3. Test with your target LLM models
4. Save model responses in `responses/example-name/model-name.md`
5. Update this README if needed

## Testing Workflow

1. Use template + example to generate prompts
2. Run against multiple models (Qwen2.5-VL, Gemma 3, Phi-4, DeepSeek-R1, etc.)
3. Save each model's response in the appropriate response folder
4. Compare outputs for quality, consistency, and usefulness

## Related Components

- `/dify/` - Workflow automation configurations
- `/ollama37/` - Docker runtime for LLM execution
- `CLAUDE.md` - Project development guidelines