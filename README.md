# Arabic Academic Research Toolkit

Open-source Python tooling for auditing Arabic academic prose, enforcing methodological precision, removing AI-generated clichés, and supporting reproducible humanities research workflows integrated with **Obsidian (Zettelkasten)** and **Google Antigravity**.

## Research Context

Arabic-language scholarship in philosophy of religion, epistemology, and classical Islamic philosophical theology (*Kalām*) frequently faces two technical bottlenecks:
1. **Methodological & Stylistic Drift**: AI-assisted drafting introduces translational clichés, vague generalizations, and unrigorous polemical terminology instead of analytical precision.
2. **Reproducibility & Knowledge Management**: Bridging classical Arabic primary sources, printed page citations, and contemporary analytic literature requires structured verification pipelines.

## Components

- **`arabic_academic_humanizer.py`** — Core static analyzer and rule-based purifier:
  - Detects and purges common AI clichés, rhetorical filler, and journalistic calques.
  - Enforces analytical terminology (e.g., replacing polemical *critique/deconstruction* with *epistemological and dialectical analysis*).
  - Replaces ambiguous foreign loanwords with precise classical Arabic equivalents.
  - Computes a quantitative **Human Scholarly Index (0–100)** per draft.
- **`humanize.py`** — Unified CLI supporting:
  - Single-file inspection (`python humanize.py article.md`)
  - Safe in-place purification with backup (`--in-place`)
  - Instant clipboard purification (`--clip`)
  - Live folder/Obsidian vault watcher (`--watch ./vault_drafts`)
- **`academic_humanizer_studio.py`** — Interactive RTL Gradio web studio with live metrics, rule violation tables, sample presets, and batch Markdown/TXT file processing.

## Integration with Obsidian & Google Antigravity

Designed to run inside an **Obsidian Zettelkasten** research vault alongside **Google Antigravity** agentic workflows:
- Point `--watch` at an Obsidian drafts folder (`03. Chapters/` or `02. Notes/`) so every saved Markdown note is automatically audited for stylistic rigor and methodological compliance before citation verification.
- Combine with local bilingual RAG and PDF/page-number verification scripts to ensure primary texts, commentaries, and footnotes remain strictly separated and reproducible.

## Installation & Usage

```bash
pip install -r requirements.txt

# Analyze a Markdown draft
python humanize.py draft.md

# Watch an Obsidian vault folder live
python humanize.py --watch ./my_obsidian_vault/drafts

# Launch the interactive Gradio studio
python academic_humanizer_studio.py
```

## Author

**Abderrahim Kaci** — University of Algiers 1 (Benyoucef Benkhedda), Faculty of Islamic Sciences.

## License

MIT License. See [LICENSE](LICENSE).
