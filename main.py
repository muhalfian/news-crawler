"""Main entry point for the news crawler CLI."""

import argparse
import logging
import os

import pandas as pd

from config import DEFAULT_YEARS, SITE_CONFIG
from crawler import Crawler


def run_cli() -> None:
    parser = argparse.ArgumentParser(description="News crawler exporting to Excel")
    parser.add_argument("--sites", nargs="+", default=list(SITE_CONFIG.keys()), help="Sites to crawl")
    parser.add_argument("--years", type=str, default="2015-2026", help="Years range like 2015-2026 or single year")
    parser.add_argument("--out", default="data/news.xlsx", help="Output Excel file path")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    # Parse years
    if "-" in args.years:
        start, end = map(int, args.years.split("-"))
        years = list(range(start, end + 1))
    else:
        years = [int(args.years)]

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO, format="%(levelname)s: %(message)s")
    crawler = Crawler(years=years)
    all_articles = []
    for site_key in args.sites:
        cfg = SITE_CONFIG[site_key]
        start_url = cfg.base_url
        logging.info("Crawling %s", site_key)
        found = crawler.crawl_site(start_url)
        logging.info("Found %d articles from %s", len(found), site_key)
        all_articles.extend(found)

    if not all_articles:
        logging.info("No articles collected.")
        return

    df = pd.DataFrame(all_articles)
    df = df[["title", "date", "link", "content", "source"]]
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    df.to_excel(args.out, index=False)
    logging.info("Wrote %d articles to %s", len(df), args.out)


if __name__ == "__main__":
    run_cli()