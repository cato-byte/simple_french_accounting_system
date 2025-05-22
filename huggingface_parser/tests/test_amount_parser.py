import pytest
from decimal import Decimal
from amount_parser import AmountParser  # Adjust path if needed

parser = AmountParser()

@pytest.mark.parametrize("ocr_raw, expected", [
    (
        [{"text": "Total: $1,234.56"}],
        [("Total: $1,234.56", Decimal("1234.56"))]
    ),
    (
        [{"text": "Amount due: USD 987.65"}, {"text": "Discount: $12.00"}],
        [("Amount due: USD 987.65", Decimal("987.65")), ("Discount: $12.00", Decimal("12.00"))]
    ),
])
def test_extract_english(ocr_raw, expected):
    result = parser.extract_amounts_with_context(ocr_raw)
    assert sorted(result) == sorted(expected)


@pytest.mark.parametrize("ocr_raw, expected", [
    (
        [{"text": "Total à payer: 1 234,56 €"}],
        [("Total à payer: 1 234,56 €", Decimal("1234.56"))]
    ),
    (
        [{"text": "Remise: 10,00 €"}, {"text": "Montant TTC: €1.244,56"}],
        [("Remise: 10,00 €", Decimal("10.00")), ("Montant TTC: €1.244,56", Decimal("1244.56"))]
    ),
])
def test_extract_french(ocr_raw, expected):
    result = parser.extract_amounts_with_context(ocr_raw)
    assert sorted(result) == sorted(expected)


@pytest.mark.parametrize("ocr_raw, expected", [
    (
        [{"text": "Total a pagar: COP 1.234,56"}],
        [("Total a pagar: COP 1.234,56", Decimal("1234.56"))]
    ),
    (
        [{"text": "Importe: 999,99 COP"}, {"text": "Descuento: 20,00"}],
        [("Importe: 999,99 COP", Decimal("999.99")), ("Descuento: 20,00", Decimal("20.00"))]
    ),
])
def test_extract_spanish(ocr_raw, expected):
    result = parser.extract_amounts_with_context(ocr_raw)
    assert sorted(result) == sorted(expected)


def test_guess_total_logic():
    ocr_raw = [
        {"text": "Subtotal: $1,000.00"},
        {"text": "Tax: $200.00"},
        {"text": "Total to pay: $1,200.00"},
        {"text": "Discount: $50.00"},
    ]
    amounts = parser.extract_amounts_with_context(ocr_raw)
    total = parser.guess_total(amounts)
    assert total == Decimal("1200.00")
