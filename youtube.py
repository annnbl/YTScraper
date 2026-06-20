from googleapiclient.discovery import build
from config import YOUTUBE_API_KEY

youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)


def search_videos(keyword, max_results=25):
    request = youtube.search().list(
        q=keyword,
        part="snippet",
        type="video",
        maxResults=max_results,
        regionCode="US",
        relevanceLanguage="en"
    )
    response = request.execute()

    video_ids = []
    for item in response["items"]:
        video_ids.append(item["id"]["videoId"])

    return video_ids


def get_video_details(video_ids):
    request = youtube.videos().list(
        part="snippet,statistics",
        id=",".join(video_ids)
    )
    response = request.execute()

    videos = []

    for item in response["items"]:
        snippet = item["snippet"]
        stats = item.get("statistics", {})

        videos.append({
            "video_id": item["id"],
            "title": snippet["title"],
            "channel": snippet["channelTitle"],
            "published": snippet["publishedAt"],
            "views": int(stats.get("viewCount", 0)),
            "likes": int(stats.get("likeCount", 0)),
            "comments": int(stats.get("commentCount", 0))
        })

    return videos