"""
Delivery Note PDF Generator
============================
Generates delivery notes for material drop-offs to client sites.
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
)


OPTIONAL_KEYS = {
    "client_name": "",
    "client_address": "",
    "quotation_ref": "",
    "delivery_date": None,
    "site_address": "",
    "items": [],
    "delivered_by": C.DIRECTOR_NAME,
    "vehicle_ref": "",
    "notes": "",
}


def _next_dn_number() -> str:
    import json, os
    state_file = os.path.join(os.path.dirname(__file__), "data", "dn_counter.json")
    os.makedirs(os.path.dirname(state_file), exist_ok=True)
    counter = 0
    if os.path.exists(state_file):
        with open(state_file) as f:
            counter = json.load(f).get("counter", 0)
    counter += 1
    with open(state_file, "w") as f:
        json.dump({"counter": counter}, f)
    return f"BRS-DN-{counter:04d}"


def reset_dn_counter():
    """Reset the delivery note counter to 0."""
    import json, os
    state_file = os.path.join(os.path.dirname(__file__), "data", "dn_counter.json")
    os.makedirs(os.path.dirname(state_file), exist_ok=True)
    with open(state_file, "w") as f:
        json.dump({"counter": 0}, f)


class DeliveryNoteGenerator:

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

        # Handle delivery_date - convert string to date object if needed
        if isinstance(d["delivery_date"], str):
            try:
                from datetime import datetime
                # Try common date formats
                for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d %B %Y", "%B %d, %Y"):
                    try:
                        d["delivery_date"] = datetime.strptime(d["delivery_date"], fmt).date()
                        break
                    except ValueError:
                        continue
                else:
                    # If none of the formats worked, set to None
                    d["delivery_date"] = None
            except Exception:
                d["delivery_date"] = None

        dn_number = _next_dn_number()

        pdf = BRSBase(show_header=True)
        pdf.set_auto_page_break(auto=True, margin=22)
        pdf.add_page()

        # ── Title ────────────────────────────────────────────────────────
        sf(pdf, C.STYLE_BOLD, 14)
        pdf.set_text_color(*C.BRAND_ACCENT)
        pdf.cell(0, 8, "DELIVERY NOTE", new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(*C.BRAND_DARK)
        pdf.ln(2)

        # ── Meta ─────────────────────────────────────────────────────────
        key_value(pdf, "Delivery Note No:", dn_number)
        key_value(pdf, "Date:", C.date_issued(d["delivery_date"]))
        key_value(pdf, "Quotation Ref:", d["quotation_ref"])
        pdf.ln(2)

        # ── Delivery Info ────────────────────────────────────────────────
        section_title(pdf, "DELIVERY INFORMATION")
        key_value(pdf, "Client:", d["client_name"])
        key_value(pdf, "Site Address:", d.get("site_address", d["client_address"]))
        key_value(pdf, "Delivered By:", d["delivered_by"])
        if d["vehicle_ref"]:
            key_value(pdf, "Vehicle:", d["vehicle_ref"])
        pdf.ln(3)

        # ── Items ────────────────────────────────────────────────────────
        section_title(pdf, "ITEMS DELIVERED")
        cols = [
            ("#", 10, "C"),
            ("Description", 75, "L"),
            ("Qty", 20, "C"),
            ("Unit", 25, "L"),
            ("Notes", 40, "L"),
            ("Received", 20, "C"),
        ]
        table_header(pdf, cols)
        for i, item in enumerate(d["items"], 1):
            table_row(pdf, [
                (str(i), 10, "C"),
                (item["desc"], 75, "L"),
                (str(item.get("qty", "")), 20, "C"),
                (item.get("unit", ""), 25, "L"),
                (item.get("notes", "")[:35], 40, "L"),
                ("☐", 20, "C"),
            ])
        pdf.ln(3)

        # ── Notes ────────────────────────────────────────────────────────
        if d["notes"]:
            section_title(pdf, "NOTES")
            sf(pdf, "", 8)
            pdf.multi_cell(0, 4.5, d["notes"])
            pdf.ln(3)

        # ── Signatures ───────────────────────────────────────────────────
        pdf.ln(5)
        section_title(pdf, "ACKNOWLEDGEMENT OF DELIVERY")
        sf(pdf, "", 8)
        pdf.multi_cell(0, 4.5,
            "I confirm receipt of the items listed above in good condition unless noted otherwise.")
        pdf.ln(8)

        pdf.cell(90, 5, "Delivered by: _______________________")
        pdf.cell(90, 5, "Received by: _______________________", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(3)
        pdf.cell(90, 5, "Date: _______________________")
        pdf.cell(90, 5, "Date: _______________________", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(3)
        pdf.cell(90, 5, "Signature: _______________________")
        pdf.cell(90, 5, "Signature: _______________________", new_x="LMARGIN", new_y="NEXT")

        self.pdf = pdf
        return pdf

    def save(self, path: str) -> str:
        if self.pdf is None:
            raise RuntimeError("Call build() before save()")
        self.pdf.output(path)
        return path
