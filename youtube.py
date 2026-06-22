from googleapiclient.discovery import build
from datetime import datetime, timedelta
import os

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)


def search_videos(keyword, max_results=25):
    week_ago = (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")

    request = youtube.search().list(
        q=keyword,
        part="snippet",
        type="video",
        maxResults=max_results,
        regionCode="US",
        relevanceLanguage="en",
        order="relevance",
        publishedAfter=week_ago
    )
    response = request.execute()
    return [item["id"]["videoId"] for item in response["items"]]


def get_video_details(video_ids):
    request = youtube.videos().list(
        part="snippet,statistics,contentDetails",
        id=",".join(video_ids)
    )
    response = request.execute()

    videos = []
    for item in response["items"]:
        snippet = item["snippet"]
        stats = item.get("statistics", {})
        duration = item.get("contentDetails", {}).get("duration", "PT0S")

        videos.append({
            "video_id": item["id"],
            "url":