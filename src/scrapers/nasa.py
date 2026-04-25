import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urlparse


def extract_date_from_nasa_url(url: str) -> datetime:
    """Extracts the date from a NASA news article's url"""

    if not url:
        return None

    path_parts = urlparse(url).path.strip("/").split("/")

    for i in range(len(path_parts) - 2):
        year, month, day = path_parts[i : i + 3]

        if year.isdigit() and month.isdigit() and day.isdigit():
            if len(year) == 4 and len(month) == 2 and len(day) == 2:
                return datetime.fromisoformat(f"{year}-{month}-{day}")

    return None


def extract_nasa_article(article_div: str) -> dict:
    """Extract article data from a NASA hds-content-item div."""

    heading_link = article_div.select_one("a.hds-content-item-heading")
    title_tag = article_div.select_one(".hds-a11y-heading-22")
    readtime_tag = article_div.select_one(".hds-content-item-readtime")
    summary_tag = article_div.select_one("p")
    content_type_tag = article_div.select_one(".display-flex span")
    image_tag = article_div.select_one("img")
    article_url = (heading_link.get("href") if heading_link else None,)
    article_date = datetime.now()

    return {
        "title": title_tag.get_text(strip=True) if title_tag else None,
        "url": article_url[0],
        "date": article_date,
        "source": "NASA",
        "read_time": readtime_tag.get_text(strip=True) if readtime_tag else None,
        "summary": summary_tag.get_text(" ", strip=True) if summary_tag else None,
        "content_type": (
            content_type_tag.get_text(strip=True) if content_type_tag else None
        ),
        "image_url": image_tag.get("src") if image_tag else None,
    }


def get_nasa_news() -> list[dict]:
    """Crawls the NASA recently published website for news"""

    url = "https://www.nasa.gov/news/recently-published/"

    headers = {
        "User-Agent": "andy-news-project/1.0",
        "Accept": "text/html,application/xhtml+xml",
    }

    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    articles = []

    for article_div in soup.select("div.hds-content-item"):
        article = extract_nasa_article(article_div)

        if article["title"] and article["url"]:
            articles.append(article)

    return articles
