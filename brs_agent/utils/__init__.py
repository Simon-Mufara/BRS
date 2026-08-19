"""
PDF helper utilities — reusable drawing primitives for fpdf2.
"""
from __future__ import annotations

from fpdf import FPDF

import re
import brs_agent.config as C


def safe_text(text: str) -> str:
    """Replace Unicode characters unsupported by built-in Helvetica with ASCII equivalents."""
    replacements = {
        '\u2014': '--',   # em dash
        '\u2013': '-',    # en dash
        '\u2018': "'",    # left single quote
        '\u2019': "'",    # right single quote
        '\u201c': '"',    # left double quote
        '\u201d': '"',    # right double quote
        '\u2022': '*',    # bullet
        '\u2713': '[x]',  # check mark
        '\u2714': '[x]',  # heavy check mark
        '\u2302': '|',    # house
        '\u2501': '-',    # box drawing
        '\u2610': '[ ]',  # ballot box
        '\u00b7': '*',    # middle dot
    }
    for orig, repl in replacements.items():
        text = text.replace(orig, repl)
    return text


def sf(pdf: FPDF, style: str = "", size: int = 8):
    """Shorthand: set_font with Helvetica + style + size."""
    pdf.set_font(C.FONT_REGULAR, style, size)


class BRSBase(FPDF):
    """Base PDF class with common header / footer for BuildRight Solutions."""

    def __init__(self, show_header: bool = True, show_footer: bool = True, **kw):
        super().__init__(**kw)
        self._show_header = show_header
        self._show_footer = show_footer

    # ── Auto-sanitize text for built-in Helvetica (no Unicode support)
    def cell(self, w, h=0, text="", **kw):
        if isinstance(text, str):
            text = safe_text(text)
        return super().cell(w, h, text, **kw)

    def multi_cell(self, w, h=0, text="", **kw):
        if isinstance(text, str):
            text = safe_text(text)
        return super().multi_cell(w, h, text, **kw)

    # ── Header ───────────────────────────────────────────────────────────
    def header(self):
        if not self._show_header:
            return
        sf(self, C.STYLE_BOLD, 9)
        self.set_text_color(*C.BRAND_DARK)
        self.cell(0, 5, C.COMPANY_NAME, new_x="LMARGIN", new_y="NEXT")
        sf(self, "", 7)
        self.set_text_color(100, 100, 100)
        self.cell(0, 4, f"Reg: {C.REG_NUMBER}  ·  {C.ADDRESS_LINE1}  ·  {C.EMAIL}",
                  new_x="LMARGIN", new_y="NEXT")
        sf(self, C.STYLE_ITALIC, 7)
        self.cell(0, 4, f'"{C.TAGLINE}"', new_x="LMARGIN", new_y="NEXT")
        self.ln(2)
        # Accent rule
        self.set_draw_color(*C.BRAND_ACCENT)
        self.set_line_width(0.6)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(4)

    # ── Footer ───────────────────────────────────────────────────────────
    def footer(self):
        if not self._show_footer:
            return
        self.set_y(-18)
        self.set_draw_color(*C.BRAND_ACCENT)
        self.set_line_width(0.3)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(2)
        sf(self, "", 6)
        self.set_text_color(120, 120, 120)
        self.cell(0, 3, f"{C.COMPANY_NAME}  ·  {C.ADDRESS_LINE1}  ·  {C.EMAIL}  ·  Reg {C.REG_NUMBER}",
                  align="C")


# ── Drawing helpers (free functions) ─────────────────────────────────────────

