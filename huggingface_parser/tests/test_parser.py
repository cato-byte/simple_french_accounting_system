import pytest
from parser import extract_fields
from datetime import date
from decimal import Decimal

class TestHuggingFaceParser:

    def test_extract_fields_basic_en(self):
        ocr_raw = [
            {"text": "Sandwichez Ltd."},
            {"text": "Invoice: T001/207831"},
            {"text": "Date: 16/05/2025"},
            {"text": "Total: €3.55"},
            {"text": "Paid with credit card."}
        ]
        fields = extract_fields(ocr_raw)
        assert fields["supplier"] and "Sandwichez" in fields["supplier"]
        assert fields["invoice_number"] is None or "T001" in fields["invoice_number"]
        assert fields["date"] == date(2025, 5, 16)
        assert fields["total"] == Decimal("3.55")
        assert any(a[1] == Decimal("3.55") for a in fields["amounts"])
        assert fields["payment_method"] == "card"

    def test_extract_fields_spanish(self):
        ocr_raw = [
            {"text": "Sandwichez S.A."},
            {"text": "Factura: T001/207831"},
            {"text": "Fecha: 16/05/2025"},
            {"text": "TOTAL: 3,55 €"},
            {"text": "Pagado con tarjeta."}
        ]
        fields = extract_fields(ocr_raw)
        assert fields["supplier"] and "Sandwichez" in fields["supplier"]
        assert fields["total"] == Decimal("3.55")
        assert any(a[1] == Decimal("3.55") for a in fields["amounts"])
        assert fields["payment_method"] == "card"

    def test_extract_fields_french(self):
        ocr_raw = [
            {"text": "Société Sandwichez"},
            {"text": "Facture: T001/207831"},
            {"text": "Date: 16/05/2025"},
            {"text": "Montant: 3,55 €"},
            {"text": "Paiement par carte."}
        ]
        fields = extract_fields(ocr_raw)
        assert fields["supplier"] and "Sandwichez" in fields["supplier"]
        assert fields["total"] == Decimal("3.55")
        assert any(a[1] == Decimal("3.55") for a in fields["amounts"])
        assert fields["payment_method"] == "card"

    def test_ambiguous_invoice_detection(self):
        ocr_raw = [
            {"text": "Ref T001/207831"},
            {"text": "Sandwichez S.L."},
            {"text": "Paiement: carte"},
            {"text": "Total: 45.00€"}
        ]
        fields = extract_fields(ocr_raw)
        assert fields["invoice_number"] is None or "T001" in fields["invoice_number"]
        assert fields["total"] == Decimal("45.00")
        assert any(a[1] == Decimal("45.00") for a in fields["amounts"])

    def test_no_fields_found(self):
        ocr_raw = [
            {"text": "random gibberish without structure"}
        ]
        fields = extract_fields(ocr_raw)
        assert fields["supplier"] is None
        assert fields["invoice_number"] is None
        assert fields["date"] is None
        assert fields["total"] is None
        assert fields["amounts"] == []
        assert fields["payment_method"] is None
