from io import BytesIO

import pytesseract
from PIL import Image


def recognize_text_from_image(image_bytes: bytes) -> str:
    img = Image.open(BytesIO(image_bytes))

    text = pytesseract.image_to_string(
        img,
        lang="rus+eng",
        config="--psm 3",
    )

    if not text.strip():
        raise ValueError('The text can not be recognized')

    return text