def section_title(pdf: FPDF, title: str):
    """Draw a teal-background section title."""
    sf(pdf, C.STYLE_BOLD, 10)
    pdf.set_fill_color(*C.BRAND_ACCENT)
    pdf.set_text_color(*C.BRAND_WHITE)
    pdf.cell(0, 8, f"  {title}", fill=True, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.set_text_color(*C.BRAND_DARK)


def subsection_title(pdf: FPDF, title: str):
    """Draw a bold sub-section title with a thin underline."""
    sf(pdf, C.STYLE_BOLD, 9)
    pdf.set_text_color(*C.BRAND_PRIMARY)
    pdf.cell(0, 6, title, new_x="LMARGIN", new_y="NEXT")
    pdf.set_draw_color(200, 200, 200)
    pdf.set_line_width(0.2)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
    pdf.ln(2)
    pdf.set_text_color(*C.BRAND_DARK)


def key_value(pdf: FPDF, key: str, value: str, key_w: int = 45, val_w: int = 130):
    """Print a key: value pair (label right-aligned, value left-aligned)."""
    sf(pdf, C.STYLE_BOLD, 8)
    pdf.cell(key_w, 5, key, align="R")
    sf(pdf, "", 8)
    pdf.cell(val_w, 5, f"  {value}", new_x="LMARGIN", new_y="NEXT")


def table_header(pdf: FPDF, cols: list[tuple[str, int, str]], fill: bool = True):
    """
    Draw a table header row.
    cols = [(label, width, align), ...]
    """
    sf(pdf, C.STYLE_BOLD, 8)
    pdf.set_fill_color(*C.BRAND_PRIMARY)
    pdf.set_text_color(*C.BRAND_WHITE)
    for label, w, align in cols:
        pdf.cell(w, 7, f"  {label}", fill=fill, align=align)
    pdf.ln()
    pdf.set_text_color(*C.BRAND_DARK)


def table_row(pdf: FPDF, cells: list[tuple[str, int, str]], bold: bool = False, fill: bool = False):
    """Draw a single table data row."""
    style = C.STYLE_BOLD if bold else ""
    sf(pdf, style, 8)
    if fill:
        pdf.set_fill_color(*C.BRAND_LIGHT)
    for val, w, align in cells:
        pdf.cell(w, 6, f"  {val}", fill=fill, align=align)
    pdf.ln()


def total_row(pdf: FPDF, label: str, value: str, cols: list[tuple[str, int, str]]):
    """Draw a bold total / grand-total row."""
    sf(pdf, C.STYLE_BOLD, 9)
    pdf.set_fill_color(*C.BRAND_ACCENT)
    pdf.set_text_color(*C.BRAND_WHITE)
    # span all columns before the last two (label, value)
    for _, w, _ in cols[:-2]:
        pdf.cell(w, 7, "", fill=True)
    label_w = cols[-2][1]
    val_w = cols[-1][1]
    pdf.cell(label_w, 7, f"  {label}", fill=True, align=cols[-2][2])
    pdf.cell(val_w, 7, f"  {value}", fill=True, align=cols[-1][2])
    pdf.ln()
    pdf.set_text_color(*C.BRAND_DARK)
    pdf.ln(1)


def bank_details_block(pdf: FPDF, bank_key: str = C.DEFAULT_BANK):
    """Render the banking details block."""
    b = C.BANK_ACCOUNTS[bank_key]
    section_title(pdf, "BANKING DETAILS")
    key_value(pdf, "Account Holder:", b["holder"])
    key_value(pdf, "Business Name:", b["business"])
    key_value(pdf, "Bank:", b["bank"])
    key_value(pdf, "Account Number:", b["account_number"])
    key_value(pdf, "Account Type:", b["account_type"])
    key_value(pdf, "Branch Code:", b["branch_code"])
    pdf.ln(3)


def signature_block(pdf: FPDF, title: str = "Client Acknowledgement"):
    """Draw a signature block."""
    pdf.ln(5)
    section_title(pdf, title)
    sf(pdf, "", 8)
    pdf.multi_cell(0, 5, "By signing below, I confirm receipt of this document and agree to the terms outlined above.")
    pdf.ln(8)
    pdf.cell(90, 5, "Signature: _______________________")
    pdf.cell(90, 5, "Date: _______________________", new_x="LMARGIN", new_y="NEXT")
