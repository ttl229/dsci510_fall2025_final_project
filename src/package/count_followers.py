import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Function to get the follower count for a username from social media site
"""
This is function version 1 - does not work for Instagram 
- but could work for other social media sites -
- keeping this in the project file for now -
"""
def get_follower_count(username, url) -> int:
    number_of_followers = None  # Default Value
    full_url = f"{url}/{username}"
    response = requests.get(full_url)
    html_content = response.text

    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        followers_tag = soup.find("strong", {"title": "Followers", "data-e2e": "followers-count"}) # Searches for the Followers Icon

        if not followers_tag:
            print(f"Could not find followers location for {username}")
            return None

        result = followers_tag.get_text(strip=True)

        if not result:
            print(f"Could not load follower count for {username}")
            return None

        # Normalize follower string for abbreviated number format
        if "K" in result:
            number_of_followers = int(float(result.replace("k", "")) * 1000)

        elif "M" in result:
            number_of_followers = int(float(result.replace("m", "")) * 1_000_000)

        else:
            number_of_followers = int(re.sub(r"\D", "", result)) # Converts string into number

    except Exception as e:
        print(f"Error: {e}")

    return number_of_followers



# Alternate code to extract Instagram followers using Selenium
def get_ig_followers(username)-> int:
    number_of_followers = None # Sets default value to None
    url = f"https://www.instagram.com/{username}"

    # Use Chrome Driver (headless = true no window pops up)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get(url)
    time.sleep(3) # Wait for javascript to load

    html = driver.page_source

    try:
        soup = BeautifulSoup(html, 'html.parser')

        # Extracts follower count from meta tag: "description"
        description = soup.find("meta", attrs={"name": "description"})

        if not description:
            print(f"Could not find followers for {username}")
            return None

        followers_tag= description["content"]
        result = followers_tag.split("Followers")[0].split()[-1]

        if not result:
            print(f"Could not load follower count for {username}")
            return None

        # Normalize follower string for abbreviated number format
        cleaned_result = re.sub(r'[,.]', "", result)

        if "K" in cleaned_result:
            number_of_followers = int(float(cleaned_result.replace("K", "")) * 1000)

        elif "M" in cleaned_result:
            number_of_followers = int(float(cleaned_result.replace("M", "")) * 1_000_000)

        else:
            number_of_followers = int(cleaned_result)

        driver.quit()
        print(f"Followers: {number_of_followers}")

    except Exception as e:
        print(f"Error extracting followers: {e}")

    return number_of_followers



