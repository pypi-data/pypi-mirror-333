# CapitolScraper
A web scraper for [capitoltrades](https://www.capitoltrades.com/), a website dedicated to tracking
Congress stock trades.

## Requirements
* [uv](https://github.com/astral-sh/uv)

## Installation
All main dependencies can be installed through `uv sync --no-group dev`.
For developer and testing dependencies, use `uv sync --all-groups`.

## Quickstart
```python
from scraper import Trades

scraper = Trades()
print(scraper.trades)
```

## Authors
* [TonyGrif](https://github.com/TonyGrif) - Creator and Maintainer
