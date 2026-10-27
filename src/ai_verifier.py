import os

from dotenv import load_dotenv
from google import genai


load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


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

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=[pil_image, prompt],
    )
    return response.text