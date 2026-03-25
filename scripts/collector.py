import requests
import json
import os
import time

def get_data():
    movie_list = []
    omdb_key = 'YOUR_OMDB_KEY_HERE' # <--- ENTER YOUR KEY HERE
    
    # We use these queries to fill your "By Studio" and "By Genre" sections
    search_queries = [
        {"q": "Marvel", "cat": "Marvel Studios"},
        {"q": "Avengers", "cat": "Marvel Studios"},
        {"q": "Batman", "cat": "DC Universe"},
        {"q": "Action", "cat": "Action"},
        {"q": "Bollywood", "cat": "Bollywood"},
        {"q": "Christopher Nolan", "cat": "Director's Cut"},
    ]

    print("🚀 Collecting Detailed Data...")

    for item in search_queries:
        try:
            url = f"http://www.omdbapi.com/?s={item['q']}&apikey={omdb_key}"
            res = requests.get(url).json()
            
            if res.get('Response') == 'True':
                for short_m in res.get('Search', [])[:6]:
                    # Fetching full details for each specific movie ID
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
                            "imdbRating": m.get('imdbRating', '0.0'),
                            "category": item['cat'],
                            "image": m['Poster'] if (m['Poster'] and m['Poster'] != "N/A") else "",
                            "trailer_query": f"{m['Title']} {m['Year']} official trailer"
                        })
            time.sleep(0.1) # Prevents the API from blocking us
        except Exception as e:
            print(f"Error: {e}")

    os.makedirs('data', exist_ok=True)
    with open('data/movies.json', 'w') as f:
        json.dump(movie_list, f, indent=4)
    print(f"✅ Saved {len(movie_list)} movies.")

if __name__ == "__main__":
    get_data()
