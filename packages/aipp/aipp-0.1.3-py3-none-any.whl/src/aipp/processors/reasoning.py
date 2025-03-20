from typing import Dict, Any, Optional, List, Tuple

from .base import SimpleProcessor
from ..builder import TextProcessor


def create_step_by_step_processor(detailed: bool = False) -> TextProcessor:
    """Create a processor that adds step-by-step instructions."""

    def transform(content: str, context: Optional[Dict[str, Any]] = None) -> str:
        prefix = "Please break down your response into clear, sequential steps."
        if detailed:
            prefix = "Please provide a detailed, step-by-step explanation with thorough reasoning at each step."

        if context is not None:
            context['has_step_by_step'] = True
            context['step_by_step_detailed'] = detailed

        return f"{prefix}\n{content}"

    return SimpleProcessor(transform, name="step_by_step")


def create_chain_of_thought_processor() -> TextProcessor:
    """Create a processor that requests chain-of-thought reasoning."""

    def transform(content: str, context: Optional[Dict[str, Any]] = None) -> str:
        instruction = "Please think through this step by step, showing your reasoning before providing the final answer."

        if context is not None:
            context['has_chain_of_thought'] = True

        return f"{instruction}\n{content}"

    return SimpleProcessor(transform, name="chain_of_thought")


def create_few_shot_processor(examples: List[Tuple[str, str]]) -> TextProcessor:
    """Create a processor that adds few-shot examples to the prompt."""

    def transform(content: str, context: Optional[Dict[str, Any]] = None) -> str:
        examples_text = "\n\nExamples:\n"

        for i, (input_text, output_text) in enumerate(examples, 1):
            examples_text += f"\nExample {i}:\nInput: {input_text}\nOutput: {output_text}\n"

        if context is not None:
            context['has_few_shot'] = True
            context['few_shot_count'] = len(examples)

        return f"{content}{examples_text}"

    return SimpleProcessor(transform, name="few_shot_examples")
