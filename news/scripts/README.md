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

Manual test:

```bash
cd /home/ubuntu/.hermes/profiles/susu-bot/projects/susu-feed
python3 news/scripts/collect_candidates.py > /tmp/susu-feed-candidates.json
```

The Hermes cron job uses this candidate packet as context, then writes a daily
markdown file under `news/daily/YYYY-MM-DD.md` and pushes it to GitHub.
