"""cne_hn_over200.table_utils – render story tables (rich → tabulate → ASCII)."""

from __future__ import annotations

import shutil

# ---------- terminal + optional deps -------------------------------------------------

_TERM_WIDTH = shutil.get_terminal_size(fallback=(80, 30)).columns

try:
    from rich.console import Console
    from rich.table import Table

    _console: Console | None = Console(width=_TERM_WIDTH)
except ImportError:  # pragma: no cover
    _console = None

try:
    from tabulate import tabulate  # type: ignore
except ImportError:  # pragma: no cover
    tabulate = None

# ---------- ASCII fallback -----------------------------------------------------------


def _ascii_table(headers: list[str], rows: list[list[str]]) -> str:
    """Minimal, multiline-aware ASCII table (no external deps)."""
    all_rows = [headers] + rows
    col_widths = [
        max(len(line) for row in all_rows for line in str(row[i]).split("\n"))
        for i in range(len(headers))
    ]

    def row_sep(fill: str = "-") -> str:
        return "+" + "+".join(fill * (w + 2) for w in col_widths) + "+"

    def render(row: list[str]) -> str:
        cells = [str(c).split("\n") for c in row]
        max_lines = max(len(c) for c in cells)
        for cell in cells:
            cell.extend([""] * (max_lines - len(cell)))
        return "\n".join(
            "| "
            + " | ".join(
                cells[i][line].ljust(col_widths[i]) for i in range(len(headers))
            )
            + " |"
            for line in range(max_lines)
        )

    parts: list[str] = [row_sep(), render(headers), row_sep("=")]
    for r in rows:
        parts.append(render(r))
        parts.append(row_sep())
    return "\n".join(parts)


# ---------- public helper ------------------------------------------------------------


def print_table(headers: list[str], rows: list[list[str]]) -> None:
    """Pretty-print *rows* with decreasing fidelity: rich → tabulate → ASCII."""
    # ----- rich -----
    if _console:
        table = Table(show_header=True, header_style="bold blue", box=None)
        for idx, head in enumerate(headers):
            justify = "right" if idx < 2 else "left"
            style = ("cyan" if idx == 0 else "green") if idx < 2 else ""
            table.add_column(head, justify=justify, no_wrap=idx < 2, style=style)
        for r in rows:
            table.add_row(*r)
        _console.print(table)
        return

    # ----- tabulate -----
    if tabulate:
        print(
            tabulate(
                rows,
                headers=headers,
                tablefmt="fancy_grid",
                stralign="left",
                numalign="right",
            )
        )
        return

    # ----- ASCII fallback -----
    print(_ascii_table(headers, rows))


__all__ = ["print_table"]
