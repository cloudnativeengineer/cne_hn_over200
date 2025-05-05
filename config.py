"""cne_hn_over200.config – package-wide constants."""

from __future__ import annotations

import os

MODEL_NAME: str = os.getenv("AWS_HN_DAILY_MODEL", "gpt-4.1-nano")
DEFAULT_WIDTH: int = int(os.getenv("AWS_HN_DAILY_WIDTH", "80"))

__all__ = ["MODEL_NAME", "DEFAULT_WIDTH"]
