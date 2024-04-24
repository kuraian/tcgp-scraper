# tcgplayer scraper

tcgp_scraper.py is a script implementing undetected_chromedriver and sends POST requests using selenium-requests to scrape financial data off tcgplayer

## install dependencies:

it uses undetected-chromedriver and seleniumrequests, so installation goes:
```default
pip install undetected-chromedriver
```
```default
pip install selenium-requests
```

### how to use:
* either run the script as is (change the id variable for whatever set id you want) or import the functions into your own script
* the data will be stored in ./sets/{set_id}

example
```python
import tcgp_scraper as tcgp


# set IDs can be found here: https://mpapi.tcgplayer.com/v2/Catalog/SetNames
set_id = 1

cards = tcgp.get_cards(set_id)
card_ids = get_card_ids(set_id, cards)

for card_id in card_ids:
  get_card_sales(set_id, card_id)
```

## todo:
* implement threading + proxies, or make it deployable, or both
* build a flask frontend?
* change order of parameters in functions (lazy)
* change directory building, or allow user to set it by parameter (mega lazy)

## issues:
* not conventionally deployable using selenium-grid (CRITICAL)
* not currently detected, but needs to be run through proxies or distributed (see above)
* expensive (selenium.....)
