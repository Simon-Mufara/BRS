"""
BuildRight Solutions (Pty) Ltd — Company Configuration
======================================================
Central place for all company details, banking info, and document settings.
Edit this file once; every generator picks up the changes automatically.
"""

from datetime import date, timedelta

# ── Company Identity ────────────────────────────────────────────────────────
COMPANY_NAME = "BuildRight Solutions (Pty) Ltd"
COMPANY_SHORT = "BuildRight Solutions"
TAGLINE = "We Nail It, You Enjoy It!"
REG_NUMBER = "2026/110944/07"
ADDRESS_LINE1 = "Zandspruit, Honeydew, Gauteng"
EMAIL = "buildright.solutions.agency@gmail.com"

# ── Director / Prepared By ──────────────────────────────────────────────────
DIRECTOR_NAME = "A. Simon Mufara"
DIRECTOR_TITLE = "Director"

# ── Banking Details ──────────────────────────────────────────────────────────
BANK_ACCOUNTS = {
    "fnb": {
        "holder": "Azwinndini S Mufara",
        "business": COMPANY_SHORT,
        "bank": "FNB",
        "account_number": "63223571464",
        "account_type": "FNB Aspire Account",
        "branch_code": "250655",
    },
    "capitec": {
        "holder": "Azwinndini S Mufara",
        "business": COMPANY_SHORT,
        "bank": "Capitec Bank",
        "account_number": "2528097685",
        "account_type": "Entrepreneur (Business)",
        "branch_code": "470010",
    },
}

DEFAULT_BANK = "fnb"  # Which account to show by default

# ── Document Settings ───────────────────────────────────────────────────────
QUOTATION_VALIDITY_DAYS = 30
CURRENCY = "ZAR"
CURRENCY_SYMBOL = "R"

# ── Reference Number Format ─────────────────────────────────────────────────
# BRS-YYYY-MMDD-X  where X is a project/sequence letter
def generate_ref(project_letter: str = "E", d: date | None = None) -> str:
    """Generate a quotation reference number like BRS-2026-0729-E."""
    d = d or date.today()
    return f"BRS-{d.year}-{d.month:02d}{d.day:02d}-{project_letter}"


# ── Date Helpers ─────────────────────────────────────────────────────────────
def date_issued(d: date | None = None) -> str:
    d = d or date.today()
    return d.strftime("%d %B %Y")

def validity_date(d: date | None = None) -> str:
    d = d or date.today()
    return (d + timedelta(days=QUOTATION_VALIDITY_DAYS)).strftime("%d %B %Y")

# ── PDF Appearance ──────────────────────────────────────────────────────────
BRAND_DARK   = (30, 30, 30)       # near-black
BRAND_PRIMARY = (44, 62, 80)      # dark blue-grey
BRAND_ACCENT  = (22, 160, 133)    # teal
BRAND_LIGHT   = (236, 240, 241)   # light grey
BRAND_WHITE   = (255, 255, 255)

FONT_REGULAR = "Helvetica"
FONT_BOLD    = "Helvetica"
FONT_ITALIC  = "Helvetica"
STYLE_REGULAR = ""
STYLE_BOLD    = "B"
STYLE_ITALIC  = "I"
