import requests
from bs4 import BeautifulSoup
import json


def clean_text(cell):
    return cell.get_text(strip=True) if cell else ""

def imdb_title_scraper(url:str) -> str:
    actor_name = input("Actor name: ")
    output_file = f"{actor_name}_imdb_titles.json"
    credits = [] # empty list to store actor credits in

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

    # 1. Locate the ACTOR section on page
    actor_heading = soup.find(
        "h3",
        class_="ipc-title__text",
        string=lambda x: x and "Actor" in x or "Actress" in x
    )

    if not actor_heading:
        print(f"No acting credits found for {actor_name}")
        return

    # 2. Locate PREVIOUS credits under ACTOR heading
    previous_header = actor_heading.find_next(lambda tag: tag.name == "li" and "Previous" in tag.get_text(strip=True))

    if not previous_header:
        print(f"No previous titles found for {actor_name}")
        return

    # 3. Check to see if the credits page extends past first page
    # see_all_link = previous_header.find_next("a", class_="ipc-see-more__text")

    # if see_all_link:
    #     titles_url = "https://www.imdb.com" + see_all_link["href"]
    #
    #     response = requests.get(titles_url, headers=headers)
    #     response.raise_for_status()
    #     soup = BeautifulSoup(response.content, "html.parser")
    #     print(f"Extracting all previous acting title and roles for {actor_name}")

        # Extracts all titles under the 'See All' list
        # title_items = soup.find_all("li", class_="ipc-metadata-list-summary-item")

    # 4. Locate first TITLE under PREVIOUS section
    titles_list = previous_header.find_next("ul")
    title_items = titles_list.find_all("li", recursive = False)

    # 5. Extract title and role for actor
    for item in title_items:
        title_cell = item.find("a", class_="ipc-metadata-list-summary-item__t")
        if title_cell is None:
            continue # Skip rows containing other data
        title = clean_text(title_cell)

        role_cell = item.find("span", class_="ipc-btn--not-interactable")
        role = clean_text(role_cell) if role_cell else ""

        credits.append({"title": title, "role": role,})  # Adds title and role to credits list


    with open(output_file, 'w', encoding="utf-8") as f:
        json.dump(credits, f, indent=4)

    print(len(credits), f" previous titles extracted for {actor_name} and saved to file:{output_file}")

    return output_file

