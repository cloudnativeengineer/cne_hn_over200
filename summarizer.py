"""cne_hn_over200.summarizer – thin wrapper around OpenAI chat completions."""

from __future__ import annotations

import time
from typing import Any, Dict

import openai
from openai import OpenAI

import logging

from .config import MODEL_NAME

_SYSTEM_PROMPT = "You summarise news stories."
_MAX_TOKENS = 120
_BASE_BACKOFF = 2  # seconds


def summarize_story(
    story: Dict[str, Any],
    client: OpenAI,
    *,
    model: str = MODEL_NAME,
    max_retries: int = 3,
) -> str:
    """
    Return a 2-3 sentence summary of a Hacker News story dict.

    Retries on OpenAI API errors with exponential back-off.
    """
    prompt = (
        "Summarise the following Hacker News story in 2-3 sentences:\n\n"
        f"Title:  {story.get('title')}\n"
        f"URL:    {story.get('url')}\n"
        f"Author: {story.get('by')}\n"
        f"Score:  {story.get('score')}\n"
    )

    for attempt in range(max_retries):
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": _SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.5,
                max_tokens=_MAX_TOKENS,
            )
            return resp.choices[0].message.content.strip()
        except openai.OpenAIError as exc:
            if attempt >= max_retries - 1:
                logging.error("OpenAI API error: %s", exc)
                return "Summary unavailable."
            time.sleep(_BASE_BACKOFF ** (attempt + 1))

    return "Summary unavailable."


__all__ = ["summarize_story"]
