import re
from datetime import datetime

class DateParser:
    MONTHS = {
        "en": ["january", "february", "march", "april", "may", "june",
               "july", "august", "september", "october", "november", "december"],
        "fr": ["janvier", "février", "mars", "avril", "mai", "juin",
               "juillet", "août", "septembre", "octobre", "novembre", "décembre"],
        "es": ["enero", "febrero", "marzo", "abril", "mayo", "junio",
               "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    }

    def __init__(self):
        # Create a lookup for month name → month number
        self.month_lookup = {
            name.lower(): i + 1
            for lang_months in self.MONTHS.values()
            for i, name in enumerate(lang_months)
        }

        # Build month regex pattern sorted by length
        months_flat = sorted(self.month_lookup.keys(), key=len, reverse=True)
        self.month_regex = r"|".join(months_flat)

        # Precompile patterns
        self.patterns = [
            # 16/05/2025 or 16-05-2025
            (re.compile(r"\b(\d{2})[/-](\d{2})[/-](\d{4})\b"), "%d/%m/%Y"),
            # 2025-05-16
            (re.compile(r"\b(\d{4})[/-](\d{2})[/-](\d{2})\b"), "%Y-%m-%d"),
            # 16 May 2025, 16 mai 2025, 25 de mayo de 2025
            (re.compile(
                rf"\b(\d{{1,2}})\s+(?:de\s+)?({self.month_regex})\s+(?:de\s+)?(\d{{4}})\b",
                re.IGNORECASE
            ), "textual"),
            # May 16, 2025 or mai 16 2025 with optional comma
            (re.compile(
                rf"\b({self.month_regex})\s+(\d{{1,2}})[,]?\s*(\d{{4}})\b",
                re.IGNORECASE
            ), "textual"),
            # 05/2025 or 5/2025
            (re.compile(r"\b(\d{1,2})[/-](\d{4})\b"), "%m/%Y"),
            # mai 2025 or mayo 2025 (partial textual)
            (re.compile(
                rf"\b({self.month_regex})\s+(\d{{4}})\b",
                re.IGNORECASE
            ), "partial_textual"),
        ]
    

    def parse(self, text: str):
        for pattern, fmt in self.patterns:
            match = pattern.search(text)
            if not match:
                continue
            try:
                if fmt == "%d/%m/%Y" or fmt == "%Y-%m-%d":
                    return datetime.strptime(match.group(0), fmt).date()
                elif fmt == "%m/%Y":
                    month, year = match.groups()
                    return datetime(int(year), int(month), 1).date()
                elif fmt == "textual":
                    g = match.groups()
                    if len(g) == 3:
                        if g[0].isdigit():
                            # 25 de mayo de 2025
                            day, month_str, year = g
                        else:
                            # mayo 25 2025
                            month_str, day, year = g
                        month_num = self.month_lookup.get(month_str.lower())
                        if month_num:
                            return datetime(int(year), int(month_num), int(day)).date()
                elif fmt == "partial_textual":
                    month_str, year = match.groups()
                    month_num = self.month_lookup.get(month_str.lower())
                    if month_num:
                        return datetime(int(year), int(month_num), 1).date()
            except Exception:
                continue
        return None