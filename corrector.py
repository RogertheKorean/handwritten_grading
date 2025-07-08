
import os
import difflib
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def correct_text(text, model="gpt-3.5-turbo"):
    prompt = f"""You are a grammar and writing expert.

Please:
1. Correct the grammar and spelling in the following text.
2. Then rewrite it naturally and fluently like a native speaker.

Text:
{text}
"""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    full_output = response.choices[0].message.content.strip()

    # Try to split or detect both parts intelligently
    corrected = ""
    better_response = ""
    if "2." in full_output:
        parts = full_output.split("2.")
        corrected = parts[0].strip().replace("1.", "").strip()
        better_response = parts[1].strip()
    else:
        corrected = full_output

    return corrected, [], better_response
