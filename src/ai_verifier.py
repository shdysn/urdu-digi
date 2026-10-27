import itertools
import os

from dotenv import load_dotenv
from google import genai


load_dotenv()
raw_keys = os.getenv("GEMINI_API_KEY", "")
api_keys = [key.strip() for key in raw_keys.split(",") if key.strip()]

if not api_keys:
    raise ValueError("GEMINI_API_KEY nahi mili! Barahe karam secret check karein.")

key_pool = itertools.cycle(api_keys)


def verify_with_gemini(pil_image, raw_ocr_text):
    prompt = f"""
Aapke samne 2 cheezein hain:
1. Kitab ke safhay ki asal tasveer (image).
2. EasyOCR se nikala gaya raw text (niche diya gaya hai).

Kaam:
- Niche diye gaye text ko asal tasveer ke sath match karein.
- Jahan OCR ne ghalti ki ho ya nuqte kharab kiye hon, tasveer dekh kar bilkul theek karein.
- Koi lafz apni taraf se add na karein, sirf tasveer ke mutabiq 100% theek Urdu matan wapas dein.

--- Raw OCR Text ---
{raw_ocr_text}
-------------------
"""

    client = genai.Client(api_key=next(key_pool))
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=[pil_image, prompt],
    )
    return response.text