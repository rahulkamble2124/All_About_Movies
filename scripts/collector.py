import requests
import json
import os
import time

def get_data():
    movie_list = []
    omdb_key = 'YOUR_OMDB_KEY_HERE' # <--- Ensure your key is here!
    
    # 1. TV SHOWS from TVMaze
    print("Fetching TV Shows...")
    try:
        # Fetching specific popular shows to ensure good posters
        popular_shows = ["Breaking Bad", "Stranger Things", "Dark", "The Boys", "Sacred Games", "Mirzapur"]
        for show_name in popular_shows:
            res = requests.get(f"https://api.tvmaze.com/singlesearch/shows?q={show_name}")
            if res.status_code == 200:
                s = res.json()
                movie_list.append({
                    "title": s.get('name'),
                    "summary": f"Rating: {s.get('rating', {}).get('average', 'N/A')} | {s.get('type')}",
                    "link": s.get('url'),
                    "category": "TV Show",
                    "image": s.get('image', {}).get('medium', '') if s.get('image') else ""
                })
    except Exception as e:
        print(f"TVMaze Error: {e}")

    # 2. MOVIES from OMDb (Fixed for Poster data)
    keywords = ["Marvel", "Avengers", "Pathaan", "Batman", "Interstellar", "Joker", "Disney", "Action"]
    print("Fetching Movies from OMDb...")
    for word in keywords:
        search_url = f"http://www.omdbapi.com/?s={word}&type=movie&apikey={omdb_key}"
        try:
            res = requests.get(search_url)
            data = res.json()
            if data.get('Response') == 'True':
                for m in data.get('Search', []):
                    if not any(item['title'] == m['Title'] for item in movie_list):
                        # CRITICAL FIX: Mapping 'Poster' to 'image'
                        movie_list.append({
                            "title": m['Title'],
                            "summary": f"Year: {m['Year']} | Type: Movie",
                            "link": f"https://www.imdb.com/title/{m['imdbID']}/",
                            "category": "Movie",
                            "image": m['Poster'] if (m['Poster'] and m['Poster'] != "N/A") else ""
                        })
            time.sleep(0.2) 
        except Exception as e:
            print(f"OMDb Error: {e}")

    # Final Save
    os.makedirs('data', exist_ok=True)
    with open('data/movies.json', 'w') as f:
        json.dump(movie_list, f, indent=4)
    
    print(f"Success! {len(movie_list)} items synced with posters.")

if __name__ == "__main__":
    get_data()
