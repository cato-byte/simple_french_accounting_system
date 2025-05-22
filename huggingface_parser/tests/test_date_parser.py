import pytest
from datetime import date
from date_parser import DateParser  # Adjust this import to your actual module path

parser = DateParser()

test_cases = [
    ("16/05/2025", date(2025, 5, 16)),
    ("2025-05-16", date(2025, 5, 16)),
    ("16 May 2025", date(2025, 5, 16)),
    ("16 mai 2025", date(2025, 5, 16)),
    ("25 de mayo de 2025", date(2025, 5, 25)),
    ("Mayo 25, 2025", date(2025, 5, 25)),
    ("mai 2025", date(2025, 5, 1)),
    ("mayo 2025", date(2025, 5, 1)),
    ("05/2025", date(2025, 5, 1)),
    ("5/2025", date(2025, 5, 1)),
    ("4 avril 2022", date(2022, 4, 4)),
    ("avril 2022", date(2022, 4, 1)),
    ("April 16, 2025", date(2025, 4, 16)),
]

@pytest.mark.parametrize("text, expected_date", test_cases)
def test_date_parser(text, expected_date):
    parsed = parser.parse(text)
    assert parsed == expected_date, f"Expected {expected_date} from '{text}', but got {parsed}"