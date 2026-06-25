import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash-lite""gemini-3.1-flash-lite-preview-06-17")


def analyze_reddit(keyword, posts):
    top_posts = posts[:8]

    post_summaries = []
    for p in top_posts:
        post_summaries.append({
            "title": p["title"],
            "subreddit": p["subreddit"],
            "upvotes": f"{p['upvotes']:,}",
            "comments": p["comments"],
            "upvote_ratio": f"{p['upvote_ratio']}%",
            "age_days": p["age_days"],
            "velocity": round(p["velocity"], 1),
            "preview": p["text_preview"]
        })

    prompt = f"""You are a viral content strategist analyzing why Reddit posts explode in upvotes.

Keyword: "{keyword}"

Top performing posts (ranked by upvote velocity):
{post_summaries}

Analyze ONLY these 3 things, be specific and direct:

1. 🪝 HOOKS & TITLES
   - What title patterns are working? (questions, confessions, controversies, data/numbers)
   - What words/phrases keep appearing?
   - Why do these titles get clicked and upvoted?

2. 😮 EMOTIONAL TRIGGERS
   - What core emotion is being activated? (outrage, relatability, curiosity, fear, inspiration)
   - What pain point or desire is being tapped?
   - Why does this resonate with this specific subreddit audience?

3. ⏱️ TIMING & VELOCITY
   - How old are the top posts vs their upvote counts?
   - Is this topic evergreen or a short-lived spike on Reddit?
   - What's the best time/angle to post about this topic?

Be blunt, specific, and actionable. No fluff.
"""

    response = model.generate_content(prompt)
    return response.text