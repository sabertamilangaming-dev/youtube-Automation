import logging
from typing import Dict, List

from googleapiclient.discovery import build

logger = logging.getLogger(__name__)


class YouTubeApi:
    def __init__(self, api_key: str):
        self.client = build("youtube", "v3", developerKey=api_key)

    def get_uploads_playlist_id(self, channel_id: str) -> str:
        request = self.client.channels().list(
            part="contentDetails",
            id=channel_id,
            maxResults=1,
        )
        response = request.execute()
        items = response.get("items", [])
        if not items:
            raise ValueError("No channel found for provided channel ID")
        return items[0]["contentDetails"]["relatedPlaylists"]["uploads"]

    def list_latest_videos(self, uploads_playlist_id: str, max_results: int = 25) -> List[Dict[str, str]]:
        request = self.client.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=uploads_playlist_id,
            maxResults=max_results,
        )
        response = request.execute()
        items = response.get("items", [])
        videos = []
        for item in items:
            snippet = item.get("snippet", {})
            content = item.get("contentDetails", {})
            videos.append(
                {
                    "video_id": content.get("videoId", ""),
                    "title": snippet.get("title", ""),
                    "published_at": content.get("videoPublishedAt", ""),
                }
            )
        logger.info("Fetched %s videos from playlist", len(videos))
        return videos
