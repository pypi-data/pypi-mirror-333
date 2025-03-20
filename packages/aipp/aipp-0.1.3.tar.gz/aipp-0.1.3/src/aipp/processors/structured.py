import json
from typing import Dict, Any, Optional, Union

from .base import SimpleProcessor
from ..builder import TextProcessor


def create_json_processor(data: Union[Dict, list], pretty: bool = True) -> TextProcessor:
    """Create a processor that appends JSON data to the prompt."""

    def transform(content: str, context: Optional[Dict[str, Any]] = None) -> str:
        indent = 2 if pretty else None
        json_str = json.dumps(data, indent=indent)

        if context is not None:
            context['has_json_data'] = True

        return f"{content}\n\nJSON Data:\n```json\n{json_str}\n```"

    return SimpleProcessor(transform, name="json_formatter")


def create_structured_output_processor(schema: Dict[str, Any]) -> TextProcessor:
    """Create a processor that requests output in a specific structured format."""

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
