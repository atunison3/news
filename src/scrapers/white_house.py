import requests
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta, timezone


def get_white_house_news():
    """Queries the news on whitehouse.gov"""

    # Acquire today's date
    today = date.today().strftime("%B %-d, %Y")  # e.g., April 25, 2026

    # Crawl White House's news page
    url = "https://www.whitehouse.gov/news/"
    headers = {
        "User-Agent": "andy-data-project/1.0 (contact: andrew.e.tunison@gmail.com)",
        "Accept": "text/html,application/xhtml+xml",
    }
    html = requests.get(url, timeout=20).text
    soup = BeautifulSoup(html, "html.parser")

    # Filter to news article titles/links
    results = []
    elements = soup.select("h2:has(a)")
    for h2 in soup.select("h2:has(a)"):
        a = h2.find("a")

        # go up to the parent container (the <div> wrapping everything)
        container = h2.find_parent("div")

        # find the <time> inside that container
        time_tag = container.find("time")

        # Get the date
        article_date = (
            datetime.fromisoformat(time_tag["datetime"]).astimezone(timezone.utc)
            if time_tag
            else None
        )
        todays_date = datetime.now(timezone.utc)

        if (article_date) and ((todays_date - article_date).days <= 7):
            results.append(
                {
                    "title": a.get_text(strip=True),
                    "url": a["href"],
                    "date": article_date,
                    "source": "White House",
                }
            )

    return results
