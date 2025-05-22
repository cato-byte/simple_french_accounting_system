import requests

def call_huggingface_parser(ocr_raw: list[dict]) -> dict:
    """
    Send OCR raw output to the Hugging Face parser container and return structured fields.
    """
    response = requests.post("http://huggingface-parser:5003/parse", json={"ocr_raw": ocr_raw})
    if response.ok:
        return response.json()
    return {}

def extract_text_from_receipt(image_file):
    """
    Send the receipt image to the OCR container and return the raw OCR result (list of boxes).
    """
    response = requests.post("http://ocr:5000/ocr", files={"file": image_file})
    response.raise_for_status()
    return response.json().get("raw", [])  # <-- this is the list of {text, box, confidence}

def extract_fields_from_receipt_image(image_file):
    """
    Full flow: OCR → Hugging Face parser → structured fields.
    """
    ocr_raw = extract_text_from_receipt(image_file)
    if not ocr_raw:
        return {}

    parsed_fields = call_huggingface_parser(ocr_raw)
    return parsed_fields