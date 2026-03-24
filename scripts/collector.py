import requests
import json
import os

# CONFIGURATION
OMDB_KEY = "eb48e89" # Free 1000/day limit. Get your own at omdbapi.com
WIKI_URL = "https://en.wikipedia.org/api/rest_v1/page/summary/"

def fetch_wiki_bio(name):
    try:
        # Wikipedia REST API is 100% free and commercial-friendly
        res = requests.get(WIKI_URL + name.replace(" ", "_")).json()
        return {"bio": res.get("extract", "No bio found."), "source": res.get("content_urls", {}).get("desktop", {}).get("page", "")}
    except:
        return {"bio": "Biography pending update.", "source": "https://wikipedia.org"}

def update_db():
    # Example starting list - the script will gather data for these
    movies_to_track = ["Jawan", "Avengers: Endgame", "Pathaan", "Inception"]
    final_db = []

    for title in movies_to_track:
        m = requests.get(f"http://www.omdbapi.com/?t={title}&apikey={OMDB_KEY}").json()
        if m.get("Response") == "True":
            # Adding Director & Actor Bios
            m["Director_Info"] = fetch_wiki_bio(m["Director"])
            m["Actor_Bios"] = [fetch_wiki_bio(name) for name in m["Actors"].split(", ")]
            final_db.append(m)
    
    # Save into the data folder
    os.makedirs('data', exist_ok=True)
    with open('data/movies.json', 'w') as f:
        json.dump(final_db, f, indent=4)

if __name__ == "__main__":
    update_db()
