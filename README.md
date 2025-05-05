# cne\_hn\_over200

> **AI‑generated summary — review the code before relying on it in production.**

`cne_hn_over200` is a command‑line tool that surfaces high‑scoring Hacker News stories (default ≥ 200 points), distils each one to a two‑to‑three‑sentence abstract using an OpenAI chat model, and prints the result as a compact table that automatically adapts to the capabilities of your terminal.

---

## How it works

1. **`cli.main()`** orchestrates the workflow.
2. **`get_story_ids.get_top_stories()`** queries the Hacker News Firebase API for stories that meet the score threshold.
3. **`builder.build_rows()`** wraps titles and delegates summarisation to **`summarizer.summarize_story()`**, producing rows ready for display.
4. **`table_utils.print_table()`** renders those rows via **Rich** if installed, falls back to **tabulate**, and finally to a pure‑ASCII implementation.

---

## Module‑by‑module overview

| Module                 | Purpose                                                                                                                         | Key Public Symbols            |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- |
| **`cli.py`**           | Entry‑point & CLI argument parsing; passes control to `main()` and exits.                                                       | `cli`, `main`                 |
| **`builder.py`**       | Calculates per‑column widths from terminal size; formats titles & summaries; returns printable rows.                            | `build_rows`                  |
| **`summarizer.py`**    | Thin wrapper around `openai.ChatCompletion`; builds prompts, applies retry/exponential back‑off, and returns concise summaries. | `summarize_story`             |
| **`get_story_ids.py`** | Talks directly to the Hacker News Firebase REST API; filters stories by score ≥ *min\_score*.                                   | `get_top_stories`             |
| **`table_utils.py`**   | Three‑tier printing helper: Rich → tabulate → pure ASCII.                                                                       | `print_table`                 |
| **`config.py`**        | Centralised constants (`MODEL_NAME`, `DEFAULT_WIDTH`) with environment‑variable overrides.                                      | `MODEL_NAME`, `DEFAULT_WIDTH` |
| **`__init__.py`**      | Defines the package’s public surface for imports.                                                                               | *see file*                    |
| **`__main__.py`**      | Enables `python -m cne_hn_over200` execution by forwarding to the CLI.                                                          | –                             |

---

## Quick start

```bash
git clone https://github.com/cloudnativeengineer/cne_hn_over200.git
pip install -r cne_hn_over200/requirements.txt
export OPENAI_API_KEY="sk‑..."
python -m cne_hn_over200 --min-score 300 --limit 15
```

### Environment variables

| Variable             | Purpose                                          | Default        |
| -------------------- | ------------------------------------------------ | -------------- |
| `OPENAI_API_KEY`     | Secret key for OpenAI access                     | **required**   |
| `AWS_HN_DAILY_MODEL` | Override the chat model used for summarisation   | `gpt-4.1-nano` |
| `AWS_HN_DAILY_WIDTH` | Default terminal width when auto‑detection fails | `80`           |

---

## Extending & customizing

* **Swap the LLM** by changing `MODEL_NAME` or passing a different model to `summarize_story()`.
* **Add columns** by editing `builder.build_rows()`.
* **Change the output format** by inserting a new renderer in `table_utils` before the fallback chain.

---

## Disclaimer

This README was produced by an AI model. Validate all information and audit the code before executing it in production environments.
