import easyocr
import numpy as np


reader = easyocr.Reader(["ur"], gpu=False)


def run_easyocr(pil_image):
    image_array = np.array(pil_image)
    raw_results = reader.readtext(image_array, detail=0)
    return " ".join(raw_results)