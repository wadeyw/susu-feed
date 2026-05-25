#!/usr/bin/env python3
"""Collect candidate items for SuSu Feed.

This script intentionally does not generate the final daily feed. It gathers a
candidate packet from configured feeds so an LLM/agent can curate against
profile.yaml, active-questions.yaml, sources.yaml, feedback.yaml, and recent
published history.
"""
from __future__ import annotations

import datetime as dt
import email.utils
import html
import json
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

try:
    import yaml
except Exception as exc:  # pragma: no cover
    print(f"PyYAML is required: {exc}", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[2]
NEWS = ROOT / "news"
DATA = NEWS / "data"
DAILY = NEWS / "daily"
SOURCES = DATA / "sources.yaml"
PROFILE = DATA / "profile.yaml"
QUESTIONS = DATA / "active-questions.yaml"
FEEDBACK = DATA / "feedback.yaml"

USER_AGENT = "SuSuFeed/0.2 (+https://github.com/wadeyw/susu-feed)"
MAX_PER_FEED = 6
MAX_TOTAL = 60
TIMEOUT = 12
SOURCE_LINE_RE = re.compile(r"^- Source: (?P<source_name>.+?) — (?P<url>https?://\S+)\s*$")
TITLE_LINE_RE = re.compile(r"^### \d+\) (?P<title>.+?)\s*$")
DATE_LINE_RE = re.compile(r"^# (?P<date>\d{4}-\d{2}-\d{2}) Daily Feed\s*$")


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text()) or {}


def strip_text(value: str | None, limit: int = 500) -> str:
    if not value:
        return ""
    value = re.sub(r"<[^>]+>", " ", value)
    value = html.unescape(value)
    value = re.sub(r"\s+", " ", value).strip()
    return value[:limit]


def slug_text(value: str | None) -> str:
    return re.sub(r"\W+", " ", (value or '').lower()).strip()


def parse_date(value: str | None) -> str | None:
    if not value:
        return None
    try:
        parsed = email.utils.parsedate_to_datetime(value)
        if parsed.tzinfo:
            parsed = parsed.astimezone(dt.timezone.utc)
        return parsed.date().isoformat()
    except Exception:
        return strip_text(value, 80) or None


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return resp.read(2_000_000)


def child_text(elem: ET.Element, names: list[str]) -> str:
    for name in names:
        found = elem.find(name)
        if found is not None and found.text:
            return found.text
    wanted = {n.split("}")[-1].lower() for n in names}
    for child in list(elem):
        if child.tag.split("}")[-1].lower() in wanted and child.text:
            return child.text
    return ""


def child_attr(elem: ET.Element, child_name: str, attr: str) -> str:
    for child in list(elem):
        if child.tag.split("}")[-1].lower() == child_name.lower():
            return child.attrib.get(attr, "")
    return ""


def parse_feed(xml_bytes: bytes) -> list[dict[str, str | None]]:
    root = ET.fromstring(xml_bytes)
    tag = root.tag.split("}")[-1].lower()
    if tag == "rss":
        channel = root.find("channel")
        items = [] if channel is None else channel.findall("item")
        out = []
        for item in items:
            out.append({
                "title": strip_text(child_text(item, ["title"]), 180),
                "url": strip_text(child_text(item, ["link"]), 500),
                "published": parse_date(child_text(item, ["pubDate", "published", "updated"])),
                "summary": strip_text(child_text(item, ["description", "summary", "content"]), 500),
            })
        return out
    entries = [e for e in root.iter() if e.tag.split("}")[-1].lower() == "entry"]
    out = []
    for entry in entries:
        link = child_attr(entry, "link", "href") or child_text(entry, ["link"])
        out.append({
            "title": strip_text(child_text(entry, ["title"]), 180),
            "url": strip_text(link, 500),
            "published": parse_date(child_text(entry, ["published", "updated"])),
            "summary": strip_text(child_text(entry, ["summary", "content"]), 500),
        })
    return out


