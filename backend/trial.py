import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import cv2
import numpy as np
import os

# OPTIONAL: Manually specify tesseract path (Windows only)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_image(image_path: str) -> str:
    """
    Extract text accurately from an image using Tesseract OCR with preprocessing.
    """
    # --- Load image ---
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError(f"❌ Could not load image: {image_path}")

    # --- Convert to grayscale ---
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # --- Apply threshold to make text clearer ---
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # --- Denoise and sharpen ---
    gray = cv2.medianBlur(gray, 3)

    # --- Save temp preprocessed image ---
    temp_filename = "temp_ocr_image.png"
    cv2.imwrite(temp_filename, gray)

    # --- Extract text using pytesseract ---
    extracted_text = pytesseract.image_to_string(Image.open(temp_filename), lang='eng')

    # --- Cleanup temp file ---
    os.remove(temp_filename)

    return extracted_text.strip()
