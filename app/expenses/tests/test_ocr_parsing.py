import pytest
from unittest.mock import patch
from expenses.ocr_parsing import extract_fields_from_receipt_image

# Mocked response class
class MockResponse:
    def __init__(self, json_data, status_code=200):
        self._json_data = json_data
        self.status_code = status_code

    def json(self):
        return self._json_data

    @property
    def ok(self):
        return self.status_code == 200

    def raise_for_status(self):
        if not self.ok:
            raise Exception("Mocked error")

# Dummy file-like object
class DummyFile:
    def read(self):
        return b"fake-image-bytes"

@patch("expenses.ocr_parsing.requests.post")
def test_extract_fields_from_receipt_image(mock_post):
    # Mock OCR response
    ocr_response = {
        "raw": [
            {"text": "Sandwichez Ltd."},
            {"text": "Invoice: T001/207831"},
            {"text": "Date: 16/05/2025"},
            {"text": "Total: €3.55"},
            {"text": "Paid with credit card."}
        ]
    }

    # Mock Hugging Face parser response
    parser_response = {
        "supplier": "Sandwichez Ltd.",
        "invoice_number": "T001/207831",
        "date": "2025-05-16",
        "total": 3.55,
        "amounts": [["Total: €3.55", 3.55]],
        "payment_method": "card"
    }

    # Configure mock behavior: first call → OCR, second call → parser
    mock_post.side_effect = [
        MockResponse(ocr_response),
        MockResponse(parser_response)
    ]

    result = extract_fields_from_receipt_image(DummyFile())

    assert result["supplier"] == "Sandwichez Ltd."
    assert result["invoice_number"] == "T001/207831"
    assert result["total"] == 3.55
    assert result["payment_method"] == "card"
    assert result["date"] == "2025-05-16"
    assert any(a[1] == 3.55 for a in result["amounts"])