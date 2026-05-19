# SuSu Feed

A personal daily feed focused on material relevance, not generic news.

## Purpose

This feed is designed to answer:
- What actually matters to me today?
- What may change my decisions, priorities, or perspective?
- What is worth thinking about for work, life, family, and growth?

## Daily output shape

Each daily file should be short and high-signal:
1. What materially matters today
2. Why it matters to me
3. Idea sparks
4. Life/family nudge
5. Ignore this noise
6. Reflection question

## Structure

- `daily/` — one markdown file per day
- `weekly/` — weekly rollups and calibration
- `data/profile.yaml` — stable relevance model
- `data/active-questions.yaml` — what the feed should currently optimize for
- `data/sources.yaml` — source definitions and admission rules
- `data/feedback.yaml` — lightweight feedback loop and learning state
- `templates/` — markdown templates for daily and weekly generation

## Principles

- Optimize for relevance, not volume
- Organize by why it matters, not by source category
- Mix work, life, family, ideas, and growth
- Prefer decision support over summarization
- Suppress noise aggressively
