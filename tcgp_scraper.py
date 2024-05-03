"""A module including the class TCGPScraper, used for scraping TCGPlayer.com

Typical usage example:

    set_id = '23228'
    scraper = TCGPScraper()
    scraper.load_set(set_id)
"""

import asyncio
import httpx
import sys
import time
import re


class TCGPScraper:
    """A scraper for TCGPlayer.com sales information.

    Attributes:
        No public attributes
    """

    def __init__(self, set_id: str = None) -> None:
        self._set_id = None
        self._cards = None
        self._card_ids = None
        if set_id:
            self.load_set(set_id)

    async def __payload_generator(self, n: int) -> dict:
        """Generates a payload for a given offset.

        Args:
            n: An integer for the current offset.

        Returns:
            A JSON payload for a POST request to
                https://mpapi.tcgplayer.com/v2/product/{id}/latestsales
        """
        payload = {
            "listingType": "All",
            "offset": n * 25,
            "limit": 25,
            "time": round(time.time() * 1000),
        }
        return payload

    async def __request_cards(self) -> None:
        """GETs and stores JSON of card entries from TCGPlayer for self._set_id into self._cards.
        """  # noqa: E501
        try:
            response = httpx.get(
                'https://infinite-api.tcgplayer.com/priceguide/'
                f'set/{self._set_id}/cards/?rows=5000',
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            print(
                f'HTTP Exception for {exc.request.url} - {exc}',
                file=sys.stderr,
            )
            sys.exit(1)
        else:
            self._cards = response.json()

    async def __extract_card_ids(self) -> None:
        """Extracts the card_ids from _cards."""
        unique_ids = set()
        try:
            for card in self._cards['result']:
                unique_ids.add(str(card['productID']))
        except Exception as exc:
            print(
                f'Unexpected error in __extract_card_ids - {exc}',
                file=sys.stderr,
            )
            sys.exit(1)
        else:
            self._card_ids = list(unique_ids)

    async def load_set(self, set_id: str) -> None:
        """Loads a set_id and requests and extracts cards from that set."""
        self._set_id = set_id
        await self.__request_cards()
        await self.__extract_card_ids()

    async def get_card_sales(self, card_id: str, end: int = None) -> list:
        """Gets all card sales for a given card id and ending offset
        Args:
            card_id: A card_id string.

        Returns:
            A list of sales JSON. For example:

            [
                {
                    'condition': 'Near Mint',
                    'variant': 'Reverse Holofoil',
                    'language': 'English',
                    'quantity': 1,
                    'title': 'Altaria',
                    'listingType': 'ListingWithoutPhotos',
                    'customListingId': '0',
                    'purchasePrice': 0.24,
                    'shippingPrice': 0.0,
                    'orderDate': '2024-04-24T01:53:25.003+00:00'
                },
            ]

        Raises:
            ValueError: A card_id with invalid format was passed as an argument.
        """  # noqa: E501
        # Check for a valid card_id
        if not re.match(r'^\d{6}$', card_id):
            raise ValueError(
                'A card_id with invalid format was passed '
                f'as an argument - {card_id}'
            )

        offset = 1
        next_page = True
        sales = []
        api_url = (
            f'https://mpapi.tcgplayer.com/v2/product/{card_id}/latestsales?mpfev=2399'  # noqa: E501
        )

        async with httpx.AsyncClient() as client:
            while next_page:
                payload = await self.__payload_generator(offset)
                try:
                    response = await client.post(api_url, json=payload)
                    response.raise_for_status()
                except httpx.HTTPError as exc:
                    print(
                        f'HTTP Exception for {exc.request.url} - {exc}',
                        file=sys.stderr,
                    )
                else:
                    data = response.json()
                    sales.extend(data['data'])
                    if data['nextPage'] == 'Yes' and offset != end:
                        time.sleep(0.1)
                        offset += 1
                    else:
                        next_page = False
        return sales

    def get_cards(self) -> dict:
        """Getter for self._cards."""
        return self._cards

    def get_card_ids(self) -> dict:
        """Getter for self._card_ids."""
        return self._card_ids


async def main():
    set_id = '23228'
    scraper = TCGPScraper()
    await scraper.load_set(set_id)
    cards = scraper.get_card_ids()
    sales = await scraper.get_card_sales(cards[0], end=2)
    print(sales)


if __name__ == '__main__':
    asyncio.run(main())
