import requests
import json
import os
import time

def get_data():
    movie_list = []
    omdb_key = 'YOUR_OMDB_KEY_HERE'  # <--- MUST HAVE YOUR KEY
    
    # 1. TV SHOWS (Fetching from TVMaze Schedule)
    print("Fetching TV Shows...")
    # Fetching the last 2 days of shows to get a bigger list
    tv_url = "https://api.tvmaze.com/schedule/full" 
    try:
        tv_res = requests.get(tv_url)
        if tv_res.status_code == 200:
            all_shows = tv_res.json()[:50] # Get 50 shows
            for s in all_shows:
                movie_list.append({
                    "title": s.get('name', 'Unknown'),
                    "summary": "TV Series - Latest Episode",
                    "link": s.get('url', '#'),
                    "category": "TV Show",
                    "image": s.get('image', {}).get('medium', '') if s.get('image') else ""
                })
    except:
        print("TVMaze skipped")

    # 2. MOVIES (Fetching by Keywords for Volume)
    # Each keyword returns about 10 movies
    keywords = ["Marvel", "Avatar", "Pathaan", "Action", "Horror", "Comedy", "Bollywood", "Hollywood", "2026", "Disney"]
    
    print("Fetching Movies from OMDb...")
    for word in keywords:
        search_url = f"http://www.omdbapi.com/?s={word}&type=movie&apikey={omdb_key}"
        try:
            res = requests.get(search_url)
            data = res.json()
            if data.get('Response') == 'True':
                for m in data.get('Search', []):
                    # To avoid duplicates, check if title already exists
                    if not any(item['title'] == m['Title'] for item in movie_list):
                        movie_list.append({
                            "title": m['Title'],
                            "summary": f"Released: {m['Year']} | Click for details",
                            "link": f"https://www.imdb.com/title/{m['imdbID']}/",
                            "category": "Movie",
                            "image": m['Poster'] if m['Poster'] != "N/A" else ""
                        })
            # Respect API speed limits
            time.sleep(0.2) 
        except:
            continue

    # Save everything
    os.makedirs('data', exist_ok=True)
    with open('data/movies.json', 'w') as f:
        json.dump(movie_list, f, indent=4)
    
    print(f"Success! {len(movie_list)} items are now in your database.")

if __name__ == "__main__":
    get_data()
