from transformers import pipeline
from date_parser import DateParser
from amount_parser import AmountParser

date_parser = DateParser()
amount_parser = AmountParser()
ner_pipeline = pipeline("ner", model="Davlan/xlm-roberta-base-ner-hrl", grouped_entities=True)

def extract_fields(ocr_raw):
    """
    Receives OCR output as a list of dicts from EasyOCR
    Returns structured extracted fields
    """
    text = " ".join(entry["text"] for entry in ocr_raw)
    ner_results = ner_pipeline(text)

    fields = {
        "supplier": None,
        "invoice_number": None,
        "date": None,
        "amounts": [],         # List of (context, Decimal)
        "total": None,         # Best guess
        "payment_method": None
    }

    # NER logic
    for entity in ner_results:
        label = entity["entity_group"].lower()
        value = entity["word"]

        if label == "org" and not fields["supplier"]:
            fields["supplier"] = value
        elif label == "misc" and "t" in value.lower() and not fields["invoice_number"]:
            fields["invoice_number"] = value

    # Amounts and total
    amounts = amount_parser.extract_amounts_with_context(ocr_raw)
    fields["amounts"] = amounts
    fields["total"] = amount_parser.guess_total(amounts)

    # Date
    fields["date"] = date_parser.parse(text)

    # Payment method heuristic
    lowered = text.lower()
    if any(k in lowered for k in ["carte", "credit", "targeta", "tarjeta"]):
        fields["payment_method"] = "card"
    elif any(k in lowered for k in ["efectiu", "cash", "espèces"]):
        fields["payment_method"] = "cash"

    return fields
