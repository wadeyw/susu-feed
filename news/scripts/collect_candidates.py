#!/usr/bin/env python3
"""Collect candidate items for SuSu Feed.

This script intentionally does not generate the final daily feed. It gathers a
small candidate packet from configured feeds so an LLM/agent can curate against
profile.yaml, active-questions.yaml, and feedback.yaml.
"""
from __future__ import annotations

import datetime as dt
import email.utils
import html
import json
import re
import sys
import textwrap
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
SOURCES = NEWS / "data" / "sources.yaml"
PROFILE = NEWS / "data" / "profile.yaml"
QUESTIONS = NEWS / "data" / "active-questions.yaml"
FEEDBACK = NEWS / "data" / "feedback.yaml"

USER_AGENT = "SuSuFeed/0.1 (+https://github.com/wadeyw/susu-feed)"
MAX_PER_FEED = 5
MAX_TOTAL = 40
TIMEOUT = 12


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
    # Namespace-insensitive fallback.
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
    items: list[ET.Element]
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
    # Atom fallback.
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


def main() -> int:
    sources = load_yaml(SOURCES)
    profile = load_yaml(PROFILE)
    questions = load_yaml(QUESTIONS)
    feedback = load_yaml(FEEDBACK)

    packet: dict[str, Any] = {
        "generated_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "repo_root": str(ROOT),
        "output_path_suggestion": f"news/daily/{dt.date.today().isoformat()}.md",
        "purpose": "Candidate packet for LLM curation. Do not include items unless they materially matter to the user.",
        "selection_rules": sources.get("admission_rules", {}),
        "manual_watch_topics": sources.get("manual_watch_topics", []),
        "relevance_domains": profile.get("relevance_domains", []),
        "active_questions": questions.get("questions", []),
        "feedback_states": feedback.get("item_feedback_states", []),
        "candidates": [],
        "fetch_errors": [],
    }

    for feed in sources.get("feeds", []):
        try:
            xml_bytes = fetch(feed["url"])
            parsed = parse_feed(xml_bytes)[:MAX_PER_FEED]
            for item in parsed:
                if not item.get("title") or not item.get("url"):
                    continue
                packet["candidates"].append({
                    "source_id": feed.get("id"),
                    "source_name": feed.get("name"),
                    "bucket": feed.get("bucket"),
                    "source_why": feed.get("why"),
                    "source_caution": feed.get("caution"),
                    **item,
                })
        except (urllib.error.URLError, TimeoutError, ET.ParseError, KeyError) as exc:
            packet["fetch_errors"].append({
                "source_id": feed.get("id"),
                "url": feed.get("url"),
                "error": str(exc)[:300],
            })

    packet["candidates"] = packet["candidates"][:MAX_TOTAL]
    print(json.dumps(packet, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
