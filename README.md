# Instagram Image Scraper in 130 LOC

> An open source Instagram scraper

## Running locally

1. Clone the repo, rename `.example.env` to `.env`, and replace your IG username and password
2. Download [ChromeDriver](https://googlechromelabs.github.io/chrome-for-testing/#stable) and add it to your PATH
3. Run `pip install -r requirements.txt` to install dependencies
4. Run `python main.py` to run the scraper

## How it works

1. The scraper logs into your Instagram account
2. It navigates to the profile page of the user you want to scrape
3. Get the first 12 images and download them to a folder called `assets`
4. Each image has a unique ID, which can be used to navigate to the post page
4. Finally, create a `data.json` file with info about the instagram account scraped
