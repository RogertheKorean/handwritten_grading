
from PIL import ImageDraw, ImageFont

def annotate_image(image, corrections):
    draw = ImageDraw.Draw(image)
    width, height = image.size
    font_size = max(15, width // 50)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()

    y_offset = 10
    for orig, corr in corrections:
        message = f"{orig} → {corr}"
        draw.text((10, y_offset), message, fill="red", font=font)
        y_offset += font_size + 10

    return image
