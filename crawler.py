"""Crawler class module."""

from typing import List, Optional, Dict, Any
import logging
import time
import re
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from config import SITE_CONFIG, SiteConfig, DEFAULT_YEARS
from utils import _safe_get, _find_links, _parse_article, LOG, make_session_with_retries


class Crawler:
    """Crawl listing pages for a site across years and export articles."""

    def __init__(self, session: Optional[requests.Session] = None, years: Optional[List[int]] = None, rate: float = 1.0):
        self.session = session or make_session_with_retries()
        self.years = years or DEFAULT_YEARS
        self.rate = rate

    def _build_listing_url(self, parsed_base, cfg: SiteConfig, year: int, page: int) -> str:
        base = cfg.base_path.format(year=year)
        if page == 1:
            return f"{parsed_base.scheme}://{parsed_base.netloc}{base}/"
        else:
            return f"{parsed_base.scheme}://{parsed_base.netloc}{base}/page/{page}/"

    def  crawl_site(self, start_url: str) -> List[Dict[str, Any]]:
        parsed = urlparse(start_url)
        host = parsed.netloc
        cfg = SITE_CONFIG.get(host, SiteConfig())
        results: List[Dict[str, Any]] = []
        article_count = 0

        # Extract year from start_url if present, e.g., /2016/
        year_match = re.search(r'/(\d{4})/', start_url)
        years_to_crawl = [int(year_match.group(1))] if year_match else self.years

        for year in years_to_crawl:
            page = 1
            while True:
                url = self._build_listing_url(parsed, cfg, year, page)
                LOG.info("Crawling page %d for year %d on %s", page, year, host)
                resp = _safe_get(self.session, url)
                if not resp or resp.status_code != 200:
                    LOG.info("No more pages for year %d on %s (status: %s)", year, host, resp.status_code if resp else 'None')
                    break
                soup = BeautifulSoup(resp.content, "html.parser")
                raw_links = _find_links(soup, cfg.list_selectors)
                links = [urljoin(url, l) for l in raw_links]
                if not links:
                    LOG.info("No article links on page %d for year %d on %s", page, year, host)
                    break
                for link in links:
                    article = _parse_article(self.session, link, cfg, host)
                    if article:
                        results.append(article)
                        article_count += 1
                        LOG.info("Processed article %d: %s", article_count, article['title'][:50] if article['title'] else 'No title')
                    time.sleep(self.rate)
                page += 1
            time.sleep(self.rate)
        return results
