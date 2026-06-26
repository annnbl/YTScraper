import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash-lite")


def analyze(keyword, videos, creators):
    try:
        top_videos = videos[:8]

        video_summaries = []
        for v in top_videos:
            video_summaries.append({
                "title": v["title"],
                "channel": v["channel"],
                "published": v["published"][:10],
                "views": f"{v['views']:,}",
                "likes": f"{v['likes']:,}",
                "comments": f"{v['comments']:,}",
                "tags": v["tags"],
                "description_preview": v["description"],
                "url": v["url"]
            })

        prompt = f"""You are a viral content strategist analyzing why YouTube videos explode in views.

Keyword: "{keyword}"

Top performing videos (ranked by views):
{video_summaries}

Analyze ONLY these 3 things, be specific and direct:

1. 🪝 HOOKS & TITLES
   - What title patterns are working? (numbers, questions, shock, curiosity gaps)
   - What words/phrases keep appearing?
   - Why do these hooks stop the scroll?

2. 😮 EMOTIONAL TRIGGERS
   - What core emotion is being activated? (fear, greed, curiosity, outrage, hope)
   - How is the thumbnail/title combo triggering that emotion?
   - What pain point or desire is being tapped?

3. ⏱️ TIMING & VELOCITY
   - How recent are the top videos?
   - Is this topic evergreen or a short-lived spike?
   - What's the ideal window to publish content on this topic?

Be blunt, specific, and actionable. No fluff.
"""

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        if "ResourceExhausted" in str(e):
            return "⚠️ Gemini free tier daily limit reached. Please try again after midnight Pacific time (UTC-7)."
        return f"⚠️ Analysis failed: {str(e)}"