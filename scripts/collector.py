import requests
import json
import os

def get_data():
    movie_list = []
    omdb_key = '52d4ec2e' # <--- Put your key from the email here

    # 1. Fetch Trending TV Shows from TVMaze (No Key Needed)
    print("Fetching TV Shows...")
    tv_response = requests.get("https://api.tvmaze.com/schedule?country=US")
    if tv_response.status_code == 200:
        shows = tv_response.json()[:10] # Get first 10 shows
        for item in shows:
            show = item['show']
            movie_list.append({
                "title": show['name'],
                "summary": f"TV Show - Status: {show['status']}",
                "link": show['url'],
                "category": "TV Show",
                "image": show['image']['medium'] if show['image'] else ""
            })

    # 2. Fetch Specific Movies from OMDb
    # We will search for a few hits to ensure the site looks full
    search_terms = ["Avatar", "Pathaan", "Jawan", "Batman", "Avengers"]
    print("Fetching Movies from OMDb...")
    for title in search_terms:
        omdb_url = f"http://www.omdbapi.com/?t={title}&apikey={omdb_key}"
        m_res = requests.get(omdb_url)
        if m_res.status_code == 200:
            m = m_res.json()
            if m.get('Response') == 'True':
                movie_list.append({
                    "title": m['Title'],
                    "summary": f"Rating: {m['imdbRating']} | {m['Plot'][:100]}...",
                    "link": f"https://www.imdb.com/title/{m['imdbID']}/",
                    "category": "Movie",
                    "image": m['Poster'] if m['Poster'] != "N/A" else ""
                })

    # Save to JSON
    os.makedirs('data', exist_ok=True)
    with open('data/movies.json', 'w') as f:
        json.dump(movie_list, f, indent=4)
    
    print(f"Success! Saved {len(movie_list)} items.")

if __name__ == "__main__":
    get_data()
