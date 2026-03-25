import requests
import json
import os
import time

def get_data():
    movie_list = []
    omdb_key = 'YOUR_OMDB_KEY_HERE' # <--- ENTER YOUR KEY
    
    # Categories to search for to fill the "Studios" and "Genres" headings
    search_queries = [
        {"q": "Marvel", "cat": "Marvel Studios"},
        {"q": "Avengers", "cat": "Marvel Studios"},
        {"q": "Batman", "cat": "DC Universe"},
        {"q": "Action", "cat": "Action"},
        {"q": "Horror", "cat": "Horror"},
        {"q": "Bollywood", "cat": "Bollywood"},
        {"q": "Christopher Nolan", "cat": "Director's Cut"},
    ]

    print("🚀 Starting Mega-Collection...")

    for item in search_queries:
        try:
            url = f"http://www.omdbapi.com/?s={item['q']}&apikey={omdb_key}"
            res = requests.get(url).json()
            
            if res.get('Response') == 'True':
                for short_m in res.get('Search', [])[:5]: # Get top 5 per category
                    # Get FULL details for the separate movie page
                    detail_url = f"http://www.omdbapi.com/?i={short_m['imdbID']}&apikey={omdb_key}"
                    m = requests.get(detail_url).json()
                    
                    if m.get('Response') == 'True' and not any(x['id'] == m['imdbID'] for x in movie_list):
                        movie_list.append({
                            "id": m['imdbID'],
                            "title": m['Title'],
                            "year": m['Year'],
                            "director": m.get('Director', 'N/A'),
                            "actors": m.get('Actors', 'N/A'),
                            "genre": m.get('Genre', 'N/A'),
                            "plot": m.get('Plot', 'No plot available.'),
                            "category": item['cat'],
                            "image": m['Poster'] if (m['Poster'] and m['Poster'] != "N/A") else "",
                            # Create a clean YouTube search link
                            "trailer_query": f"{m['Title']} {m['Year']} official trailer"
                        })
            time.sleep(0.1)
        except Exception as e:
            print(f"Error on {item['q']}: {e}")

    # Save to data folder
    os.makedirs('data', exist_ok=True)
    with open('data/movies.json', 'w') as f:
        json.dump(movie_list, f, indent=4)
    
    print(f"✅ Success! {len(movie_list)} detailed movies saved.")

if __name__ == "__main__":
    get_data()
