from __future__ import annotations

from bs4 import BeautifulSoup
import requests

from src.config import REQUEST_TIMEOUT


def scrape_url_text(url: str) -> str:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36"
        )
    }
    response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "noscript", "iframe", "header", "footer", "nav"]):
        tag.decompose()

    article_root = soup.find("article") or soup.find("main") or soup.body or soup
    blocks = article_root.find_all(["h1", "h2", "h3", "p", "li"])
    text_parts = [block.get_text(" ", strip=True) for block in blocks if block.get_text(strip=True)]

    if not text_parts:
        text_parts = [article_root.get_text(" ", strip=True)]

    return "\n".join(text_parts).strip()