def collect_recent_history(lookback_days: int) -> dict[str, Any]:
    today = dt.date.today()
    recent_urls: set[str] = set()
    recent_title_slugs: set[str] = set()
    recent_items: list[dict[str, str]] = []

    for path in sorted(DAILY.glob('*.md'), reverse=True):
        text = path.read_text()
        lines = text.splitlines()
        feed_date = None
        titles: list[str] = []
        source_pairs: list[tuple[str, str]] = []
        for line in lines:
            if feed_date is None:
                m = DATE_LINE_RE.match(line)
                if m:
                    feed_date = dt.date.fromisoformat(m.group('date'))
                    continue
            title_match = TITLE_LINE_RE.match(line)
            if title_match:
                titles.append(title_match.group('title').strip())
                continue
            source_match = SOURCE_LINE_RE.match(line)
            if source_match:
                source_pairs.append((source_match.group('source_name').strip(), source_match.group('url').strip()))
        if feed_date is None or (today - feed_date).days > lookback_days:
            continue
        for idx, (source_name, url) in enumerate(source_pairs):
            title = titles[idx] if idx < len(titles) else ''
            recent_urls.add(url)
            if title:
                recent_title_slugs.add(slug_text(title))
            recent_items.append({
                'date': feed_date.isoformat(),
                'title': title,
                'url': url,
                'source_name': source_name,
            })
    return {
        'lookback_days': lookback_days,
        'recent_urls': sorted(recent_urls),
        'recent_title_slugs': sorted(recent_title_slugs),
        'recent_items': recent_items[:50],
    }


def main() -> int:
    sources = load_yaml(SOURCES)
    profile = load_yaml(PROFILE)
    questions = load_yaml(QUESTIONS)
    feedback = load_yaml(FEEDBACK)

    reuse_guard = sources.get('recent_reuse_guard', {}) or {}
    lookback_days = int(reuse_guard.get('lookback_days', 7))
    history = collect_recent_history(lookback_days) if reuse_guard.get('enabled', True) else {
        'lookback_days': 0,
        'recent_urls': [],
        'recent_title_slugs': [],
        'recent_items': [],
    }
    recent_url_set = set(history['recent_urls'])
    recent_title_slug_set = set(history['recent_title_slugs'])

    packet: dict[str, Any] = {
        'generated_at_utc': dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds'),
        'repo_root': str(ROOT),
        'output_path_suggestion': f"news/daily/{dt.date.today().isoformat()}.md",
        'purpose': 'Candidate packet for LLM curation. Do not include items unless they materially matter to the user.',
        'selection_rules': profile.get('selection_rules', {}),
        'anti_slop': profile.get('anti_slop', {}),
        'source_admission_rules': sources.get('admission_rules', {}),
        'manual_watch_topics': sources.get('manual_watch_topics', []),
        'focus_tracks': profile.get('focus_tracks', []),
        'active_questions': questions.get('questions', []),
        'feedback_states': feedback.get('item_feedback_states', []),
        'recent_reuse_guard': {
            'enabled': reuse_guard.get('enabled', True),
            'lookback_days': history['lookback_days'],
            'blocked_recent_url_count': len(recent_url_set),
            'blocked_recent_title_count': len(recent_title_slug_set),
            'recent_items': history['recent_items'],
        },
        'candidates': [],
        'filtered_recent_duplicates': [],
        'fetch_errors': [],
    }

    for feed in sources.get('feeds', []):
        try:
            xml_bytes = fetch(feed['url'])
            parsed = parse_feed(xml_bytes)[:MAX_PER_FEED]
            for item in parsed:
                title = item.get('title') or ''
                url = item.get('url') or ''
                if not title or not url:
                    continue
                title_slug = slug_text(title)
                duplicate_reasons = []
                if reuse_guard.get('block_same_url', True) and url in recent_url_set:
                    duplicate_reasons.append('recent_url')
                if reuse_guard.get('block_same_title', True) and title_slug and title_slug in recent_title_slug_set:
                    duplicate_reasons.append('recent_title')
                if duplicate_reasons:
                    packet['filtered_recent_duplicates'].append({
                        'source_id': feed.get('id'),
                        'title': title,
                        'url': url,
                        'reasons': duplicate_reasons,
                    })
                    continue
                packet['candidates'].append({
                    'source_id': feed.get('id'),
                    'source_name': feed.get('name'),
                    'source_role': feed.get('role'),
                    'track_bias': feed.get('track_bias', []),
                    'trust': feed.get('trust'),
                    'source_why': feed.get('why'),
                    'source_caution': feed.get('caution'),
                    **item,
                })
        except (urllib.error.URLError, TimeoutError, ET.ParseError, KeyError) as exc:
            packet['fetch_errors'].append({
                'source_id': feed.get('id'),
                'url': feed.get('url'),
                'error': str(exc)[:300],
            })

    packet['candidates'] = packet['candidates'][:MAX_TOTAL]
    print(json.dumps(packet, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
