
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def correct_text(text, model="gpt-3.5-turbo"):
    prompt = f"""Correct the grammar and spelling in the following text and make it more fluent and natural like a native speaker. Only return the improved version.

Text:
{text}
"""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    improved = response.choices[0].message.content.strip()
    return improved, [], ""  # Only returning corrected as needed
