import requests
import json
import os
from datetime import datetime

# Get API key from GitHub Secrets
api_key = os.getenv("TMDB_API_KEY")

# Fetch latest movies
url = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}&with_genres=16,10751&language=en-US&sort_by=release_date.desc&page=1"
response = requests.get(url)
data = response.json()

# Save movies.json
with open("movies.json", "w", encoding="utf-8") as f:
    json.dump(data["results"], f, indent=2)

print(f"✅ Updated {len(data['results'])} movies at {datetime.now()}")
