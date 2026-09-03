import requests
from bs4 import BeautifulSoup
import os
import json
from datetime import datetime, timezone


TGJU_URL = "https://www.tgju.org/profile/price_dollar_rl"

GIST_ID = os.environ["GIST_ID"]
GITHUB_TOKEN = os.environ["MY_TOKEN"]


def get_dollar_price():

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/140.0 Safari/537.36"
        )
    }

    response = requests.get(
        TGJU_URL,
        headers=headers,
        timeout=15
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    element = soup.select_one(".price")

    if not element:
        raise Exception(
            "Dollar price element not found"
        )

    price = element.get_text(
        strip=True
    )

    return price


def update_gist(price):

    url = f"https://api.github.com/gists/{GIST_ID}"

    headers = {
        "Authorization": f"Bearer {MY_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    data = {
        "files": {
            "dollar.json": {
                "content": json.dumps(
                    {
                        "success": True,
                        "price": price,
                        "updated_at": datetime.now(
                            timezone.utc
                        ).isoformat()
                    },
                    ensure_ascii=False,
                    indent=2
                )
            }
        }
    }

    response = requests.patch(
        url,
        headers=headers,
        json=data,
        timeout=15
    )

    response.raise_for_status()


def main():

    price = get_dollar_price()

    print("Dollar price:", price)

    update_gist(price)

    print("Gist updated successfully.")


if __name__ == "__main__":
    main()
