
import os
import difflib
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def correct_text(text, model="gpt-3.5-turbo"):
    prompt = f"""You are a grammar and writing expert.

1. Correct the grammar and spelling in the following text.
2. Rewrite the corrected text to be more natural and fluent like a native speaker.

Text:
{text}
"""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    full_output = response.choices[0].message.content

    # Attempt to parse output if separated into parts
    parts = full_output.split("2.")
    corrected = parts[0].strip()
    better_response = parts[1].strip() if len(parts) > 1 else ""

    return corrected, [], better_response
