from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup


@dataclass
class Quote:
    text: str
    author: str
    tags: list[str]


def get_last_page() -> int:
    count = 1
    while True:
        content = requests.get(f"https://quotes.toscrape.com/page/{count}").content
        soup = BeautifulSoup(content, "html.parser")
        if (
            soup.select_one("div.row:not(.header-box) > div.col-md-8")
            .find(string=True)
            .strip()
            == "No quotes found!"
        ):
            return count - 1
        count += 1


def get_data_from_page(page: int):
    content = requests.get(f"https://quotes.toscrape.com/page/{page}").content
    soup = BeautifulSoup(content, "html.parser")
    all_quotes = soup.select("div.quote")
    array_of_quotes_instances = [
        Quote(
            text=quote.select_one(".text").text.strip(),
            author=quote.select_one(".author").text.strip(),
            tags=[tag.text for tag in quote.select(".tag")],
        )
        for quote in all_quotes
    ]
    return array_of_quotes_instances


def main(output_csv_path: str) -> None:
    last_page = get_last_page()
    result = [get_data_from_page(i) for i in range(1, last_page + 1)]
    return result


if __name__ == "__main__":
    print(main("quotes.csv"))
