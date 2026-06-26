def rank_videos(videos, keyword=""):
    """Sort videos by views descending — no calculated scores."""
    return sorted(videos, key=lambda x: x["views"], reverse=True)


def get_creators(videos):
    creators = {}
    for v in videos:
        c = v["channel"]
        if c not in creators:
            creators[c] = {"channel": c, "total_views": 0, "total_likes": 0, "total_comments": 0, "videos": 0}
        creators[c]["total_views"] += v["views"]
        creators[c]["total_likes"] += v["likes"]
        creators[c]["total_comments"] += v["comments"]
        creators[c]["videos"] += 1

    return sorted(creators.values(), key=lambda x: x["total_views"], reverse=True)