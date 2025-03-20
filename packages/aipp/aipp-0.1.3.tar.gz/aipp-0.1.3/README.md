# Generative AI Prompt extensions

A flexible, composable library for constructing and transforming LLM prompts with a fluent interface.

## Installation

```
pip install aipp
```

### Development Setup

```
uv venv
source .venv/bin/activate
uv sync --group e
pytest -s
code .
```

## Overview

Generative AI Prompt extensions helps you build complex prompts with:

- Chain-of-thought reasoning instructions
- Variable substitution
- Few-shot examples
- Role/persona assignment
- JSON data formatting
- Structured output requirements
- And more...

## Quick Start

```python
from aipp import PromptBuilder

# Simple example
prompt = (
    PromptBuilder()
    .configure_variables(model="GPT-4", task="summarization")
    .step_by_step(detailed=True)
    .prompt("Create a summary using {model} for {task} task.")
)

print(str(prompt))
```

Output:
```
Please provide a detailed, step-by-step explanation with thorough reasoning at each step.
Create a summary using GPT-4 for summarization task.
```

## Features

### Variable Substitution

```python
prompt = (
    PromptBuilder()
    .configure_variables(model="GPT-4", task="summarization", length="short")
    .prompt("Create a {length} summary using {model} for {task} task.")
)
```

### JSON Data

```python
data = {
    "user": {"name": "Alice", "preferences": ["science", "history"]},
    "settings": {"language": "en", "format": "paragraph"}
}

prompt = (
    PromptBuilder()
    .prompt("Generate content based on user preferences")
    .with_json(data)
)
```

### Few-Shot Examples

```python
examples = [
    ("Summarize: The quick brown fox jumps over the lazy dog.",
     "A fox quickly jumps over a dog that is resting."),
    ("Summarize: The study showed significant results with p<0.05.",
     "The research findings were statistically significant.")
]

prompt = (
    PromptBuilder()
    .prompt("Summarize the following text")
    .with_few_shot(examples)
)
```

### Structured Output

```python
schema = {
    "type": "object",
    "properties": {
        "summary": {"type": "string"},
        "length": {"type": "integer"},
        "topics": {"type": "array", "items": {"type": "string"}}
    }
}

prompt = (
    PromptBuilder()
    .prompt("Analyze the following text")
    .structured_output(schema)
)
```

### Chain of Thought

```python
prompt = (
    PromptBuilder()
    .prompt("Solve this math problem")
    .chain_of_thought()
)
```

### Role/Persona Assignment

```python
prompt = (
    PromptBuilder()
    .prompt("Explain quantum computing")
    .as_role("quantum physicist", "with expertise in quantum information theory")
)
```

### Lambda Processors

Use inline lambda functions for custom transformations:

```python
prompt = (
    PromptBuilder()
    .prompt("Standard prompt text")
    .process(lambda content, _: f"IMPORTANT: {content}")
    .process(lambda content, _: f"{content}\n\nPlease be thorough.")
)
```

## Combining Processors

Processors can be combined in any order:

```python
prompt = (
    PromptBuilder()
    .prompt("Summarize the following article")
    .chain_of_thought()
    .with_few_shot(examples)
    .structured_output(schema)
    .as_role("professional writer")
    .process(lambda content, _: f"{content}\n\nLimit response to 3 paragraphs.")
)
```

## Advanced Usage

### Custom Processors

Create your own processors:

```python
from aipp.processors.base import SimpleProcessor


def create_custom_processor(options):
    def transform(content, context=None):
        # Transform the content based on options
        return f"Custom prefix: {content}"

    return SimpleProcessor(transform, name="custom_processor")


prompt = (
    PromptBuilder()
    .prompt("Base content")
    .add_processor(create_custom_processor({"option": "value"}))
)
```

### Processing Context

Processors can share context:

```python
def create_metadata_processor():
    def transform(content, context=None):
        if context is not None:
            context['processed_at'] = "2023-01-01"
        return content
    
    return SimpleProcessor(transform, name="metadata")

prompt = PromptBuilder()
prompt.add_processor(create_metadata_processor())
prompt.prompt("Content")
print(prompt.metadata)  # Contains processed_at
```

## Contributing

We welcome contributions to improve Generative AI Prompt extensions! See [CONTRIBUTING.md](https://github.com/descoped/aipp/blob/master/CONTRIBUTING.md) for detailed information on:

- Architecture overview
- Core concepts
- How to extend the library
- Design patterns used
- Best practices
- Testing guidelines

Please submit issues and pull requests following our guidelines.

## License

MIT
