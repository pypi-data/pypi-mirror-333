from typing import Dict, Any, Optional

from .base import SimpleProcessor
from ..builder import TextProcessor


def create_variable_processor(variables: Dict[str, Any]) -> TextProcessor:
    """Create a processor that handles variable substitution in prompt text."""

    def transform(content: str, context: Optional[Dict[str, Any]] = None) -> str:
        if context is not None:
            context['variables'] = variables

        try:
            return content.format(**variables)
        except KeyError as e:
            raise ValueError(f"Missing variable in template: {e}")

    return SimpleProcessor(transform, name="variable_substitution")


def create_creativity_processor(temperature: float) -> TextProcessor:
    """Create a processor that adds temperature/creativity instructions."""

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
