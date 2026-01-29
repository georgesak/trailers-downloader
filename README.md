# Trailers Downloader

A Python script to automatically download movie trailers from YouTube based on popular movies from TMDB (The Movie Database), filtered by genre.

## Features

- Fetches popular movies from TMDB.
- Filters movies by user-defined genres.
- Downloads trailers from YouTube using `yt-dlp`.
- Supports multi-threaded downloading.
- Maintains a history file to avoid re-downloading previously downloaded trailers.
- Configurable output directory, limit, and genres.

## Prerequisites

- Python 3.x
- [FFmpeg](https://ffmpeg.org/download.html) (Required by `yt-dlp` for merging video and audio)

## Installation

1.  Clone the repository or download the source code.
2.  Install the required Python packages:

    ```bash
    pip install requests yt-dlp
    ```

3.  Ensure `ffmpeg` is installed and added to your system's PATH (or in the same folder as the script).

## Configuration

Edit `config.py` to customize the behavior:

-   **TMDB_API_KEY**: Get your own API key from [The Movie Database](https://www.themoviedb.org/documentation/api) and paste it here.
-   **OUTPUT_FOLDER**: The directory where trailers will be saved.
-   **LIMIT**: The number of trailers to download in one run.
-   **MAX_WORKERS**: Number of parallel downloads.
-   **MAX_VIDEO_HEIGHT**: Maximum video resolution (height) for downloads. Default is `1080`.
-   **HISTORY_FILE**: The filename to store the list of downloaded trailers.
    -   Set to a filename (e.g., `'downloaded_history.txt'`) to enable history tracking (prevents duplicates).
    -   Set to `None`, `''` (empty string), or comment it out to **disable** history tracking.
-   **ALLOWED_GENRES**: Set genres to `1` to include them, or `0` to exclude them.

## Usage

Run the script using Python:

```bash
python Trailers_Downloader.py
```

## History File

The script uses a history file (default: `downloaded_history.txt`) in the output folder to keep track of downloaded trailers.

-   **Enabled**: The script checks this file before downloading. If a trailer ID is in the file, it is skipped. New downloads are appended to this file.
-   **Disabled**: If you remove `HISTORY_FILE` from `config.py` or set it to an empty string, the script will not check or write to any history file. It will rely on checking if the `.mp4` file already exists in the folder to avoid re-downloading.
