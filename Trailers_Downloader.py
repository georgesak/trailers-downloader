import os
import requests
import yt_dlp
import time
import concurrent.futures
import threading
import config

class TrailerDownloader:
    def __init__(self, api_key, output_folder, allowed_genres, history_file):
        self.api_key = api_key
        self.output_folder = output_folder
        self.allowed_genres = allowed_genres
        self.history_file = history_file
        self.allowed_ids = self._get_allowed_genre_ids()
        self.print_lock = threading.Lock() # To prevent garbled console output

        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def _get_allowed_genre_ids(self):
        """Converts the list of user genre names into TMDB IDs."""
        name_to_id = {v: k for k, v in config.GENRE_MAP.items()}
        return {
            name_to_id[name] 
            for name, is_allowed in self.allowed_genres.items() 
            if is_allowed and name in name_to_id
        }

    def log(self, message):
        """Thread-safe print function."""
        with self.print_lock:
            print(message)

    def fetch_filtered_movies(self, limit):
        """Fetches popular movies and filters them by genre until we hit the limit."""
        valid_movies = []
        page = 1
        
        self.log(f"Searching for {limit} movies matching your genres...")
        
        while len(valid_movies) < limit and page <= 5: # Limit to 5 pages
            url = "https://api.themoviedb.org/3/movie/popular"
            params = {
                'api_key': self.api_key,
                'language': 'en-US',
                'page': page
            }
            try:
                response = requests.get(url, params=params)
                response.raise_for_status()
                results = response.json().get('results', [])
                
                for movie in results:
                    movie_genres = set(movie.get('genre_ids', []))
                    # Check if the movie has ANY of the allowed genres
                    if not movie_genres.isdisjoint(self.allowed_ids):
                        valid_movies.append(movie)
                        if len(valid_movies) >= limit:
                            break
                
                page += 1
                time.sleep(0.2) 
                
            except requests.RequestException as e:
                self.log(f"Error fetching page {page}: {e}")
                break
                
        return valid_movies

    def get_trailer_url(self, movie_id):
        """Finds the YouTube trailer URL for a specific movie ID."""
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos"
        params = {
            'api_key': self.api_key,
            'language': 'en-US'
        }
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                results = response.json().get('results', [])
                for video in results:
                    if video.get('site') == 'YouTube' and video.get('type') == 'Trailer':
                        return f"https://www.youtube.com/watch?v={video.get('key')}"
        except requests.RequestException:
            pass
        return None

    def download_trailer(self, url, title, year):
        """Downloads the trailer using yt-dlp."""
        # Clean title
        safe_title = "".join([c for c in title if c.isalpha() or c.isdigit() or c==' ' or c in '-_']).rstrip()
        filename = f"{safe_title} ({year})"
        file_path = os.path.join(self.output_folder, f"{filename}.mp4")
        safe_title = "".join([c for c in title if c.isalpha() or c.isdigit() or c==' ' or c in '-_']).rstrip()
        filename = f"{safe_title} ({year})"
        file_path = os.path.join(self.output_folder, f"{filename}.mp4")
        
        archive_file = None
        if self.history_file:
            archive_file = os.path.join(self.output_folder, self.history_file)

        if os.path.exists(file_path):
            self.log(f"Skipping (File exists): {filename}")
            return

        self.log(f"Processing: {filename}...")
        
        ydl_opts = {
            'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]/best',
            'merge_output_format': 'mp4',
            'outtmpl': file_path,
            'quiet': True,
            'no_warnings': True,
        }
        
        if archive_file:
            ydl_opts['download_archive'] = archive_file

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                # yt-dlp handles the download archive check internally, but logic here can be simplified
                # if it downloaded, info will be present.
                
                # We can check if file exists now to confirm download
                if os.path.exists(file_path):
                     # Could check height/width here if desired, usually mostly relevant for debugging
                    self.log(f"Downloaded: {filename}")
                else:
                    self.log(f"Skipped (In History or Failed): {filename}")

        except Exception as e:
            self.log(f"Failed: {filename} ({e})")

    def process_movie(self, movie):
        """Worker function to process a single movie."""
        title = movie.get('title', 'Unknown')
        release_date = movie.get('release_date', '0000')
        year = release_date.split('-')[0] if release_date else '0000'
        movie_id = movie.get('id')
        
        if not movie_id:
            return

        trailer_url = self.get_trailer_url(movie_id)
        
        if trailer_url:
            self.download_trailer(trailer_url, title, year)
        else:
            self.log(f"No trailer found for: {title}")

    def run(self, limit=10, max_workers=5):
        movies = self.fetch_filtered_movies(limit)
        self.log(f"Found {len(movies)} candidates. Checking for trailers with {max_workers} threads...")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            executor.map(self.process_movie, movies)
            
        self.log("\nDone!")

def main():
    history_file = getattr(config, 'HISTORY_FILE', None)
    downloader = TrailerDownloader(config.TMDB_API_KEY, config.OUTPUT_FOLDER, config.ALLOWED_GENRES, history_file)
    downloader.run(config.LIMIT, config.MAX_WORKERS)

if __name__ == "__main__":
    main()