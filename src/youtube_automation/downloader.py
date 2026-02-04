import logging
from pathlib import Path
from typing import Optional

from yt_dlp import YoutubeDL

logger = logging.getLogger(__name__)


class Downloader:
    def __init__(self, download_dir: str):
        self.download_path = Path(download_dir)
        self.download_path.mkdir(parents=True, exist_ok=True)

    def download(self, video_id: str) -> Optional[Path]:
        url = f"https://www.youtube.com/watch?v={video_id}"
        output_template = str(self.download_path / "%(title)s [%(id)s].%(ext)s")
        options = {
            "outtmpl": output_template,
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": "mp4",
            "quiet": True,
            "no_warnings": True,
        }
        try:
            with YoutubeDL(options) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
            path = Path(filename)
            logger.info("Downloaded video %s to %s", video_id, path)
            return path
        except Exception as exc:
            logger.exception("Failed to download video %s: %s", video_id, exc)
            return None
