import streamlit as st
from youtube import search_videos, get_video_details
from trends import rank_videos, get_creators
from analysis import analyze

st.set_page_config(page_title="YouTube Viral Intelligence", page_icon="🔥", layout="wide")
st.title("🔥 YouTube Viral Intelligence Tool")
st.caption("Find out why videos go viral — hooks, emotions, and timing.")

keyword = st.text_input("Enter keyword or topic", "credit card debt")
num_videos = st.slider("Number of videos to analyze", 5, 25, 10)

if st.button("🔍 Analyze Virality", type="primary"):

    with st.spinner("Fetching top videos..."):
        video_ids = search_videos(keyword, max_results=num_videos)
        videos = get_video_details(video_ids)
        ranked_videos = rank_videos(videos)
        creators = get_creators(ranked_videos)

    col1, col2 = st.columns([3, 2])

    with col1:
        st.subheader("🔥 Top Trending Videos")
        for i, v in enumerate(ranked_videos[:10], 1):
            with st.expander(f"#{i} — {v['title']}"):
                st.markdown(f"**Channel:** {v['channel']}")
                st.markdown(f"**Views:** {v['views']:,} &nbsp;|&nbsp; **Likes:** {v['likes']:,} &nbsp;|&nbsp; **Comments:** {v['comments']:,}")
                st.markdown(f"**Engagement Rate:** {v['engagement_rate']}% &nbsp;|&nbsp; **Age:** {v['days_old']} days old")
                st.markdown(f"**Virality Score:** {round(v['score'], 2)}")
                if v["tags"]:
                    st.markdown(f"**Tags:** `{'`, `'.join(v['tags'][:6])}`")
                st.markdown(f"[▶ Watch on YouTube]({v['url']})")

    with col2:
        st.subheader("🏆 Top Creators")
        for c in creators[:5]:
            st.markdown(f"**{c['channel']}**")
            st.markdown(f"Views: `{c['total_views']:,}` &nbsp;|&nbsp; Videos: `{c['videos']}` &nbsp;|&nbsp; Avg Engagement: `{c['avg_engagement']}%`")
            st.divider()

    st.subheader("🧠 Viral Analysis")
    with st.spinner("Analyzing why this is going viral..."):
        result = analyze(keyword, ranked_videos, creators)
    st.markdown(result)