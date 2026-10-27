import itertools
import os

from dotenv import load_dotenv
from google import genai


load_dotenv()
raw_keys = os.getenv("GEMINI_API_KEY", "")
api_keys = []

for key in raw_keys.replace("\n", ",").replace(";", ",").split(","):
    cleaned_key = key.strip().strip("'\"")
    if "GEMINI_API_KEY=" in cleaned_key:
        cleaned_key = cleaned_key.split("GEMINI_API_KEY=", 1)[-1].strip().strip("'\"")
    if cleaned_key:
        api_keys.append(cleaned_key)

if not api_keys:
    raise ValueError("Koi valid GEMINI_API_KEY nahi mili! GitHub Secrets check karein.")

print(f"Total {len(api_keys)} API keys detect hui hain.")
for index, key in enumerate(api_keys, start=1):
    masked_key = "*" * min(len(key), 8)
    print(f"Key {index}: {masked_key} (total length: {len(key)})")

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
        model="gemini-3.5-flash-lite",
        contents=[pil_image, prompt],
    )
    return response.text