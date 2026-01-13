"""Utility functions for the crawler."""

import logging
from typing import List, Optional, Dict, Any
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config import SiteConfig

LOG = logging.getLogger("news_crawler")


def make_session_with_retries(total: int = 3, backoff: float = 0.5) -> requests.Session:
    session = requests.Session()
    retries = Retry(total=total, backoff_factor=backoff, status_forcelist=(429, 500, 502, 503, 504))
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.headers.update({"User-Agent": "NewsCrawler/1.0 (+https://example)"})
    return session


def _safe_get(session: requests.Session, url: str, timeout: int = 15) -> Optional[requests.Response]:
    try:
        return session.get(url, timeout=timeout)
    except requests.RequestException:
        LOG.debug("Request failed: %s", url, exc_info=True)
        return None


def _find_links(soup: BeautifulSoup, selectors: List[str]) -> List[str]:
    links: List[str] = []
    for sel in selectors:
        for el in soup.select(sel):
            href = el.get("href") or el.get("data-href")
            if href:
                links.append(href)
    seen = set()
    ordered: List[str] = []
    for link in links:
        if link not in seen:
            seen.add(link)
            ordered.append(link)
    return ordered


def _extract_text(soup: BeautifulSoup, selectors: List[str]) -> str:
    for sel in selectors:
        node = soup.select_one(sel)
        if node:
            return node.get_text(separator=" ", strip=True)
    return ""


def _parse_article(session: requests.Session, url: str, cfg: SiteConfig, host: str) -> Optional[Dict[str, Any]]:
    resp = _safe_get(session, url)
    if not resp or resp.status_code != 200:
        return None
    soup = BeautifulSoup(resp.content, "html.parser")
    title = _extract_text(soup, cfg.title_selectors)
    # published time meta or selectors
    meta = soup.find("meta", property="article:published_time")
    date = meta.get("content") if meta and meta.get("content") else _extract_text(soup, cfg.date_selectors)

    content = ""
    for sel in cfg.content_selectors:
        node = soup.select_one(sel)
        if node:
            paragraphs = [p.get_text(strip=True) for p in node.find_all("p") if p.get_text(strip=True)]
            content = "\n\n".join(paragraphs) if paragraphs else node.get_text(separator=" ", strip=True)
            break
    if not content:
        paragraphs = [p.get_text(strip=True) for p in soup.find_all("p") if p.get_text(strip=True)]
        content = "\n\n".join(paragraphs)

    return {"title": title, "date": date, "content": content, "link": url, "source": host}