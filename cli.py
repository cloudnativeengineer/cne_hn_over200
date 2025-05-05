"""cne_hn_over200.cli – command-line interface for summarising HN stories."""

from __future__ import annotations

import argparse
import os
import sys

from openai import OpenAI

from .builder import build_rows
from .get_story_ids import get_top_stories
from .table_utils import print_table


def main(
    *,
    min_score: int = 200,
    limit: int = 30,
    api_key: str | None = None,
) -> None:
    """Fetch stories, build the table, and print it."""
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        print("OPENAI_API_KEY not set.", file=sys.stderr)
        sys.exit(1)

    client = OpenAI(api_key=key)

    try:
        stories = get_top_stories(min_score=min_score, limit=limit)
    except Exception as exc:
        print(f"Error fetching stories: {exc}", file=sys.stderr)
        sys.exit(1)

    if not stories:
        print("No stories found.", file=sys.stderr)
        return

    rows = build_rows(stories, client)
    print_table(["#", "Pts", "Title", "Summary"], rows)


def cli() -> None:
    """Parse CLI arguments and delegate to ``main``."""
    parser = argparse.ArgumentParser(
        description="Summarise top Hacker News stories."
    )
    parser.add_argument(
        "--min-score",
        type=int,
        default=200,
        help="Minimum story score to include (default: 200)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=30,
        help="Maximum number of stories to fetch (default: 30)",
    )
    parser.add_argument(
        "--api-key",
        type=str,
        help="OpenAI API key (overrides env var OPENAI_API_KEY)",
    )
    args = parser.parse_args()

    main(min_score=args.min_score, limit=args.limit, api_key=args.api_key)


__all__ = ["cli", "main"]

if __name__ == "__main__":  # allows `python cli.py …` for convenience
    cli()
