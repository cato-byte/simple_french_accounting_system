from fastapi import FastAPI, File, UploadFile          # FastAPI for building the REST API
from fastapi.middleware.cors import CORSMiddleware     # Allows Django to call this service via HTTP
import easyocr                                         # PyTorch-based OCR engine
from PIL import Image                                  # Python Imaging Library to open/convert images
import io                                              # For byte stream reading
import numpy as np

app = FastAPI()

#  Allow calls from other containers ()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # could be restricted later to just Django
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load OCR model for English + French + Spanish (only once, on app start)
reader = easyocr.Reader(['fr', 'en', 'es', 'ca'], gpu=False)

# API endpoint for OCR
@app.post("/ocr")
async def ocr_endpoint(file: UploadFile = File(...)):
    image_bytes = await file.read()  # Read uploaded file
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")  # Convert to image
    image_np = np.array(image)

    results = reader.readtext(image_np)  # Perform OCR

    # results = [(bbox, text, confidence), ...]
    extracted_text = " ".join([item[1] for item in results])  # Join all text parts

        # Convert raw to plain Python types
    formatted_results = [
        {
            "box": [list(map(float, point)) for point in item[0]],  # Ensure float (or int)
            "text": str(item[1]),
            "confidence": float(item[2])
        }
        for item in results
    ]

    return {
        "text": extracted_text,
        "raw": formatted_results  # Also return raw data if you want bounding boxes and confidence
    }