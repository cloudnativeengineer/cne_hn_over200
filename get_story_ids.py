"""cne_hn_over200.get_story_ids – thin wrapper around the HN Firebase API."""

from __future__ import annotations

import requests
from typing import Any, Dict, List

API_ROOT = "https://hacker-news.firebaseio.com/v0"
_TIMEOUT = 10  # seconds


def _fetch_json(url: str) -> Any:
    resp = requests.get(url, timeout=_TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def get_top_stories(
    *,
    min_score: int = 200,
    limit: int = 30,
) -> List[Dict[str, Any]]:
    """
    Return *limit* Hacker News stories whose score exceeds *min_score*.

    The API returns story IDs in ranking order; we walk the list until we have
    enough items or run out of IDs.
    """
    ids: List[int] = _fetch_json(f"{API_ROOT}/topstories.json")
    stories: List[Dict[str, Any]] = []

    for story_id in ids:
        if len(stories) >= limit:
            break

        data = _fetch_json(f"{API_ROOT}/item/{story_id}.json")
        if not data or data.get("score", 0) <= min_score:
            continue

        stories.append(
            {
                "title": data.get("title"),
                "score": data.get("score"),
                "url": data.get("url"),
                "by": data.get("by"),
                "id": data.get("id"),
            }
        )

    return stories


__all__ = ["get_top_stories"]
