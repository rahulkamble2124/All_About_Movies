import wikipediaapi
import json
import os

def get_movies():
    wiki = wikipediaapi.Wikipedia(
        language='en',
        extract_format=wikipediaapi.ExtractFormat.WIKI,
        user_agent="CinemaHub/1.0 (rahulkamble2124@example.com)"
    )

    movie_list = []
    
    # Target Categories
    categories = [
        {"name": "Category:2020s_Hindi-language_films", "label": "Bollywood"},
        {"name": "Category:2020s_English-language_films", "label": "Hollywood"}
    ]

    for cat_info in categories:
        cat_page = wiki.page(cat_info["name"])
        if cat_page.exists():
            count = 0
            for page in cat_page.categorymembers.values():
                if count >= 15: break
                if page.ns == wikipediaapi.Namespace.MAIN:
                    movie_list.append({
                        "title": page.title,
                        "summary": page.summary[:200] + "...",
                        "link": page.fullurl,
                        "category": cat_info["label"]
                    })
                    count += 1

    # FALLBACK: If Wikipedia fails, add these manually so the site isn't empty
    if not movie_list:
        movie_list = [
            {"title": "Avatar: The Way of Water", "summary": "Jake Sully lives with his newfound family formed on the extrasolar moon Pandora.", "link": "https://en.wikipedia.org/wiki/Avatar:_The_Way_of_Water", "category": "Hollywood"},
            {"title": "Pathaan", "summary": "An exiled RAW agent is assigned to take down a private terrorist organization.", "link": "https://en.wikipedia.org/wiki/Pathaan_(film)", "category": "Bollywood"}
        ]

    os.makedirs('data', exist_ok=True)
    with open('data/movies.json', 'w') as f:
        json.dump(movie_list, f, indent=4)
    
    print(f"Total movies saved: {len(movie_list)}")

if __name__ == "__main__":
    get_movies()
