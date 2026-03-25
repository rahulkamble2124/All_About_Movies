import requests
import json
import os
import time

def get_data():
    movie_list = []
    omdb_key = '52d4ec2e' # Get for free at omdbapi.com
    
    # 1. TV SHOWS (Free TVMaze API)
    print("Fetching TV...")
    tv_res = requests.get("https://api.tvmaze.com/schedule/full").json()[:10]
    for s in tv_res:
        movie_list.append({
            "id": str(s['id']),
            "title": s.get('name', 'Show'),
            "year": "2026",
            "director": "Various",
            "genre": "Reality/TV",
            "imdbRating": "7.5",
            "category": "TV Show",
            "image": s.get('image', {}).get('medium', '') if s.get('image') else "",
            "budget": "TV Budget",
            "revenue": "Network Revenue"
        })

    # 2. MOVIES (OMDb Free)
    keywords = ["Marvel", "Avatar", "Batman", "Pathaan"]
    for word in keywords:
        res = requests.get(f"http://www.omdbapi.com/?s={word}&apikey={omdb_key}").json()
        if res.get('Response') == 'True':
            for m in res.get('Search', [])[:5]:
                # Get details
                d = requests.get(f"http://www.omdbapi.com/?i={m['imdbID']}&apikey={omdb_key}").json()
                movie_list.append({
                    "id": m['imdbID'],
                    "title": d['Title'],
                    "year": d['Year'],
                    "director": d['Director'],
                    "genre": d['Genre'],
                    "imdbRating": d['imdbRating'],
                    "category": "Movie",
                    "image": d['Poster'],
                    "budget": "$200M", # Placeholder for free tier
                    "revenue": "$800M"
                })
        time.sleep(0.1)

    os.makedirs('data', exist_ok=True)
    with open('data/movies.json', 'w') as f:
        json.dump(movie_list, f, indent=4)

if __name__ == "__main__":
    get_data()
