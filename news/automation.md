# Daily Feed Generation Plan

## Current v2 workflow

1. `news/scripts/collect_candidates.py` reads:
   - `news/data/profile.yaml`
   - `news/data/active-questions.yaml`
   - `news/data/sources.yaml`
   - `news/data/feedback.yaml`

2. It fetches configured RSS/Atom feeds, applies a recent-history dedupe guard, and prints a candidate JSON packet.

3. A Hermes cron job uses that candidate packet as context, curates only high-relevance items, writes:
   - `news/daily/YYYY-MM-DD.md`

4. The job commits and pushes the generated file to GitHub.

## Important design rule

The script gathers candidates. The agent decides relevance.

This prevents the system from becoming a dumb RSS summarizer. A final item should only be included if it passes at least one of these tests:

- updates a mental model
- clarifies a tradeoff or contradiction
- improves a real decision
- reveals a future pattern with consequences
- improves the knowledge system
- improves daughters' future-readiness

And it should usually be rejected if it is:

- generic AI news without implication
- conclusion-only writing with no tradeoffs
- inspirational quote energy
- low-substance emotional content
- a repeated take without new signal
- polished but obvious summary content

## Personal tracks

The feed is now optimized around these tracks:

- AI change
- daughters' future skills
- own-business learning
- better decisions
- remembering via the knowledge base

## Recent-item guard

`news/scripts/collect_candidates.py` now reads recent daily files and rejects URLs/titles that appeared in the last 14 days. Repeats should only return if there is materially new signal or a changed implication.

## Manual test

```bash
cd /home/ubuntu/.hermes/profiles/susu-bot/projects/susu-feed
python3 news/scripts/collect_candidates.py > /tmp/susu-feed-candidates.json
```

## Publishing

```bash
git add news README.md
git commit -m "Update daily feed"
git push
```

## Cron behavior

The cron job should be allowed to commit only when files changed. If no meaningful feed can be generated, it should write nothing and avoid pushing noise.
