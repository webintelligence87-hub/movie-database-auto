import os
import requests
import json
import time

# --- Settings ---
API_KEY = os.getenv("TMDB_API_KEY")  # from GitHub Secrets
OUTPUT_FILE = "movies.json"
MOVIES_PER_PAGE = 20
TOTAL_PAGES = 50  # 20 x 50 = 1000 movies
SLEEP_BETWEEN_REQUESTS = 0.25  # seconds (safe for API rate limit)
GENRES = "16,10751"  # Animation + Family
LANGUAGE = "en-US"
SORT_BY = "release_date.desc"

# --- Function to fetch a page ---
def fetch_movies(page):
    url = (
        f"https://api.themoviedb.org/3/discover/movie"
        f"?api_key={API_KEY}"
        f"&with_genres={GENRES}"
        f"&language={LANGUAGE}"
        f"&sort_by={SORT_BY}"
        f"&page={page}"
    )
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Error on page {page}: {e}")
        return []

# --- Main function ---
def update_movie_database():
    all_movies = []
    print("🚀 Starting movie update from TMDb...")

    for page in range(1, TOTAL_PAGES + 1):
        print(f"📄 Fetching page {page}/{TOTAL_PAGES}...")
        movies = fetch_movies(page)
        if not movies:
            print(f"⚠️ No movies found on page {page}, skipping...")
        all_movies.extend(movies)
        time.sleep(SLEEP_BETWEEN_REQUESTS)

    print(f"\n✅ Total movies fetched: {len(all_movies)}")

    # --- Save to JSON file ---
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(all_movies, f, ensure_ascii=False, indent=4)
        print(f"💾 Movies saved to {OUTPUT_FILE}")
    except Exception as e:
        print(f"❌ Error saving file: {e}")

if __name__ == "__main__":
    update_movie_database()
