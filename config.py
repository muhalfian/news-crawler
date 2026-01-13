"""Configuration module for crawler settings."""

from dataclasses import dataclass, field
from typing import List, Dict


DEFAULT_YEARS = list(range(2015, 2027))


@dataclass
class SiteConfig:
    list_selectors: List[str] = field(default_factory=lambda: ["article a", "h2 a", ".post a"])
    title_selectors: List[str] = field(default_factory=lambda: ["h1", ".entry-title"])
    date_selectors: List[str] = field(default_factory=lambda: ["time", ".entry-date"]) 
    content_selectors: List[str] = field(default_factory=lambda: [".entry-content", "article", "#content"])
    base_path: str = "/{year}"
    base_url: str = "" 


SITE_CONFIG: Dict[str, SiteConfig] = {
    "tatoli.tl": SiteConfig(
        list_selectors=["article a", ".entry-title a", "h2.title a"],
        title_selectors=["h1.entry-title", "h1.title", "h1"],
        date_selectors=["time", ".entry-date", "meta[property='article:published_time']"],
        content_selectors=[".entry-content", ".post-content", "article"],
        base_url="https://tatoli.tl/",
    ),
    "thediliweekly.com": SiteConfig(
        list_selectors=["article a", ".entry-title a", "h2 a"],
        title_selectors=["h1.entry-title", "h1"],
        base_url="https://thediliweekly.com/",
    ),
    "www.rmtl.org": SiteConfig(
        list_selectors=["article a", ".post a", "h2 a"],
        title_selectors=["h1.entry-title", "h1"],
        content_selectors=[".entry-content", ".post-content", "article", "#content"],
        base_path="/blog/{year}",
        base_url="https://www.rmtl.org/blog/",
    ),
}