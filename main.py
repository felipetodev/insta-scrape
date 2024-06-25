import time
import requests
import os
import json
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from typing import List

load_dotenv()
IG_USERNAME = os.getenv("IG_USERNAME")
IG_PASSWORD = os.getenv("IG_PASSWORD")
DRIVER_PATH = os.getenv("CHROMEDRIVER")

service = Service(DRIVER_PATH)
driver = webdriver.Chrome(service=service)

driver.get('https://www.instagram.com')
time.sleep(1)

username = driver.find_element(By.NAME, 'username').send_keys(IG_USERNAME)
password = driver.find_element(By.NAME, 'password').send_keys(IG_PASSWORD)

## button type submit
login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
login_button.click()
time.sleep(4)

# Remove modal - save login info
modal_button = driver.find_element(By.CSS_SELECTOR, 'div[role="button"]')
modal_button.click()
time.sleep(2)

# Remove modal - notifications
modal_dialog = driver.find_element(By.CSS_SELECTOR, 'div[role="dialog"]')
modal_last_button = modal_dialog.find_elements(By.CSS_SELECTOR, 'button')[-1]
modal_last_button.click()

def download_image(url: str, prefix: str, store: str, index: int):
  response = requests.get(url)
  image_name = f"{str(index).rjust(2, '0')}_{prefix}.jpg"
  image_path = f"assets/{store}/{image_name}"

  if not os.path.exists(f"assets/{store}"):
    os.makedirs(f"assets/{store}")

  if response.status_code == 200:
    with open(image_path, 'wb') as file:
      file.write(response.content)
    print(f"{image_name} was downloaded successfully")
  else:
    print(f"Error downloading {image_name} 🤐")

def scrape_ig(stores: List[str]):
  stores_data_scrapped = []

  for scrape_counter, coffee in enumerate(stores, start=1):
    print(f"Scrapping {scrape_counter} of {len(stores)}")
    time.sleep(1)

    # Go to search bar icon (aside navigation)
    search_button = driver.find_elements(By.CSS_SELECTOR, 'a[role="link"]')[2]
    search_button.click()
    time.sleep(2)

    # go to the search input
    search_input = driver.find_element(By.CSS_SELECTOR, 'input[type="text"]')
    search_input.clear()
    search_input.click()
    search_input.send_keys(coffee)
    time.sleep(2)

    # go to the IG account "a[role='link'][href='/cafeblackmamba/']"
    instagram_result = driver.find_element(By.CSS_SELECTOR, 'a[href="/{}/"]'.format(coffee))
    instagram_result.click()
    time.sleep(2)

    # get store name, media count, followers and following
    account_numbers = driver.find_element(By.CSS_SELECTOR, 'header>section:nth-child(3)').text.split('\n')
    follower_count = driver.find_element(By.CSS_SELECTOR, 'span[title]').get_attribute('title')
    account_details = driver.find_element(By.CSS_SELECTOR, 'header>section:nth-child(4)').text.split('\n')

    ig_account_info = {
      "username": coffee,
      "full_name": account_details[0],
      "category": account_details[1],
      "media_count": int(account_numbers[0].split(' ')[0]),
      "follower_count": int(follower_count.replace('.', '')),
      "following_count": int(account_numbers[2].split(' ')[0])
    }

    stores_data_scrapped.append(ig_account_info)

    # get all images, avoid first image (avatar)
    post_images = driver.find_elements(By.CSS_SELECTOR, 'a img')[1:]

    # get posts url links which href starts with "/p/"
    posts_images_id = driver.find_elements(By.CSS_SELECTOR, 'a[href^="/p/"]') # "/p/C73BAovObJa/"

    for idx, image in enumerate(post_images, start=1):
      image_url = image.get_attribute('src')
      try:
        image_id = posts_images_id[idx-1].get_attribute('href').split('/')[-2]
      except Exception:
        image_id = coffee

      download_image(
        url=image_url,
        prefix=image_id,
        store=coffee,
        index=idx
      )

    print(f"{coffee} scrapped successfully ☕✅")

  with open('data.json', 'w', encoding='utf-8') as file:
    json.dump(stores_data_scrapped, file, indent=2, ensure_ascii=False)

  driver.quit()

coffee_stores = [
  #"cafeblackmamba",
  #"melbournecafe",
  #"cafelocalvillarrica",
  #"domestico.cafe",
  "area.stgo"
]

scrape_ig(coffee_stores)
