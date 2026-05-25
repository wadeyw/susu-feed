# AGENTS.md

Repository guidance for SuSu Feed.

## GitHub Pages routing

GitHub Pages does not provide automatic folder browsing for this repo, so explicit index pages are used:
- `index.html`
- `news/index.html`
- `news/daily/index.html`
- `news/weekly/index.html`
- `reports/index.html`

These index pages auto-discover markdown files in their mapped directories using the GitHub contents API.

## Normal content additions

You do NOT need to manually update an index page when adding normal markdown files under:
- `news/daily/`
- `news/weekly/`
- `reports/`

Those should appear automatically in the corresponding directory index.

## When you DO need to update an index page

Update the relevant `index.html` when:
- a new top-level content area should appear in navigation
- a directory path changes
- the GitHub owner/repo/branch changes
- labels or section layout should change

## Content placement

- Daily feeds -> `news/daily/`
- Weekly summaries -> `news/weekly/`
- Standalone deep-dive reports -> `reports/`
