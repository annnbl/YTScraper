from datetime import datetime


def days_old(date_str):
    dt = datetime.strptime(date_str.replace("Z", ""), "%Y-%m-%dT%H:%M:%S")
    return max(1, (datetime.utcnow() - dt).days)


def score_video(video):
    age = days_old(video["published"])

    velocity = video["views"] / age
    engagement = (video["likes"] + video["comments"]) / max(1, video["views"])

    return (velocity * 0.7) + (engagement * 0.3)


def rank_videos(videos):
    for v in videos:
        v["score"] = score_video(v)

    return sorted(videos, key=lambda x: x["score"], reverse=True)


def get_creators(videos):
    creators = {}

    for v in videos:
        c = v["channel"]

        if c not in creators:
            creators[c] = {
                "channel": c,
                "total_views": 0,
                "videos": 0
            }

        creators[c]["total_views"] += v["views"]
        creators[c]["videos"] += 1

    return sorted(creators.values(), key=lambda x: x["total_views"], reverse=True)