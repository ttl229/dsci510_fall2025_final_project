import requests
import json

def tmdb_get_release_date(title, url):
    search_item = title
    key_file = "../keys/tmdb_key.txt"

    with open(key_file, "r") as f:  # Reads API key
        key = f.readline().strip()
        print(f"Using key from {key_file}")

    search_url = f"https://api.themoviedb.org/3/search/movie"
    params = {'api_key': key, 'query': title}

    response = requests.get(url, params=params)
    title_result = response.json()

    if not title_result:
        print("No such title found.")
        return None

    title_id = title_result['results'][0]['id']

    details_url = f"https://api.themoviedb.org/3/movie/{title_id}?api_key={key}"
    response = requests.get(details_url, params=params)

    title_details = response.json()
    release_date = title_details.get(class_='release_date')

    if release_date:
        print(f"Release date: {release_date}")
        return release_date

    else:
        print("No release date found")
        return None


title = "Frankenstein"
url = "https://www.themoviedb.org/movie/1062722-frankenstein?language=en-US"
tmdb_get_release_date(title, url)

