
import os
import json
import io
from google.cloud import vision
from PIL import Image

def extract_text(image: Image.Image) -> str:
    key_json = os.getenv("GCP_KEY_JSON")

    if key_json:
        key_dict = json.loads(key_json)
        with open("temp_key.json", "w") as f:
            json.dump(key_dict, f)
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "temp_key.json"

    client = vision.ImageAnnotatorClient()

    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    content = img_byte_arr.getvalue()

    image_for_api = vision.Image(content=content)
    response = client.text_detection(image=image_for_api)
    texts = response.text_annotations

    # Optional cleanup
    if os.path.exists("temp_key.json"):
        os.remove("temp_key.json")

    return texts[0].description if texts else ""
