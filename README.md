# News Crawler (Python)

Simple Python crawler that fetches articles (title, date, content, link, source) from listing pages across multiple years and exports results to an Excel file in the "data" folder.

## Features
- Crawls multiple news sites automatically.
- Supports year ranges (e.g., "2015-2020").
- Exports to Excel with source information.
- Interactive CLI progress display.
- 1-second delay per article to avoid blocking.

## Installation

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# or cmd
.\.venv\Scripts\activate.bat
pip install -r requirements.txt
```

## Usage

Run the crawler with default settings (all sites, years 2015-2026):

```bash
python main.py
```

### Examples

- **Crawl specific year range from all sites:**
  ```bash
  python main.py --years "2016-2018"
  ```

- **Crawl specific sites and years:**
  ```bash
  python main.py --sites tatoli.tl thediliweekly.com --years "2017"
  ```

- **Custom output file:**
  ```bash
  python main.py --years "2015-2020" --out data/custom_output.xlsx
  ```

- **Enable debug logging:**
  ```bash
  python main.py --debug
  ```

### Arguments
- `--sites`: List of sites to crawl (default: all sites in config).
- `--years`: Year range like "2015-2020" or single year (default: "2015-2026").
- `--out`: Output Excel file path (default: "data/news.xlsx").
- `--debug`: Enable debug logging.

### Output
- All Excel files are saved in the "data" folder.
- Columns: title, date, link, content, source.
- The crawler provides real-time progress in the CLI.

## Notes
- The crawler uses CSS selectors configured in `config.py`. Adjust if needed.
- It stops when no more articles or pages are found.
- Rate limited to 1 request per second per article to avoid blocks.
