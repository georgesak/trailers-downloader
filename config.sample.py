# --- CONFIGURATION ---
TMDB_API_KEY = ''  # Paste your TMDB API key inside the quotes
OUTPUT_FOLDER = r''     # Path where the trailers will be downloaded
LIMIT = 10      # Number of trailers to download
MAX_WORKERS = 2 # Number of parallel downloads
HISTORY_FILE = 'downloaded_history.txt'  # File to store downloaded trailer history

# Only movies containing AT LEAST one of these genres will be downloaded.
# Set to 1 to include, 0 to exclude
ALLOWED_GENRES = {
    "Action": 1, 
    "Adventure": 1, 
    "Animation": 1, 
    "Comedy": 1, 
    "Crime": 1, 
    "Documentary": 1, 
    "Drama": 1, 
    "Family": 1, 
    "Fantasy": 1, 
    "History": 1, 
    "Horror": 1, 
    "Music": 1, 
    "Mystery": 1, 
    "Romance": 1, 
    "Science Fiction": 1, 
    "TV Movie": 1, 
    "Thriller": 1, 
    "War": 1,
    "Western": 1
}
# ---------------------

# TMDB Genre ID Map (Static Standard)
GENRE_MAP = {
    28: "Action", 12: "Adventure", 16: "Animation", 35: "Comedy", 
    80: "Crime", 99: "Documentary", 18: "Drama", 10751: "Family", 
    14: "Fantasy", 36: "History", 27: "Horror", 10402: "Music", 
    9648: "Mystery", 10749: "Romance", 878: "Science Fiction", 
    10770: "TV Movie", 53: "Thriller", 10752: "War", 37: "Western"
}
