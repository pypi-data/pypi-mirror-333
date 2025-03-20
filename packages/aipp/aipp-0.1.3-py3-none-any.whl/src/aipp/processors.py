import json
from typing import Dict, Any, Optional, Union

from .builder import TextProcessor


class SimpleProcessor(TextProcessor):
    """A simple implementation of TextProcessor."""

    def __init__(self, transform_func, name=None):
        self.transform_func = transform_func
        self.name = name or getattr(transform_func, "__name__", "transform")

    def process(self, content: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Apply the transform function to the content."""
        return self.transform_func(content, context)

    def __str__(self) -> str:
        return f"<{self.name} Processor>"


def create_step_by_step_processor(detailed: bool = False) -> TextProcessor:
    """Create a processor that adds step-by-step instructions.

    Args:
        detailed: If True, adds more detailed instructions.

    Returns:
        A TextProcessor that transforms the content.
    """

    def transform(content: str, context: Optional[Dict[str, Any]] = None) -> str:
        prefix = "Please break down your response into clear, sequential steps."
        if detailed:
            prefix = "Please provide a detailed, step-by-step explanation with thorough reasoning at each step."

        if context is not None:
            context['has_step_by_step'] = True
            context['step_by_step_detailed'] = detailed

        return f"{prefix}\n{content}"

    return SimpleProcessor(transform, name="step_by_step")


# Create additional processor factories for other extensions


# Variable formatting processor
def create_variable_processor(variables: Dict[str, Any]) -> TextProcessor:
    """Create a processor that handles variable substitution in prompt text.

    Args:
        variables: Dictionary of variable names and values for substitution.

    Returns:
        A TextProcessor that replaces {variable} placeholders in the content.
    """

    def transform(content: str, context: Optional[Dict[str, Any]] = None) -> str:
        if context is not None:
            context['variables'] = variables

        try:
            return content.format(**variables)
        except KeyError as e:
            raise ValueError(f"Missing variable in template: {e}")

    return SimpleProcessor(transform, name="variable_substitution")


# JSON formatting processor
def create_json_processor(data: Union[Dict, list], pretty: bool = True) -> TextProcessor:
    """Create a processor that appends JSON data to the prompt.

    Args:
        data: Dictionary or list to be formatted as JSON.
        pretty: If True, formats JSON with indentation for readability.

    Returns:
        A TextProcessor that adds formatted JSON to the content.
    """

    def transform(content: str, context: Optional[Dict[str, Any]] = None) -> str:
        indent = 2 if pretty else None
        json_str = json.dumps(data, indent=indent)

        if context is not None:
            context['has_json_data'] = True

        return f"{content}\n\nJSON Data:\n```json\n{json_str}\n```"

    return SimpleProcessor(transform, name="json_formatter")


# Binary data processor
def create_binary_processor(values: list, format_type: str = "binary") -> TextProcessor:
    """Create a processor that formats binary/hex/octal data.

    Args:
        values: List of integers to format.
        format_type: Type of formatting - "binary", "hex", or "octal".

    Returns:
        A TextProcessor that adds formatted binary data to the content.
    """

    def transform(content: str, context: Optional[Dict[str, Any]] = None) -> str:
        if format_type == "binary":
            formatted = [f"{v:08b}" for v in values]
            prefix = "0b"
        elif format_type == "hex":
            formatted = [f"{v:02x}" for v in values]
            prefix = "0x"
        elif format_type == "octal":
            formatted = [f"{v:03o}" for v in values]
            prefix = "0o"
        else:
            raise ValueError(f"Unsupported format type: {format_type}")

        data_str = ", ".join(f"{prefix}{f}" for f in formatted)

        if context is not None:
            context['binary_format'] = format_type

        return f"{content}\n\n{format_type.capitalize()} Data: {data_str}"

    return SimpleProcessor(transform, name="binary_formatter")


# Few-shot examples processor
def create_few_shot_processor(examples: list) -> TextProcessor:
    """Create a processor that adds few-shot examples to the prompt.

    Args:
        examples: List of input/output example pairs.

    Returns:
        A TextProcessor that adds few-shot examples to the content.
    """

    def transform(content: str, context: Optional[Dict[str, Any]] = None) -> str:
        examples_text = "\n\nExamples:\n"

        for i, (input_text, output_text) in enumerate(examples, 1):
            examples_text += f"\nExample {i}:\nInput: {input_text}\nOutput: {output_text}\n"

        if context is not None:
            context['has_few_shot'] = True
            context['few_shot_count'] = len(examples)

        return f"{content}{examples_text}"

    return SimpleProcessor(transform, name="few_shot_examples")


# Temperature/creativity control processor
def create_creativity_processor(temperature: float) -> TextProcessor:
    """Create a processor that adds temperature/creativity instructions.

    Args:
        temperature: Value from 0.0 (deterministic) to 1.0 (creative).

    Returns:
        A TextProcessor that adds creativity instructions to the content.
    """

    def transform(content: str, context: Optional[Dict[str, Any]] = None) -> str:
        if temperature < 0.3:
            instruction = "Please provide a precise, factual response with minimal creativity."
        elif temperature < 0.7:
            instruction = "Please balance creativity with accuracy in your response."
        else:
            instruction = "Please provide a creative, diverse response that explores multiple possibilities."

        if context is not None:
            context['temperature'] = temperature

        return f"{instruction}\n{content}"

    return SimpleProcessor(transform, name="creativity_control")


# XML/structured output processor
def create_structured_output_processor(schema: Dict[str, Any]) -> TextProcessor:
    """Create a processor that requests output in a specific structured format.

    Args:
        schema: Dictionary describing the expected output structure.

    Returns:
        A TextProcessor that adds structured output instructions.
    """

    def transform(content: str, context: Optional[Dict[str, Any]] = None) -> str:
        schema_str = json.dumps(schema, indent=2)
        instruction = f"""
Please format your response as structured data according to this schema:
```json
{schema_str}
```
Your response should be valid XML or JSON that matches this structure.
"""
        if context is not None:
            context['has_structured_output'] = True
            context['output_schema'] = schema

        return f"{content}\n\n{instruction}"

    return SimpleProcessor(transform, name="structured_output")


# Chain of thought processor
def create_chain_of_thought_processor() -> TextProcessor:
    """Create a processor that requests chain-of-thought reasoning.

    Returns:
        A TextProcessor that adds chain-of-thought instructions.
    """

    def transform(content: str, context: Optional[Dict[str, Any]] = None) -> str:
        instruction = "Please think through this step by step, showing your reasoning before providing the final answer."

        if context is not None:
            context['has_chain_of_thought'] = True

        return f"{instruction}\n{content}"

    return SimpleProcessor(transform, name="chain_of_thought")


# Role or persona processor
def create_role_processor(role: str, details: Optional[str] = None) -> TextProcessor:
    """Create a processor that assigns a specific role or persona.

    Args:
        role: The role/persona to assume (e.g., "expert programmer").
        details: Optional details about the role.

    Returns:
        A TextProcessor that adds role instructions.
    """

    def transform(content: str, context: Optional[Dict[str, Any]] = None) -> str:
        instruction = f"Please respond as {role}."
        if details:
            instruction += f" {details}"

        if context is not None:
            context['role'] = role

        return f"{instruction}\n{content}"

    return SimpleProcessor(transform, name="role_assignment")
