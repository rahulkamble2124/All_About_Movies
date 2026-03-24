import requests
import json
import os
import time

def get_data():
    movie_list = []
    omdb_key = '52d4ec2e' # <--- DOUBLE CHECK THIS KEY
    
    # 1. TV SHOWS (Reliable TVMaze API)
    print("Step 1: Fetching TV Shows...")
    popular_shows = ["Breaking Bad", "Stranger Things", "Dark", "The Boys", "Sacred Games", "Mirzapur", "Money Heist", "The Mandalorian"]
    for show_name in popular_shows:
        try:
            res = requests.get(f"https://api.tvmaze.com/singlesearch/shows?q={show_name}")
            if res.status_code == 200:
                s = res.json()
                movie_list.append({
                    "title": s.get('name'),
                    "summary": f"TV Series | Rating: {s.get('rating', {}).get('average', 'N/A')}",
                    "link": s.get('url'),
                    "category": "TV Show",
                    "image": s.get('image', {}).get('medium', '') if s.get('image') else ""
                })
        except: continue

    # 2. MOVIES (OMDb Search - Multiple Keywords)
    print("Step 2: Fetching Movies from OMDb...")
    # We use very common words to ensure we get 100+ results
    keywords = ["Marvel", "Avengers", "Batman", "Spider", "Star Wars", "Action", "Bollywood", "2025", "2024", "Love"]
    
    for word in keywords:
        try:
            # We add &page=1 to be specific
            search_url = f"http://www.omdbapi.com/?s={word}&type=movie&apikey={omdb_key}"
            res = requests.get(search_url)
            data = res.json()
            
            if data.get('Response') == 'True':
                for m in data.get('Search', []):
                    # Avoid duplicates
                    if not any(item['title'] == m['Title'] for item in movie_list):
                        movie_list.append({
                            "title": m['Title'],
                            "summary": f"Movie | Released: {m['Year']}",
                            "link": f"https://www.imdb.com/title/{m['imdbID']}/",
                            "category": "Movie",
                            "image": m['Poster'] if (m['Poster'] and m['Poster'] != "N/A") else ""
                        })
            else:
                print(f"OMDb couldn't find movies for: {word} - Error: {data.get('Error')}")
            
            time.sleep(0.1) # Small delay to stay safe
        except Exception as e:
            print(f"Error fetching {word}: {e}")

    # 3. EMERGENCY FALLBACK (If OMDb fails, you still see these)
    if len(movie_list) < 10:
        print("Emergency Fallback Triggered!")
        movie_list.append({"title": "Inception", "summary": "A thief who steals corporate secrets...", "link": "#", "category": "Movie", "image": "https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_SX300.jpg"})
        movie_list.append({"title": "RRR", "summary": "A fearless revolutionary and an officer...", "link": "#", "category": "Movie", "image": "https://m.media-amazon.com/images/M/MV5BODUwNDNjYzctZDlhNC00MjgzLWI4NWUtYzI4ZTYyOTUzZGE2XkEyXkFqcGdeQXVyNTE0MzY3NjY@._V1_SX300.jpg"})

    # Final Save
    os.makedirs('data', exist_ok=True)
    with open('data/movies.json', 'w') as f:
        json.dump(movie_list, f, indent=4)
    
    print(f"SUCCESS: Total items collected: {len(movie_list)}")

if __name__ == "__main__":
    get_data()
