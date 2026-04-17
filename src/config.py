from __future__ import annotations

import os


APP_TITLE = "Fake News & Scam Detector"
DEFAULT_MODEL_NAME = os.getenv(
    "DETECTOR_MODEL_NAME",
    "cardiffnlp/twitter-roberta-base-sentiment-latest",
)
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "12"))
MAX_INPUT_CHARS = int(os.getenv("MAX_INPUT_CHARS", "5000"))
MAX_SCRAPED_CHARS = int(os.getenv("MAX_SCRAPED_CHARS", "4000"))

LABELS = ["Fake", "Real", "Scam"]

RISK_LEXICON = {
    "High risk": [
        "urgent",
        "act now",
        "limited time",
        "verify your account",
        "claim now",
        "wire transfer",
        "crypto giveaway",
        "password reset",
        "free money",
        "win now",
        "guaranteed",
        "exclusive offer",
        "click here immediately",
        "your account will be closed",
    ],
    "Moderate risk": [
        "shocking",
        "unbelievable",
        "secret",
        "once in a lifetime",
        "risk free",
        "investment opportunity",
        "bonus",
        "miracle",
        "lottery",
        "congratulations",
        "double your money",
        "urgent response",
    ],
}
