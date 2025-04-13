import pytesseract
from PIL import Image

def extract_text(image: Image.Image) -> str:
    return pytesseract.image_to_string(image)
