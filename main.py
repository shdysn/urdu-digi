import os

from PIL import Image

from src.ai_verifier import verify_with_gemini
from src.ocr_engine import run_easyocr
from src.pdf_utils import extract_images_from_pdf


INPUT_DIR = "input"
OUTPUT_DIR = "output"
SUPPORTED_IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".webp")


def process_file(file_name):
    file_path = os.path.join(INPUT_DIR, file_name)

    if file_name.lower().endswith(".pdf"):
        print(f"PDF extract ho rahi hai: {file_name}")
        pages = extract_images_from_pdf(file_path)
    elif file_name.lower().endswith(SUPPORTED_IMAGE_EXTENSIONS):
        pages = [(1, Image.open(file_path))]
    else:
        return

    for page_num, image in pages:
        print(f"\n--- Page {page_num} Processing ---")
        print("1. EasyOCR se text nikal raha hai...")
        raw_text = run_easyocr(image)

        print("2. Gemini image aur text ko compare kar raha hai...")
        final_text = verify_with_gemini(image, raw_text)

        output_file = os.path.join(OUTPUT_DIR, f"{file_name}_page_{page_num}.txt")
        with open(output_file, "w", encoding="utf-8") as output:
            output.write(final_text or "")

        print(f"Saved: {output_file}")


if __name__ == "__main__":
    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    files = [file_name for file_name in os.listdir(INPUT_DIR) if not file_name.startswith(".")]
    if not files:
        print("input/ folder khali hai! Koi image ya PDF wahan upload karein.")
    else:
        for file_name in files:
            process_file(file_name)