import streamlit as st
import requests
import urllib.parse
from datetime import datetime, timedelta
import os
from analysis_reddit import analyze_reddit
import time

st.set_page_config(page_title="Reddit Viral Intelligence", page_icon="🔴", layout="wide")
st.title("🔴 Reddit Viral Intelligence Tool")
st.caption("Find out why posts go viral on Reddit — hooks, emotions, and timing.")

SUBREDDITS = [
    "personalfinance",
    "investing",
    "financialindependence",
    "FinancialPlanning",
    "Frugal",
    "Insurance",
    "leanfire",
    "MoneyDiariesACTIVE",
    "OriginFinancial",
    "pointstravel",
    "SideProject",
    "StableCoins",
    "startups",
    "stocks",
    "taskmonkey",
    "TheMoneyGuy",
    "WeekendMVP",
    "fatFIRE"
]


def search_reddit(keyword, subreddit, time_filter="week", limit=25):
    time_map = {"day": 1, "week": 7, "month": 30}
    days = time_map.get(time_filter, 7)

    # Arctic Shift commonly expects ISO timestamps, not Unix timestamps
    after_date = (
        datetime.utcnow() - timedelta(days=days)
    ).strftime("%Y-%m-%dT%H:%M:%SZ")

    url = "https://arctic-shift.photon-reddit.com/api/posts/search"

    params = {
    "subreddit": subreddit.lower().replace("r/", ""),
    "title": keyword,
    "after": after_date,
    "limit": int(limit),
    "sort": "desc",
    "sort_type": "default"
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=20,
            headers={
                "User-Agent": "reddit-viral-intelligence/1.0"
            }
        )

        if response.status_code != 200:
            st.warning(f"r/{subreddit} returned status {response.status_code}")
            st.code(response.text)  # temporary: shows the actual API error
            return []

        data = response.json()

        # Arctic Shift may return "data" or "posts" depending on endpoint version
        items = data.get("data", data.get("posts", []))

        posts = []
        for p in items:
            created_utc = p.get("created_utc", 0)

            # Some API responses give a Unix timestamp, others ISO text
            if isinstance(created_utc, (int, float)):
                created = datetime.utcfromtimestamp(created_utc)
            else:
                created = datetime.fromisoformat(
                    str(created_utc).replace("Z", "+00:00")
                ).replace(tzinfo=None)

            age_days = max(1, (datetime.utcnow() - created).days)
            score = int(p.get("score", 0))

            posts.append({
                "title": p.get("title", ""),
                "subreddit": subreddit,
                "url": f"https://reddit.com{p.get('permalink', '')}",
                "upvotes": score,
                "comments": int(p.get("num_comments", 0)),
                "upvote_ratio": round(float(p.get("upvote_ratio", 0)) * 100, 1),
                "age_days": age_days,
                "velocity": round(score / age_days, 1),
                "flair": p.get("link_flair_text") or "None",
                "text_preview": p.get("selftext", "")[:200]
            })

        return posts

    except requests.RequestException as e:
        st.warning(f"Could not fetch r/{subreddit}: {e}")
        return []
col1, col2 = st.columns(2)

with col1:
    keyword = st.text_input("Enter keyword or topic", "credit card debt")

with col2:
    selected_subreddits = st.multiselect(
        "Select subreddits",
        SUBREDDITS,
        default=["personalfinance", "investing"]
    )

time_filter = st.selectbox("Time period", ["week", "day", "month"], index=0)
num_posts = st.slider("Posts per subreddit", 5, 25, 10)

if st.button("🔍 Analyze Reddit Trends", type="primary"):

    if not selected_subreddits:
        st.warning("Please select at least one subreddit.")
        st.stop()

    all_posts = []

    with st.spinner("Fetching Reddit posts..."):
        for sub in selected_subreddits:
            posts = search_reddit(keyword, sub, time_filter, num_posts)
            all_posts.extend(posts)
            time.sleep(0.5)

    if not all_posts:
        st.error("No posts found. Try a different keyword or subreddit.")
        st.stop()

    ranked_posts = sorted(all_posts, key=lambda x: x["velocity"], reverse=True)

    col1, col2 = st.columns([3, 2])

    with col1:
        st.subheader("🔥 Top Trending Posts")
        for i, p in enumerate(ranked_posts[:10], 1):
            with st.expander(f"#{i} — {p['title']}"):
                st.markdown(f"**Subreddit:** r/{p['subreddit']} &nbsp;|&nbsp; **Flair:** {p['flair']}")
                st.markdown(f"**Upvotes:** {p['upvotes']:,} &nbsp;|&nbsp; **Comments:** {p['comments']:,} &nbsp;|&nbsp; **Upvote Ratio:** {p['upvote_ratio']}%")
                st.markdown(f"**Age:** {p['age_days']} days &nbsp;|&nbsp; **Velocity:** {p['velocity']} upvotes/day")
                if p["text_preview"]:
                    st.markdown(f"**Preview:** {p['text_preview']}...")
                st.markdown(f"[▶ View on Reddit]({p['url']})")

    with col2:
        st.subheader("📊 Subreddit Breakdown")
        sub_stats = {}
        for p in ranked_posts:
            s = p["subreddit"]
            if s not in sub_stats:
                sub_stats[s] = {"total_upvotes": 0, "posts": 0, "total_comments": 0}
            sub_stats[s]["total_upvotes"] += p["upvotes"]
            sub_stats[s]["posts"] += 1
            sub_stats[s]["total_comments"] += p["comments"]

        for sub, stats in sorted(sub_stats.items(), key=lambda x: x[1]["total_upvotes"], reverse=True):
            st.markdown(f"**r/{sub}**")
            st.markdown(f"Upvotes: `{stats['total_upvotes']:,}` &nbsp;|&nbsp; Posts: `{stats['posts']}` &nbsp;|&nbsp; Comments: `{stats['total_comments']:,}`")
            st.divider()

    st.subheader("🧠 Viral Analysis")
    with st.spinner("Analyzing why this is going viral on Reddit..."):
        result = analyze_reddit(keyword, ranked_posts)
    st.markdown(result)