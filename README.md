# tcgplayer scraper

tcgp_scraper.py is a module implementing httpx for scraping financial data off tcgplayer

## install dependencies:

it uses httpx so:

```default
pip install httpx
```

### how to use:

- either run the script as is (change the id variable for whatever set id you want) or import the functions into your own script
- the data will be stored in ./sets/{set_id}

example

```python
import tcgp_scraper as tcgp


async def main():
    set_id = '23228'
    scraper = tcgp.TCGPScraper()
    await scraper.load_set(set_id)
    cards = scraper.get_card_ids()
    sales = await scraper.get_card_sales(cards[0], end=2)  # For example's sake, gets the 50 most recent sales of a single card.
    print(sales)


if __name__ == '__main__':
    asyncio.run(main())
```

## todo:

- implement threading + proxies
- build and deploy using docker + k8s
- build a flask app
- r/w to mongodb

## issues:

- not currently detected, but should be run through proxies (see above)
