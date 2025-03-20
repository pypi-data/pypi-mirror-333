from typing import Dict, Any, Optional, Callable

from ..builder import TextProcessor


class SimpleProcessor(TextProcessor):
    """A simple implementation of TextProcessor."""

    def __init__(self, transform_func: Callable[[str, Optional[Dict[str, Any]]], str], name: Optional[str] = None):
        self.transform_func = transform_func
        self.name = name or getattr(transform_func, "__name__", "transform")

    def process(self, content: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Apply the transform function to the content."""
        return self.transform_func(content, context)

    def __str__(self) -> str:
        return f"<{self.name} Processor>"
