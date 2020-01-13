# Newspaper

Newspaper is a simple framework for crawling the websites of different departments in my school. Its main functionality is to generate Excel documents with statistical charts based on hits on the news page, revealing how the website updates the relating news.

## Requirements

- `bs4`
- `requests`
- `pandas` (optional)

You can install the above dependencies via `pip install`。

## Usage

Change the following parts of code to suit your need:

- `base_url`
- `news_url`
- `headers` (optional)
- `max_page`
- `SoupStrainer` Filters
- util functions such as `page2url, get*, fillTable`
- other functions, e.g. to GET other pages beforehand

For more details, check out the given examples `Newspaper-comm.py` and `Newspaper-soci.py`.
