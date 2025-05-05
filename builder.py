import shutil
import textwrap
from .config import DEFAULT_WIDTH
from .summarizer import summarize_story


def build_rows(stories: list[dict], client) -> list[list[str]]:
    """Wrap title and generated summary so each column fits the terminal width."""
    term_width = shutil.get_terminal_size(fallback=(DEFAULT_WIDTH, 30)).columns

    title_w = min(35, term_width // 3)
    summary_w = max(
        term_width
        - (
            len(str(len(stories)))                # index column
            + max(len("Pts"), max(len(str(s["score"])) for s in stories))  # score col
            + title_w
            + 10                                  # spacing / borders
        ),
        20,
    )

    rows: list[list[str]] = []
    for idx, story in enumerate(stories, 1):
        title_wrapped = textwrap.fill(story["title"], width=title_w)
        summary_raw = summarize_story(story, client)
        summary_wrapped = textwrap.fill(summary_raw, width=summary_w)
        rows.append(
            [str(idx), str(story["score"]), title_wrapped, summary_wrapped]
        )
    return rows
