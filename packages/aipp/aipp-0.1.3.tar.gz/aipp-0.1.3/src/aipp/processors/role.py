from typing import Dict, Any, Optional

from .base import SimpleProcessor
from ..builder import TextProcessor


def create_role_processor(role: str, details: Optional[str] = None) -> TextProcessor:
    """Create a processor that assigns a specific role or persona."""

    def transform(content: str, context: Optional[Dict[str, Any]] = None) -> str:
        instruction = f"Please respond as {role}."
        if details:
            instruction += f" {details}"

        if context is not None:
            context['role'] = role

        return f"{instruction}\n{content}"

    return SimpleProcessor(transform, name="role_assignment")
