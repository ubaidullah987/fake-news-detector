from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Any
from urllib.parse import urlparse

import requests

from src.config import DEFAULT_MODEL_NAME, MAX_INPUT_CHARS, MAX_SCRAPED_CHARS
from src.explain import build_explanation
from src.highlighting import HighlightedSegment, Trigger, build_highlighted_segments, detect_triggers
from src.scraper import scrape_url_text


class DetectionError(Exception):
    """Raised when the application cannot complete a detection request."""


@dataclass
class DetectionResult:
    label: str
    confidence: float
    confidence_percent: float
    risk_level: str
    explanation: str
    highlighted_segments: list[HighlightedSegment]
    triggers: list[Trigger]
    source_mode: str


@lru_cache(maxsize=1)
def load_transformer_pipeline():
    try:
        from transformers import pipeline

        return pipeline(
            "text-classification",
            model=DEFAULT_MODEL_NAME,
            truncation=True,
        )
    except Exception:
        return None


def _normalize_input(text: str) -> str:
    cleaned = " ".join(text.split())
    if not cleaned:
        raise DetectionError("The provided input is empty after cleaning. Please try a longer message or article.")
    return cleaned[:MAX_INPUT_CHARS]


def _risk_from_triggers(triggers: list[Trigger]) -> tuple[float, str]:
    high_risk_hits = sum(1 for trigger in triggers if trigger.severity == "High risk")
    moderate_hits = sum(1 for trigger in triggers if trigger.severity == "Moderate risk")
    score = min(0.15 + high_risk_hits * 0.16 + moderate_hits * 0.08, 0.99)

    if high_risk_hits >= 2 or score >= 0.72:
        return score, "High"
    if moderate_hits >= 1 or score >= 0.42:
        return score, "Medium"
    return max(score, 0.18), "Low"


def _run_transformer(text: str) -> tuple[str | None, float, str]:
    classifier = load_transformer_pipeline()
    if classifier is None:
        return None, 0.0, "Transformer model unavailable, so the app used fallback risk heuristics."

    try:
        raw_result: Any = classifier(text[:512])[0]
        label = str(raw_result.get("label", "")).lower()
        score = float(raw_result.get("score", 0.0))
    except Exception:
        return None, 0.0, "The transformer model could not process this input, so fallback heuristics were used."

    if "negative" in label:
        mapped_label = "Fake"
    elif "positive" in label:
        mapped_label = "Real"
    else:
        mapped_label = "Scam"

    summary = f"The transformer model detected a {mapped_label.lower()}-leaning tone with model confidence of {score * 100:.1f}%."
    return mapped_label, score, summary


def _fuse_scores(model_label: str | None, model_score: float, trigger_score: float, triggers: list[Trigger]) -> tuple[str, float]:
    if any(trigger.category == "Financial trap" for trigger in triggers) and trigger_score >= 0.45:
        return "Scam", max(trigger_score, model_score)

    if model_label == "Real" and trigger_score < 0.30:
        return "Real", max(model_score, 0.68)

    if trigger_score >= 0.65:
        return "Scam", max(trigger_score, model_score)

    if trigger_score >= 0.38:
        return "Fake", max(trigger_score, model_score, 0.62)

    if model_label:
        return model_label, max(model_score, 0.55)

    return "Real", 0.64


def predict_from_text(text: str) -> DetectionResult:
    normalized = _normalize_input(text)
    triggers = detect_triggers(normalized)
    trigger_score, risk_level = _risk_from_triggers(triggers)
    model_label, model_score, model_summary = _run_transformer(normalized)
    label, confidence = _fuse_scores(model_label, model_score, trigger_score, triggers)
    explanation = build_explanation(label, triggers, model_summary)
    highlighted_segments = build_highlighted_segments(normalized, triggers)

    return DetectionResult(
        label=label,
        confidence=confidence,
        confidence_percent=confidence * 100,
        risk_level=risk_level,
        explanation=explanation,
        highlighted_segments=highlighted_segments,
        triggers=triggers,
        source_mode="Text",
    )


def predict_from_url(url: str) -> DetectionResult:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise DetectionError("Please enter a valid URL that starts with http:// or https://")

    try:
        article_text = scrape_url_text(url)
    except requests.RequestException as exc:
        raise DetectionError(f"Could not fetch the page content: {exc}") from exc

    if not article_text.strip():
        raise DetectionError("The page was fetched, but no readable article text could be extracted.")

    result = predict_from_text(article_text[:MAX_SCRAPED_CHARS])
    result.source_mode = "URL"
    return result
