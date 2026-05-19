# Daily Feed Generation Plan

## Current v1 workflow

1. `news/scripts/collect_candidates.py` reads:
   - `news/data/profile.yaml`
   - `news/data/active-questions.yaml`
   - `news/data/sources.yaml`
   - `news/data/feedback.yaml`

2. It fetches configured RSS/Atom feeds and prints a candidate JSON packet.

3. A Hermes cron job uses that candidate packet as context, curates only high-relevance items, writes:
   - `news/daily/YYYY-MM-DD.md`

4. The job commits and pushes the generated file to GitHub.

## Important design rule

The script gathers candidates. The agent decides relevance.

This prevents the system from becoming a dumb RSS summarizer. A final item should only be included if it passes at least one of these tests:

- improves a decision
- challenges a stale assumption
- reveals an early pattern
- sparks a concrete idea
- improves life or family quality

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
