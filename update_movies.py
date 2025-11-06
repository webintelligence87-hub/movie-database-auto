import requests, json, datetime, os

API_KEY = os.environ.get('TMDB_API_KEY')
if not API_KEY:
    raise SystemExit("Error: TMDB_API_KEY not found")

url = f"https://api.themoviedb.org/3/discover/movie?api_key={be0215624ce3e4b3f121e773d936751d}&with_genres=16,10751&language=en-US&sort_by=release_date.desc&page=1"

res = requests.get(url)
data = res.json()

movies = []
for m in data.get("results", []):
    movies.append({
        "id": m["id"],
        "title": m["title"],
        "release_date": m["release_date"],
        "rating": m["vote_average"],
        "poster": f"https://image.tmdb.org/t/p/w500{m['poster_path']}" if m.get("poster_path") else None,
        "timestamp": datetime.datetime.utcnow().isoformat()
    })

with open("movies.json", "w", encoding="utf-8") as f:
    json.dump(movies, f, indent=2)

print(f"✅ Updated {len(movies)} movies successfully.")
