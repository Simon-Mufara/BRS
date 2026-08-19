"""
Payment Request PDF Generator
==============================
Generates deposit and final-balance payment requests.
"""

from __future__ import annotations

from fpdf import FPDF

import brs_agent.config as C
from brs_agent.utils import (
    BRSBase, sf,
    section_title,
    key_value,
    table_header,
    table_row,
    total_row,
    bank_details_block,
    signature_block,
    safe_text,
)


OPTIONAL_KEYS = {
    "client_name": "",
    "client_address": "",
    "quotation_ref": "",
    "total_project_value": 0.0,
    "payment_type": "deposit",
    "payment_pct": 50,
    "payment_amount": None,  # Optional Rand amount for payment
    "deposit_description": "Material Procurement & Delivery",
    "works_start": "",
    "date_issued": None,
    "bank": C.DEFAULT_BANK,
    "payment_ref": "",
    "custom_note": "",
}


class PaymentRequestGenerator:

    def __init__(self):
        self.pdf: FPDF | None = None
        self.data: dict = {}

    def build(self, data: dict) -> FPDF:
        self.data = {**OPTIONAL_KEYS, **data}
        d = self.data

        # Validate required fields
        required_fields = ["client_name", "client_address", "quotation_ref", "total_project_value"]
        for field in required_fields:
            if not self.data.get(field) and self.data.get(field) != 0:  # Allow 0 for total_project_value
                raise ValueError(f"Missing required field: {field}")

        pdf = BRSBase(show_header=False)
        pdf.set_auto_page_break(auto=True, margin=22)
        pdf.add_page()

        # ── Header ───────────────────────────────────────────────────────
        sf(pdf, C.STYLE_BOLD, 10)
        pdf.set_text_color(*C.BRAND_DARK)
        pdf.cell(0, 5, C.COMPANY_NAME, new_x="LMARGIN", new_y="NEXT")
        sf(pdf, "", 7)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 4, safe_text(f"Reg: {C.REG_NUMBER}  ·  {C.ADDRESS_LINE1}  ·  {C.EMAIL}"),
                 new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1)
        sf(pdf, C.STYLE_ITALIC, 7)
        pdf.cell(0, 4, f'"{C.TAGLINE}"', new_x="LMARGIN", new_y="NEXT")
        pdf.ln(3)

        # ── Title ────────────────────────────────────────────────────────
        sf(pdf, C.STYLE_BOLD, 14)
        pdf.set_text_color(*C.BRAND_ACCENT)
        pdf.cell(0, 8, "PAYMENT REQUEST", new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(*C.BRAND_DARK)

        payment_label = d["deposit_description"]
        sf(pdf, "", 9)
        pdf.cell(0, 5, payment_label, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(3)

        # ── Meta block ───────────────────────────────────────────────────
        section_title(pdf, "RECIPIENT & REFERENCE")
        key_value(pdf, "TO:", d["client_name"])
        key_value(pdf, "", d["client_address"])
        key_value(pdf, "Date:", C.date_issued(d["date_issued"]))
        key_value(pdf, "Quotation Ref:", d["quotation_ref"])
        key_value(pdf, "Works Start:", d["works_start"])
        pdf.ln(3)

        # ── Payment Breakdown ────────────────────────────────────────────
        section_title(pdf, "PAYMENT BREAKDOWN")

        total = float(d["total_project_value"])
        # Use payment_amount if provided, otherwise calculate from payment_pct
        if d.get("payment_amount") is not None:
            amount = float(d["payment_amount"])
            pct = (amount / total) * 100 if total > 0 else 0
        else:
            pct = float(d["payment_pct"]) / 100.0
            amount = total * pct
        balance = total - amount

        cols = [("Description", 110, "L"), ("Amount (ZAR)", 45, "R")]
        table_header(pdf, cols)
        table_row(pdf, [
            (f"Total project value (as per quotation {d['quotation_ref']})", 110, "L"),
            (f"R{total:,.2f}", 45, "R"),
        ])
        # Format payment description to show both percentage and amount for clarity
        # Calculate effective percentage for display (works with both payment_pct and payment_amount)
        effective_pct = float(d["payment_pct"]) if d.get("payment_amount") is None else (float(d["payment_amount"]) / total * 100)
        if effective_pct == 100:
            payment_line = f"{d['deposit_description']} — 100% (R{amount:,.2f})"
        else:
            payment_line = f"{d['deposit_description']} ({effective_pct:g}% — R{amount:,.2f})"

        table_row(pdf, [
            (f"{payment_line} — required for {d['deposit_description'].lower()}", 110, "L"),
            (f"R{amount:,.2f}", 45, "R"),
        ])
        pdf.ln(1)
        total_row(pdf, "AMOUNT DUE NOW", f"R{amount:,.2f}", cols)
        pdf.ln(1)

        sf(pdf, C.STYLE_ITALIC, 7.5)
        pdf.cell(0, 4, f"Balance due on completion:  R{balance:,.2f}", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(3)

        # ── Banking Details ──────────────────────────────────────────────
        bank_details_block(pdf, d["bank"])

        # Payment ref note
        if d["payment_ref"]:
            sf(pdf, "", 7.5)
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(0, 4,
                f'Please use the above reference ({d["payment_ref"]}) and send proof of payment to {C.EMAIL}.')
            if d["custom_note"]:
                pdf.set_x(pdf.l_margin)
                pdf.multi_cell(0, 4, d["custom_note"])
            pdf.ln(2)

        # ── Client Acknowledgement ───────────────────────────────────────
        signature_block(pdf, "Client Acknowledgement")

        self.pdf = pdf
        return pdf

    def save(self, path: str) -> str:
        if self.pdf is None:
            raise RuntimeError("Call build() before save()")
        self.pdf.output(path)
        return path
