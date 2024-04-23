import requests
import json
import random
import time
import os
import config

API_KEY = config.scrapeops_key


def payload_generator(n):
    """Generates a payload for a given offset
    Args:
        n: the current offset, starts at 1
    Returns:
        returns a JSON payload for a POST request to
            https://mpapi.tcgplayer.com/v2/product/<product_id>/pricepoints
    """

    payload = {
        "limit": 25,
        "listingType": 1,
        "offset": n*25,
        "time": round(time.time() * 1000)
    }
    return payload


def get_cards(id):
    """Gets a JSON of card entries from tcgplayer for a set_id, writes them to a file,
        and returns a dict for those cards
    Args:
        id: a set's id number
    Returns:
        returns a dict of cards
    todo:
        implement proxies or distribution
    """

    response = requests.get(
        f"http://headers.scrapeops.io/v1/user-agents?api_key={API_KEY}")
    results_list = response.json()["result"]
    random_index = random.randint(0, len(results_list) - 1)
    random_agent = results_list[random_index]

    response = requests.get(
        f"https://infinite-api.tcgplayer.com/priceguide/set/{id}/cards/?rows=5000")

    path = f"sets/{id}"
    if not os.path.isdir(path):
        os.mkdir(path)
    with open(path + "/cards.json", "w") as f:
        cards = json.loads(response.text)
        f.write(json.dumps(cards, indent=4))
    return cards


def main():
    # its easier to just lookup the set ID manually than automate it
    # https://mpapi.tcgplayer.com/v2/Catalog/SetNames
    id = 23381
    cards = get_cards(id)
    print(cards["count"])


if __name__ == "__main__":
    main()
