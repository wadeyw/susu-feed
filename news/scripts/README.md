# SuSu Feed Automation

This folder contains the lightweight automation helpers for the personal feed.

## collect_candidates.py

Collects a candidate packet from `news/data/sources.yaml` and prints JSON.
It does not decide the final feed. The final selection should be done by an
LLM/agent using:

- `news/data/profile.yaml`
- `news/data/active-questions.yaml`
- `news/data/sources.yaml`
- `news/data/feedback.yaml`
- `news/data/conversation-bank.md` (small-talk skill drill)

Manual test:

```bash
cd /home/ubuntu/.hermes/profiles/susu-bot/projects/susu-feed
python3 news/scripts/collect_candidates.py > /tmp/susu-feed-candidates.json
```

The Hermes cron job uses this candidate packet as context, then writes a daily
markdown file under `news/daily/YYYY-MM-DD.md` and pushes it to GitHub.

### Feed types (v3)

`sources.yaml` `feeds` entries carry a `type`:

- `rss` (default) — URL is an RSS/Atom feed, parsed with the standard parser.
- `api` — URL (+ optional `params`) is a JSON endpoint returning a list of
  items; normalized to `{title, url, published, summary}`.
- `sitemap` — URL is a content sitemap; the newest N `<loc>` URLs are used as
  items (no RSS on the site). Best-effort: no dates, ordering not guaranteed —
  the agent curates.

A single broken feed is logged under `fetch_errors` and never crashes the
run. Sitemap/API types are resilient the same way.

### v3 tracks (from `profile.yaml`)

1. **influencer_mktg** — work (result-driven influencer platform; IG/YouTube/
   TikTok; China-going-overseas clients; competitor = Ahacreator)
2. **ai_change** — latest AI, narrowed (tools that could hit our workflow +
   one structural item)
3. **cross_industry** — rotating opposite industry, one item/week (ISO-week
   rotation lives in `profile.yaml` `focus_tracks.rotation`)
4. **family_future** — two daughters (born 2022-12, 2024-06), education +
   tech-lit readiness
5. **skill_drill** — small-talk practice; generated from
   `conversation-bank.md` in its own slot, not from candidates
