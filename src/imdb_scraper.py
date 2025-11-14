import requests
from bs4 import BeautifulSoup
import json
import re

def clean_text(cell):
    return cell.get_text(strip=True) if cell else ""

def imdb_title_scraper(url:str) -> str:
    output_file = "imdb_titles.json"
    actor_name = input("Actor name: ")
    credits = [] # empty dictionary to store actor credits in

    # Set a User-Agent to mimic a real browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to URL: {e}")
        return None

    soup = BeautifulSoup(response.content, "html.parser")
    print(f"Extracting {actor_name}'s previous titles from {url}")

    # Locate the Actor Section to identify Previous Titles
    actor_heading = soup.find('h3', string=lambda x: x and 'Actor' in x)
    if not actor_heading:
        print(f"No acting credits found for {actor_name}")
        return None

    previous_header = (
        actor_heading.find_next('li', string=lambda x: x and 'Previous' in x)
    )
    if not previous_header:
        print(f"No previous titles found for {actor_name}")

    previous_titles_list = previous_header.find_next('ul')
    previous_titles = previous_titles_list.find_all('li')

    for item in previous_titles:
        title_cell = item.find(class_="ipc-metadata-list-summary-item__t")
        title = clean_text(title_cell)

        role_cell = item.find(class_="ipc-btn--not-interactable")
        role = clean_text(role_cell)

        credits.append({"title": title, "role": role,}) # Adds title and role to dictionary

    with open(output_file, 'w', encoding="utf-8") as f:
        json.dump(credits, f, indent=4)

    print(len(credits), f" previous titles extracted for {actor_name} and saved to file:{output_file}")

    return output_file

