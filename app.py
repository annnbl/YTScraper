import streamlit as st

from youtube import search_videos, get_video_details
from trends import rank_videos, get_creators
from analysis import analyze

st.title("🔥 YouTube NA Trend Intelligence Tool")

keyword = st.text_input("Enter keyword", "credit card debt")

if st.button("Run Analysis"):

    st.write("Fetching videos...")

    video_ids = search_videos(keyword)
    videos = get_video_details(video_ids)

    ranked_videos = rank_videos(videos)
    creators = get_creators(ranked_videos)

    st.subheader("🔥 Top Trending Videos")

    for v in ranked_videos[:10]:
        st.write({
            "title": v["title"],
            "channel": v["channel"],
            "views": v["views"],
            "score": round(v["score"], 2)
        })

    st.subheader("🏆 Top Creators")

    for c in creators[:5]:
        st.write(c)

    st.subheader("🧠 AI Analysis")

    result = analyze(keyword, ranked_videos, creators)
    st.write(result)