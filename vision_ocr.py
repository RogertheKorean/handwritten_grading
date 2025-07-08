
import os
import json
import io
from google.cloud import vision
from PIL import Image

def extract_text(image: Image.Image) -> str:
    key_json = os.getenv("GCP_KEY_JSON")

    if key_json:
        key_dict = json.loads(key_json)
        with open("temp_gcp_key.json", "w") as f:
            json.dump(key_dict, f)
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "temp_gcp_key.json"
    else:
        raise ValueError("GCP_KEY_JSON environment variable not found.")

    client = vision.ImageAnnotatorClient()

    img_bytes = io.BytesIO()
    image.save(img_bytes, format='PNG')
    content = img_bytes.getvalue()

    image_for_api = vision.Image(content=content)
    response = client.text_detection(image=image_for_api)
    texts = response.text_annotations

    if os.path.exists("temp_gcp_key.json"):
        os.remove("temp_gcp_key.json")

    return texts[0].description if texts else ""
