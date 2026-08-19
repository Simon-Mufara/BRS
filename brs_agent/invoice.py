"""
Invoice PDF Generator
======================
Generates professional invoices for completed work or staged payments.
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
)


OPTIONAL_KEYS = {
    "client_name": "",
    "client_address": "",
    "invoice_number": None,
    "quotation_ref": "",
    "project_title": "Works Completed",
    "date_issued": None,
    "due_date": None,
    "line_items": [],
    "subtotal": None,
    "vat_rate": 0.0,
    "discount_label": None,
    "discount_amount": 0.0,
    "bank": C.DEFAULT_BANK,
    "notes": "",
    "tax_number": "RP123456789",
}


def _next_invoice_number() -> str:
    import json, os
    state_file = os.path.join(os.path.dirname(__file__), "data", "invoice_counter.json")
    os.makedirs(os.path.dirname(state_file), exist_ok=True)
    counter = 0
    if os.path.exists(state_file):
        with open(state_file) as f:
            counter = json.load(f).get("counter", 0)
    counter += 1
    with open(state_file, "w") as f:
        json.dump({"counter": counter}, f)
    return f"BRS-INV-{counter:04d}"


def reset_invoice_counter():
    """Reset the invoice counter to 0."""
    import json, os
    state_file = os.path.join(os.path.dirname(__file__), "data", "invoice_counter.json")
    os.makedirs(os.path.dirname(state_file), exist_ok=True)
    with open(state_file, "w") as f:
        json.dump({"counter": 0}, f)


class InvoiceGenerator:

    def __init__(self):
        self.pdf: FPDF | None = None
        self.data: dict = {}

    def build(self, data: dict) -> FPDF:
        self.data = {**OPTIONAL_KEYS, **data}
        d = self.data

        # Validate required fields
        required_fields = ["client_name", "client_address"]
        for field in required_fields:
            if not self.data.get(field):
                raise ValueError(f"Missing required field: {field}")

        # Handle date_issued - convert string to date object if needed
        if isinstance(d["date_issued"], str):
            try:
                from datetime import datetime
                # Try common date formats
                for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d %B %Y", "%B %d, %Y"):
                    try:
                        d["date_issued"] = datetime.strptime(d["date_issued"], fmt).date()
                        break
                    except ValueError:
                        continue
                else:
                    # If none of the formats worked, set to None (will use today's date)
                    d["date_issued"] = None
            except Exception:
                d["date_issued"] = None

        if d["invoice_number"] is None:
            d["invoice_number"] = _next_invoice_number()
        if d["due_date"] is None:
            from datetime import date, timedelta
            d["due_date"] = (date.today() + timedelta(days=30)).strftime("%d %B %Y")

        pdf = BRSBase()
        pdf.set_auto_page_break(auto=True, margin=22)
        pdf.add_page()

        # ── Title ────────────────────────────────────────────────────────
        sf(pdf, C.STYLE_BOLD, 16)
        pdf.set_text_color(*C.BRAND_ACCENT)
        pdf.cell(0, 10, "INVOICE", new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(*C.BRAND_DARK)

        # ── Meta ─────────────────────────────────────────────────────────
        section_title(pdf, "INVOICE DETAILS")
        key_value(pdf, "Invoice No:", d["invoice_number"])
        key_value(pdf, "Date Issued:", C.date_issued(d["date_issued"]))
        key_value(pdf, "Due Date:", d["due_date"])
        key_value(pdf, "Quotation Ref:", d["quotation_ref"])
        pdf.ln(3)

        # ── Bill To ──────────────────────────────────────────────────────
        section_title(pdf, "BILL TO")
        key_value(pdf, "Client:", d["client_name"])
        key_value(pdf, "Address:", d["client_address"])
        pdf.ln(3)

        # ── Line Items ───────────────────────────────────────────────────
        section_title(pdf, "LINE ITEMS")
        cols = [("Description", 70, "L"), ("Qty", 20, "C"), ("Rate (ZAR)", 35, "R"), ("Amount (ZAR)", 35, "R")]
        table_header(pdf, cols)

        subtotal = 0.0
        for item in d["line_items"]:
            amount = float(item.get("amount", float(item.get("rate", 0)) * float(item.get("qty", 1))))
            subtotal += amount
            rate = float(item.get("rate", amount / max(float(item.get("qty", 1)), 1)))
            table_row(pdf, [
                (item["desc"], 70, "L"),
                (str(item.get("qty", "")), 20, "C"),
                (f"R {rate:,.2f}", 35, "R"),
                (f"R {amount:,.2f}", 35, "R"),
            ])

        if d["subtotal"] is not None:
            subtotal = float(d["subtotal"])

        # Subtotal
        table_row(pdf, [
            ("Subtotal", 90, "R"),
            (f"R {subtotal:,.2f}", 35, "R"),
        ], bold=True, fill=True)

        # Discount
        discount = float(d.get("discount_amount", 0))
        if discount > 0:
            table_row(pdf, [
                (d.get("discount_label", "Discount"), 90, "R"),
                (f"- R {discount:,.2f}", 35, "R"),
            ])
            subtotal -= discount

        # VAT
        vat = subtotal * float(d["vat_rate"])
        if vat > 0:
            table_row(pdf, [
                (f"VAT ({int(d['vat_rate']*100)}%)", 90, "R"),
                (f"R {vat:,.2f}", 35, "R"),
            ])

        grand = subtotal + vat

        # Grand Total
        total_row(pdf, "TOTAL DUE", f"R {grand:,.2f}", cols)

        pdf.ln(3)

        # ── Notes ────────────────────────────────────────────────────────
        if d["notes"]:
            section_title(pdf, "NOTES")
            sf(pdf, "", 8)
            pdf.multi_cell(0, 4.5, d["notes"])
            pdf.ln(3)

        # ── Banking Details ──────────────────────────────────────────────
        bank_details_block(pdf, d["bank"])

        # ── Payment instructions ─────────────────────────────────────────
        sf(pdf, "", 7.5)
        pdf.multi_cell(0, 4,
            f'Please use invoice number {d["invoice_number"]} as payment reference. '
            f'Send proof of payment to {C.EMAIL}.')
        pdf.ln(3)

        # ── Signature ────────────────────────────────────────────────────
        sf(pdf, C.STYLE_BOLD, 8)
        pdf.cell(90, 5, f"Authorised by: {C.DIRECTOR_NAME}")
        pdf.cell(90, 5, "Date: _______________________", new_x="LMARGIN", new_y="NEXT")
        sf(pdf, "", 7)
        pdf.cell(90, 5, f"{C.DIRECTOR_TITLE}, {C.COMPANY_SHORT}")

        self.pdf = pdf
        return pdf

    def save(self, path: str) -> str:
        if self.pdf is None:
            raise RuntimeError("Call build() before save()")
        self.pdf.output(path)
        return path
