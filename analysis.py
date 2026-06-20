from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def analyze(keyword, videos, creators):
    top_videos = videos[:8]
    top_creators = creators[:5]

    prompt = f"""
You are analyzing North American YouTube trends.

Keyword: {keyword}

Top Videos:
{top_videos}

Top Creators:
{top_creators}

Return:
1. Why this topic is trending
2. Common video hooks/formats
3. Emotional triggers used
4. Content gaps creators can exploit
5. Best creators for collaboration and why
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content