import io

import fitz
from PIL import Image


def extract_images_from_pdf(pdf_path):
    images = []
    with fitz.open(pdf_path) as doc:
        for page_num, page in enumerate(doc, start=1):
            pixmap = page.get_pixmap(dpi=200)
            image = Image.open(io.BytesIO(pixmap.tobytes("png")))
            images.append((page_num, image))
    return images