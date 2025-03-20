from typing import Dict, List, Optional, Any, Protocol, runtime_checkable, TypeVar, Union, Callable

T = TypeVar('T')


@runtime_checkable
class TextProcessor(Protocol):
    """Protocol for text processors that transform prompt text."""

    def process(self, content: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Transform the content and return the result."""
        ...


class PromptBuilder:
    """A builder for constructing prompts with a fluent interface."""

    def __init__(self, text: str = ""):
        self.text = text
        self.processors: List[TextProcessor] = []
        self.metadata: Dict[str, Any] = {}
        self._processed_text: Optional[str] = None

    def prompt(self, text: str) -> 'PromptBuilder':
        """Set the core prompt statement text."""
        self.text = text
        self._processed_text = None
        return self

    def add_processor(self, processor: TextProcessor) -> 'PromptBuilder':
        """Add a processor to the chain."""
        self.processors.append(processor)
        self._processed_text = None
        return self

    def process(self, transform_func: Callable[[str, Optional[Dict[str, Any]]], str]) -> 'PromptBuilder':
        """Add an inline processor using a lambda or function.

        Args:
            transform_func: A function that takes content and context and returns modified content

        Returns:
            The builder instance for method chaining
        """
        from .processors.base import SimpleProcessor
        return self.add_processor(SimpleProcessor(transform_func))

    def _apply_processors(self) -> None:
        """Apply all processors in sequence."""
        current = self.text
        context = self.metadata.copy()

        for processor in self.processors:
            current = processor.process(current, context)

        self._processed_text = current

    def __str__(self) -> str:
        """Return the built prompt as a string, applying processors if needed."""
        if self._processed_text is None:
            self._apply_processors()
        return self._processed_text

    # Extension methods to simplify common processor usage

    def step_by_step(self, detailed: bool = False) -> 'PromptBuilder':
        """Add step-by-step instructions to the prompt."""
        from .processors.reasoning import create_step_by_step_processor
        return self.add_processor(create_step_by_step_processor(detailed))

    def configure_variables(self, *args, **kwargs) -> 'PromptBuilder':
        """Add variable substitution to the prompt."""
        from .processors.formatting import create_variable_processor

        if args and isinstance(args[0], dict):
            variables = args[0]
        else:
            variables = kwargs

        return self.add_processor(create_variable_processor(variables))

    def with_json(self, data: Union[Dict, list], pretty: bool = True) -> 'PromptBuilder':
        """Add JSON data to the prompt."""
        from .processors.structured import create_json_processor
        return self.add_processor(create_json_processor(data, pretty))

    def with_few_shot(self, examples: list) -> 'PromptBuilder':
        """Add few-shot examples to the prompt."""
        from .processors.reasoning import create_few_shot_processor
        return self.add_processor(create_few_shot_processor(examples))

    def chain_of_thought(self) -> 'PromptBuilder':
        """Add chain-of-thought reasoning instructions to the prompt."""
        from .processors.reasoning import create_chain_of_thought_processor
        return self.add_processor(create_chain_of_thought_processor())

    def structured_output(self, schema: Dict[str, Any]) -> 'PromptBuilder':
        """Request structured output in a specific format."""
        from .processors.structured import create_structured_output_processor
        return self.add_processor(create_structured_output_processor(schema))

    def as_role(self, role: str, details: Optional[str] = None) -> 'PromptBuilder':
        """Assign a specific role or persona for the response."""
        from .processors.role import create_role_processor
        return self.add_processor(create_role_processor(role, details))

    def creativity(self, temperature: float) -> 'PromptBuilder':
        """Set the creativity level for the response."""
        from .processors.formatting import create_creativity_processor
        return self.add_processor(create_creativity_processor(temperature))
