import requests
import json
import random
import time
import os
import config

API_KEY = config.scrapeops_key


def generate_agent():
    response = requests.get(
        f"http://headers.scrapeops.io/v1/user-agents?api_key={API_KEY}")
    results_list = response.json()["result"]
    random_index = random.randint(0, len(results_list) - 1)
    random_agent = results_list[random_index]

    return random_agent


def get_cards(set_id):
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
        f"https://infinite-api.tcgplayer.com/priceguide/set/{set_id}/cards/?rows=5000",)

    path = f"sets/{set_id}"
    if not os.path.isdir(path):
        os.mkdir(path)
    with open(path + "/cards.json", "w") as f:
        cards = response.json()
        f.write(json.dumps(cards, indent=4))
    return cards


def payload_generator(n):
    """Generates a payload for a given offset
    Args:
        n: the current offset, starts at 1
    Returns:
        A JSON payload for a POST request to
            https://mpapi.tcgplayer.com/v2/product/{id}/latestsales
    """

    payload = {
        "listingType": "All",
        "offset": n*25,
        "limit": 25,
        "time": round(time.time() * 1000)
    }
    return payload


def get_card_sales(set_id, card_id):
    """Gets all card sales for a given card id
    Args:
        set_id
        card_id
    Returns:
        A list of sales
    """

    offset = 1
    next_page = True
    sales = []

    while next_page:
        payload = payload_generator(offset)
        response = requests.post(
            f"https://mpapi.tcgplayer.com/v2/product/{card_id}/latestsales?mpfev=2372", json=payload)
        response = response.json()
        sales.extend(response["data"])
        if not response["nextPage"] == "Yes":
            next_page = False
        else:
            time.sleep(random.triangular(1.2, 2.3))
            offset += 1

    path = f"sets/{set_id}"
    if not os.path.isdir(path):
        os.mkdir(path)
    with open(f"{path}/{card_id}.json", "w") as f:
        f.write(json.dumps({"sales": sales}, indent=4))
    return sales


def main():
    # its easier to just lookup the set ID manually than automate it
    # https://mpapi.tcgplayer.com/v2/Catalog/SetNames
    set_id = 23381

    cards = get_cards(set_id)
    card_ids = set()
    for card in cards["result"]:
        card_ids.add(card["productID"])
    card_ids = list(card_ids)
    for card_id in card_ids:
        get_card_sales(set_id, card_id)


if __name__ == "__main__":
    main()
