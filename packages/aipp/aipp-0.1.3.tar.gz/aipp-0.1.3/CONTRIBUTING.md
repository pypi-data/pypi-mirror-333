# Contributing to Generative AI Prompt extensions

This guide explains core concepts and patterns used in Generative AI Prompt extensions to help developers extend its functionality.

## Architecture Overview

Generative AI Prompt extensions follows a composition-based architecture with these key components:

1. **PromptBuilder** - The main builder class with fluent interface
2. **TextProcessor** - A protocol defining the processor interface
3. **Processor Implementations** - Various implementations of TextProcessor
4. **Factory Functions** - Functions that create processor instances

## Core Concepts

### The TextProcessor Protocol

The foundation of the library is the `TextProcessor` protocol:

```python
@runtime_checkable
class TextProcessor(Protocol):
    def process(self, content: str, context: Optional[Dict[str, Any]] = None) -> str:
        ...
```

This protocol defines a processor interface that takes content and an optional context, then returns transformed content.

### SimpleProcessor Implementation

The standard implementation of the TextProcessor protocol:

```python
class SimpleProcessor(TextProcessor):
    def __init__(self, transform_func, name=None):
        self.transform_func = transform_func
        self.name = name or getattr(transform_func, "__name__", "transform")

    def process(self, content: str, context: Optional[Dict[str, Any]] = None) -> str:
        return self.transform_func(content, context)
```

This class delegates processing to a transform function, making it easy to create new processors.

### Factory Pattern

Each processor is created through a factory function:

```python
def create_xxx_processor(...) -> TextProcessor:
    def transform(content: str, context: Optional[Dict[str, Any]] = None) -> str:
        # Transform the content
        return transformed_content
    
    return SimpleProcessor(transform, name="xxx")
```

### Fluent Interface

The `PromptBuilder` class uses method chaining to provide a fluent interface:

```python
def chain_of_thought(self) -> 'PromptBuilder':
    from .processors.reasoning import create_chain_of_thought_processor
    return self.add_processor(create_chain_of_thought_processor())
```

## Extending the Library

### 1. Creating New Processors

To add a new processor:

1. Choose the appropriate module (or create a new one)
2. Create a factory function that returns a TextProcessor
3. Add re-export in `processors/__init__.py`

Example:

```python
# processors/formatting.py
def create_highlighting_processor(color: str = "yellow") -> TextProcessor:
    def transform(content: str, context: Optional[Dict[str, Any]] = None) -> str:
        if context is not None:
            context['highlight_color'] = color
        
        return f"Please highlight important points in {color}.\n{content}"
    
    return SimpleProcessor(transform, name="highlighting")
```

### 2. Adding Builder Extensions

To add a convenience method to PromptBuilder:

```python
# builder.py
def highlight(self, color: str = "yellow") -> 'PromptBuilder':
    """Add highlighting instructions to the prompt."""
    from .processors.formatting import create_highlighting_processor
    return self.add_processor(create_highlighting_processor(color))
```

### 3. Creating Advanced Processors

For more complex processors, create a dedicated class:

```python
class AdvancedProcessor(TextProcessor):
    def __init__(self, config):
        self.config = config
    
    def process(self, content: str, context: Optional[Dict[str, Any]] = None) -> str:
        # Advanced processing logic
        return transformed_content
```

## Design Patterns Used

### 1. Builder Pattern

The `PromptBuilder` class builds a complex prompt object through a sequence of steps.

### 2. Strategy Pattern

Each `TextProcessor` is a strategy for transforming content, allowing algorithms to be selected at runtime.

### 3. Factory Method Pattern

Factory functions create processor instances, hiding their implementation details.

### 4. Chain of Responsibility

Processors are applied in sequence, with each one receiving the output of the previous processor.

### 5. Command Pattern

Each processor encapsulates a transformation as an object.

## Best Practices

1. **Immutability**: Processors should not modify their inputs
2. **Idempotence**: Repeated application of a processor should be safe
3. **Isolation**: Processors should be independent, with minimal dependencies
4. **Context Use**: Use context for metadata, not for passing critical data between processors
5. **Error Handling**: Gracefully handle edge cases

## Testing

When adding new processors, include tests that verify:
- Basic functionality
- Edge cases
- Interaction with other processors
- Context usage

Example test:

```python
def test_highlighting_processor():
    prompt = (
        PromptBuilder()
        .prompt("Process this text")
        .highlight("green")
    )
    
    result = str(prompt)
    assert "highlight important points in green" in result
    assert "Process this text" in result
```

## Documentation

When adding new functionality:
1. Add clear docstrings to all public functions and methods
2. Update README.md with examples
3. Add type annotations
