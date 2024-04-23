import undetected_chromedriver as uc
import requests
import random
import time
import config

API_KEY = config.scrapeops_key
response = requests.get(
    f"http://headers.scrapeops.io/v1/user-agents?api_key={API_KEY}")
results_list = response.json()["result"]
random_index = random.randint(0, len(results_list) - 1)
random_agent = results_list[random_index]

options = uc.ChromeOptions()
options.add_argument(f"--user-agent={random_agent}")
driver = uc.Chrome(options=options)

driver.get("https://ibd.supplynation.org.au/public/s/search-results")
driver.quit()
