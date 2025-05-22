import re
from decimal import Decimal
from typing import Optional, List, Tuple

class AmountParser:
    def __init__(self):
        self.currency_symbols = r"€|\$|COP\$?|USD|EUR|COP"
        self.amount_pattern = r"(\d{1,3}(?:[.,\s]?\d{3})*[.,\s]\d{2}|\d+[.,]\d{2})"
        self.patterns = [
            re.compile(rf"{self.currency_symbols}\s?{self.amount_pattern}", re.IGNORECASE),
            re.compile(rf"{self.amount_pattern}\s?{self.currency_symbols}", re.IGNORECASE),
        ]
        self.currency_pattern = re.compile(
            rf"(?P<before>{self.currency_symbols})?\s*(?P<amount>{self.amount_pattern})\s*(?P<after>{self.currency_symbols})?",
            re.IGNORECASE
        )


    def normalize_amount(self, raw: str) -> Optional[Decimal]:
        raw = raw.replace(" ", "")
        if re.match(r"^\d{1,3}(?:\.\d{3})+,\d{2}$", raw):
            # European: 1.234,56
            raw = raw.replace(".", "").replace(",", ".")
        elif re.match(r"^\d{1,3}(?:,\d{3})+\.\d{2}$", raw):
            # US: 1,234.56
            raw = raw.replace(",", "")
        elif "," in raw and "." not in raw:
            # Plain European: 1234,56
            raw = raw.replace(",", ".")
        else:
            # Fallback: remove thousands separator if present
            raw = raw.replace(",", "")
        try:
            return Decimal(raw)
        except Exception:
            return None


    def extract_amounts_with_context(self, ocr_raw: List[dict]) -> List[Tuple[str, Decimal]]:
        results = []

        for entry in ocr_raw:
            text = entry["text"]
            for match in self.currency_pattern.finditer(text):
                print(match.group("before"))
                print(match.group("amount"))
                print(match.group("after"))
                raw_amount = match.group("amount")
                if raw_amount:
                    amount = self.normalize_amount(raw_amount)
                    if amount is not None:
                        results.append((text, amount))
        return results


    def guess_total(self, amounts_with_context: List[Tuple[str, Decimal]]) -> Optional[Decimal]:
        scored = []
        for context, amount in amounts_with_context:
            score = 0
            ctx = context.lower()
            if "total" in ctx: score += 5
            if "payer" in ctx or "due" in ctx: score += 3
            if "ttc" in ctx: score += 2
            if "net" in ctx: score += 1
            if "remise" in ctx or "discount" in ctx: score -= 1
            if "tva" in ctx or "tax" in ctx: score -= 2
            scored.append((score, amount, context))
        if scored:
            scored.sort(reverse=True)
            return scored[0][1]
        return None
