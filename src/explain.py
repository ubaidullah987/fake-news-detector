from __future__ import annotations

from collections import Counter


def build_explanation(label: str, triggers: list, model_summary: str) -> str:
    if not triggers and model_summary:
        return (
            f"The detector leaned toward {label.lower()} content based on the language patterns learned by the model. "
            f"{model_summary}"
        )

    category_counts = Counter(trigger.category for trigger in triggers)
    category_summary = ", ".join(
        f"{count} {category.lower()} trigger{'s' if count > 1 else ''}"
        for category, count in category_counts.items()
    )

    if label == "Scam":
        prefix = "This text was flagged as a likely scam because it combines manipulative language with risky call-to-action patterns."
    elif label == "Fake":
        prefix = "This text was flagged as likely fake because it uses sensational or credibility-weakening patterns often seen in misinformation."
    else:
        prefix = "This text looks comparatively safer because it contains fewer scam or misinformation indicators."

    if category_summary:
        prefix += f" The strongest signals were: {category_summary}."

    if model_summary:
        prefix += f" {model_summary}"

    return prefix
