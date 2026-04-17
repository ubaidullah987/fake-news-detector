from __future__ import annotations

import html
import re
from dataclasses import dataclass

from src.config import RISK_LEXICON


@dataclass
class Trigger:
    term: str
    category: str
    severity: str


@dataclass
class HighlightedSegment:
    text: str
    severity: str | None = None


def detect_triggers(text: str) -> list[Trigger]:
    lowered = text.lower()
    triggers: list[Trigger] = []

    category_map = {
        "urgent": "Urgency",
        "act now": "Urgency",
        "limited time": "Urgency",
        "verify your account": "Account pressure",
        "claim now": "Urgency",
        "wire transfer": "Financial trap",
        "crypto giveaway": "Financial trap",
        "password reset": "Account pressure",
        "free money": "Financial trap",
        "win now": "Financial trap",
        "guaranteed": "Unrealistic promise",
        "exclusive offer": "Manipulation",
        "click here immediately": "Urgency",
        "your account will be closed": "Account pressure",
        "shocking": "Emotional trigger",
        "unbelievable": "Emotional trigger",
        "secret": "Manipulation",
        "once in a lifetime": "Manipulation",
        "risk free": "Unrealistic promise",
        "investment opportunity": "Financial trap",
        "bonus": "Manipulation",
        "miracle": "Emotional trigger",
        "lottery": "Financial trap",
        "congratulations": "Manipulation",
        "double your money": "Financial trap",
        "urgent response": "Urgency",
    }

    for severity, phrases in RISK_LEXICON.items():
        for phrase in phrases:
            if phrase in lowered:
                triggers.append(
                    Trigger(
                        term=phrase,
                        category=category_map.get(phrase, "Risk indicator"),
                        severity=severity,
                    )
                )
    return triggers


def build_highlighted_segments(text: str, triggers: list[Trigger]) -> list[HighlightedSegment]:
    if not text.strip():
        return [HighlightedSegment(text="No text available to highlight.")]

    matches: list[tuple[int, int, str]] = []
    for trigger in triggers:
        pattern = re.compile(re.escape(trigger.term), flags=re.IGNORECASE)
        for found in pattern.finditer(text):
            severity = "high" if trigger.severity == "High risk" else "moderate"
            matches.append((found.start(), found.end(), severity))

    if not matches:
        return [HighlightedSegment(text=text)]

    matches.sort(key=lambda item: item[0])
    collapsed: list[tuple[int, int, str]] = []
    for start, end, severity in matches:
        if not collapsed or start > collapsed[-1][1]:
            collapsed.append((start, end, severity))
            continue

        previous_start, previous_end, previous_severity = collapsed[-1]
        merged_severity = "high" if "high" in {severity, previous_severity} else "moderate"
        collapsed[-1] = (previous_start, max(previous_end, end), merged_severity)

    segments: list[HighlightedSegment] = []
    cursor = 0
    for start, end, severity in collapsed:
        if cursor < start:
            segments.append(HighlightedSegment(text=text[cursor:start]))
        segments.append(HighlightedSegment(text=text[start:end], severity=severity))
        cursor = end

    if cursor < len(text):
        segments.append(HighlightedSegment(text=text[cursor:]))

    return segments


def render_highlighted_html(segments: list[HighlightedSegment]) -> str:
    parts: list[str] = ['<div class="highlight-box">']
    for segment in segments:
        escaped = html.escape(segment.text)
        if segment.severity == "high":
            parts.append(f'<span class="highlight high-risk">{escaped}</span>')
        elif segment.severity == "moderate":
            parts.append(f'<span class="highlight moderate-risk">{escaped}</span>')
        else:
            parts.append(f"<span>{escaped}</span>")
    parts.append("</div>")
    return "".join(parts)
