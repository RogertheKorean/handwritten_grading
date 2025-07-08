
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def correct_text(text, model="gpt-3.5-turbo"):
    prompt = f"""You are a grammar and writing expert.

1. Correct the grammar and spelling in the following text.
2. Then rewrite it to be more fluent and natural for native English speakers.

Text:
{text}
"""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    full_output = response.choices[0].message.content.strip()

    corrected = ""
    suggested = ""

    if "2." in full_output:
        parts = full_output.split("2.")
        corrected = parts[0].replace("1.", "").strip()
        suggested = parts[1].strip()
    else:
        suggested = full_output

    return corrected, [], suggested
