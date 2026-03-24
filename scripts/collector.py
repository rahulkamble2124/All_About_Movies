import requests
import json
import os

# CONFIGURATION (Zero Cost)
OMDB_API_KEY = "eb48e89" # This is a common public key; get your own for free at omdbapi.com
WIKI_API_URL = "https://en.wikipedia.org/w/api.php"

def get_movie_data(title):
    # Fetching from OMDb (Hollywood/Bollywood compatible)
    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
    return requests.get(url).json()

def get_wiki_summary(search_term):
    # Fetching from Wikipedia (100% Free)
    params = {
        "action": "query", "format": "json", "prop": "extracts",
        "exintro": True, "explaintext": True, "titles": search_term
    }
    resp = requests.get(WIKI_API_URL, params=params).json()
    pages = resp.get("query", {}).get("pages", {})
    for page_id in pages:
        return pages[page_id].get("extract", "No biography available.")
    return "No info found."

def run_sync():
    # Example: List of movies to track (You can automate this list later)
    movie_titles = ["Pathaan", "Avatar: The Way of Water", "Jawan", "Deadpool & Wolverine"]
    database = []

    for title in movie_titles:
        data = get_movie_data(title)
        if data.get("Response") == "True":
            # Add Director & Actor Bio from Wiki
            data["Director_Bio"] = get_wiki_summary(data["Director"])
            database.append(data)
            print(f"Synced: {title}")

    with open('data/movies.json', 'w') as f:
        json.dump(database, f, indent=4)

if __name__ == "__main__":
    run_sync()
