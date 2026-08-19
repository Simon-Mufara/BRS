"""
Quotation PDF Generator
=======================
Generates professional quotations matching BuildRight Solutions' two document styles:
  - Style A (Tabular):  "OFFICIAL QUOTATION" header — used for crack repair, painting, etc.
  - Style B (Clean):    BUILD RIGHT header — used for tiling, multi-scope, etc.

Usage:
    from brs_agent.quotation import QuotationGenerator

    gen = QuotationGenerator()
    gen.build(data)
    gen.save("output/my_quotation.pdf")
"""

from __future__ import annotations

from fpdf import FPDF

import brs_agent.config as C
from brs_agent.utils import (
    BRSBase, sf,
    section_title,
    subsection_title,
    key_value,
    table_header,
    table_row,
    total_row,
    bank_details_block,
    signature_block,
    safe_text,
)


# ── Quotation Data Model ────────────────────────────────────────────────────

OPTIONAL_KEYS = {
    "client_name": "",
    "client_address": "",
    "project_description": "",
    "project_title": "Tiling, Waterproofing & Painting",
    "ref": None,
    "project_letter": "E",
    "date_issued": None,
    "validity_days": C.QUOTATION_VALIDITY_DAYS,
    "projected_start": "TBC (subject to site survey)",
    "measurements": [],
    "materials": [],
    "labour": [],
    "material_notes": [],
    "discount_label": None,
    "discount_amount": 0.0,
    "section_totals": [],
    "style": "A",
    "bank": C.DEFAULT_BANK,
    "prepared_by": C.DIRECTOR_NAME,
}


class QuotationGenerator:
    """Build a quotation PDF from a data dict."""

    def __init__(self):
        self.pdf: FPDF | None = None
        self.data: dict = {}

    def build(self, data: dict) -> FPDF:
        self.data = {**OPTIONAL_KEYS, **data}
        if self.data["ref"] is None:
            self.data["ref"] = C.generate_ref(self.data["project_letter"])

        # Validate required fields
        required_fields = ["client_name", "client_address", "project_title", "project_description"]
        for field in required_fields:
            if not self.data.get(field):
                raise ValueError(f"Missing required field: {field}")

        style = self.data.get("style", "A").upper()
        if style == "B":
            self._build_style_b()
        else:
            self._build_style_a()

        return self.pdf

    def save(self, path: str) -> str:
        if self.pdf is None:
            raise RuntimeError("Call build() before save()")
        self.pdf.output(path)
        return path

    # ── Style A — Tabular "OFFICIAL QUOTATION" ──────────────────────────

    def _build_style_a(self):
        d = self.data
        pdf = BRSBase(show_header=False)
        pdf.set_auto_page_break(auto=True, margin=22)
        pdf.add_page()

        # ── Title Banner ─────────────────────────────────────────────────
        sf(pdf, "", 14)
        pdf.set_text_color(*C.BRAND_ACCENT)
        pdf.cell(0, 8, "OFFICIAL QUOTATION", align="R", new_x="LMARGIN", new_y="NEXT")

        sf(pdf, C.STYLE_BOLD, 11)
        pdf.set_text_color(*C.BRAND_DARK)
        pdf.cell(0, 6, d["project_title"], new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1)

        # Company bar
        sf(pdf, C.STYLE_BOLD, 9)
        pdf.cell(0, 5, safe_text(f'{C.COMPANY_NAME}    ·    Reg. No. {C.REG_NUMBER}    ·    {C.ADDRESS_LINE1}'),
                 new_x="LMARGIN", new_y="NEXT")
        sf(pdf, "", 7)
        pdf.cell(0, 4, C.EMAIL, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(3)

        # ── Meta row ─────────────────────────────────────────────────────
        pdf.set_fill_color(*C.BRAND_LIGHT)
        meta = [
            ("QUOTATION REF", d["ref"]),
            ("DATE ISSUED", C.date_issued(d["date_issued"])),
            ("VALID FOR", f'{d["validity_days"]} days'),
            ("PREPARED BY", f'{d["prepared_by"]}\n{C.DIRECTOR_TITLE}'),
        ]
        y_start = pdf.get_y()
        col_w = (pdf.w - pdf.l_margin - pdf.r_margin) / 4
        for i, (lbl, val) in enumerate(meta):
            x = pdf.l_margin + i * col_w
            pdf.set_xy(x, y_start)
            sf(pdf, C.STYLE_BOLD, 7)
            pdf.cell(col_w, 4, lbl, align="C")
            pdf.set_xy(x, y_start + 5)
            sf(pdf, "", 8)
            pdf.multi_cell(col_w, 4, val, align="C")
        pdf.set_y(y_start + 16)
        pdf.ln(2)

        # ── Client Info ──────────────────────────────────────────────────
        section_title(pdf, "CLIENT INFORMATION")
        key_value(pdf, "CLIENT NAME:", d["client_name"])
        key_value(pdf, "PROPERTY ADDRESS:", d["client_address"])
        pdf.ln(2)

        # ── Project Description ──────────────────────────────────────────
        section_title(pdf, "PROJECT DESCRIPTION")
        sf(pdf, "", 8)
        pdf.multi_cell(0, 4.5, d["project_description"])
        pdf.ln(3)

        # ── Measurements ─────────────────────────────────────────────────
        if d["measurements"]:
            section_title(pdf, "MEASUREMENTS — PER CLIENT SKETCH")
            cols_m = [("ELEMENT", 70, "L"), ("DIMENSION", 50, "L"), ("AREA", 50, "L")]
            table_header(pdf, cols_m)
            for m in d["measurements"]:
                table_row(pdf, [
                    (m["element"], 70, "L"),
                    (m["dimension"], 50, "L"),
                    (m.get("area", "as measured"), 50, "L"),
                ])
            sf(pdf, C.STYLE_ITALIC, 6)
            pdf.multi_cell(0, 3.5,
                "Dimensions transcribed from the client's sketch; final quantities confirmed by site survey before commencement.")
            pdf.ln(3)

        # ── Quotation Breakdown ──────────────────────────────────────────
        section_title(pdf, "QUOTATION BREAKDOWN")
        cols = [("ITEM / DESCRIPTION", 75, "L"), ("QTY / SPEC", 40, "L"), ("COST (ZAR)", 35, "R")]
        table_header(pdf, cols)

        # Materials
        table_row(pdf, [("MATERIALS", 150, "L")], bold=True, fill=True)
        mat_total = 0.0
        for m in d["materials"]:
            cost = float(m["cost"])
            mat_total += cost
            table_row(pdf, [
                (m["desc"], 75, "L"),
                (m["qty"], 40, "L"),
                (f"R {cost:,.2f}", 35, "R"),
            ])
        table_row(pdf, [
            ("MATERIALS TOTAL", 45, "L"),
            ("Supplied by\nBuildRight Solutions", 70, "L"),
            (f"R {mat_total:,.2f}", 35, "R"),
        ], bold=True, fill=True)
        pdf.ln(1)

        # Material notes
        for note_text in d.get("material_notes", []):
            sf(pdf, C.STYLE_ITALIC, 6)
            pdf.multi_cell(0, 3.5, f"Note: {note_text}")
            pdf.ln(1)
        pdf.ln(1)

        # Labour
        table_row(pdf, [("LABOUR", 150, "L")], bold=True, fill=True)
        lab_total = 0.0
        for item in d["labour"]:
            cost = float(item["cost"])
            lab_total += cost
            table_row(pdf, [
                (item["desc"], 75, "L"),
                (item["qty"], 40, "L"),
                (f"R {cost:,.2f}", 35, "R"),
            ])

        # Discount
        discount = float(d.get("discount_amount", 0))
        if discount > 0:
            table_row(pdf, [
                (d.get("discount_label", "Discount"), 75, "L"),
                ("", 40, "L"),
                (f"- R {discount:,.2f}", 35, "R"),
            ])

        lab_total -= discount
        table_row(pdf, [
            ("LABOUR TOTAL", 45, "L"),
            ("", 70, "L"),
            (f"R {lab_total:,.2f}", 35, "R"),
        ], bold=True, fill=True)
        pdf.ln(1)

        # Grand Total
        grand = mat_total + lab_total
        total_row(pdf, "GRAND TOTAL",
                  f"R {grand:,.2f}",
                  cols)
        sf(pdf, C.STYLE_ITALIC, 6)
        note = "Incl. all materials & labour"
        if discount > 0:
            note += " · discount applied"
        pdf.cell(0, 3, note, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

        # Material notes
        for note_text in d.get("material_notes", []):
            sf(pdf, C.STYLE_ITALIC, 6.5)
            pdf.multi_cell(0, 3.5, f"Note: {note_text}")
            pdf.ln(1)

        # ── Footer info ──────────────────────────────────────────────────
        sf(pdf, "", 6)
        pdf.set_text_color(120, 120, 120)
        pdf.cell(0, 4, f"Materials total: R{mat_total:,.2f}  ·  Labour total: R{lab_total:,.2f}  ·  Grand Total: R{grand:,.2f}.",
                 new_x="LMARGIN", new_y="NEXT")
        sf(pdf, C.STYLE_BOLD, 6)
        pdf.cell(0, 4, f"{C.COMPANY_NAME}  ·  {C.ADDRESS_LINE1}  ·  {C.REG_NUMBER}",
                 new_x="LMARGIN", new_y="NEXT")
        sf(pdf, C.STYLE_ITALIC, 6)
        pdf.cell(0, 4, f'"{C.TAGLINE}"', new_x="LMARGIN", new_y="NEXT")

        # ── Page 2 — Terms & Conditions ──────────────────────────────────
        pdf._show_header = False
        pdf._show_footer = True
        pdf.add_page()
        _add_terms_and_conditions(pdf)

        self.pdf = pdf

    # ── Style B — Clean "BUILD RIGHT" header ─────────────────────────────

    def _build_style_b(self):
        d = self.data
        pdf = BRSBase()
        pdf.set_auto_page_break(auto=True, margin=22)
        pdf.add_page()

        # ── Header block ─────────────────────────────────────────────────
        sf(pdf, C.STYLE_BOLD, 16)
        pdf.set_text_color(*C.BRAND_DARK)
        pdf.cell(0, 8, "BUILD  RIGHT", new_x="LMARGIN", new_y="NEXT")

        sf(pdf, "", 9)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(0, 5, f"{C.COMPANY_NAME}", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 4, f"Registration No: {C.REG_NUMBER}  ·  {C.ADDRESS_LINE1}",
                 new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 4, C.EMAIL, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1)

        sf(pdf, C.STYLE_ITALIC, 8)
        pdf.cell(0, 4, f'"{C.TAGLINE}"', new_x="LMARGIN", new_y="NEXT")
        sf(pdf, "", 8)
        pdf.cell(0, 4, f'Date: {C.date_issued(d["date_issued"])}', new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 4, f'Projected Start: {d["projected_start"]}', new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 4, f'Quotation valid for: {d["validity_days"]} days', new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 4, f'Ref: {d["ref"]}', new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

        # ── Title ────────────────────────────────────────────────────────
        sf(pdf, C.STYLE_BOLD, 13)
        pdf.set_text_color(*C.BRAND_ACCENT)
        pdf.cell(0, 8, "OFFICIAL QUOTATION", new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(*C.BRAND_DARK)
        pdf.ln(1)

        # ── Client Info ──────────────────────────────────────────────────
        section_title(pdf, "CLIENT INFORMATION")
        key_value(pdf, "Client Name:", d["client_name"])
        key_value(pdf, "Project Date:", C.date_issued(d["date_issued"]))
        key_value(pdf, "Address:", d["client_address"])
        key_value(pdf, "Projected Start:", d["projected_start"])
        pdf.ln(2)

        # ── Project Description ──────────────────────────────────────────
        section_title(pdf, "PROJECT DESCRIPTION")
        sf(pdf, "", 8)
        pdf.multi_cell(0, 4.5, d["project_description"])
        pdf.ln(3)

        # ── Measurements ─────────────────────────────────────────────────
        if d["measurements"]:
            section_title(pdf, "MEASUREMENTS — PER CLIENT SKETCH")
            cols_m = [("Element", 70, "L"), ("Dimension", 50, "L"), ("Area", 50, "L")]
            table_header(pdf, cols_m)
            for m in d["measurements"]:
                table_row(pdf, [
                    (m["element"], 70, "L"),
                    (m["dimension"], 50, "L"),
                    (m.get("area", "as measured"), 50, "L"),
                ])
            sf(pdf, C.STYLE_ITALIC, 6)
            pdf.multi_cell(0, 3.5,
                "Dimensions transcribed from the client's sketch. Final quantities will be confirmed by tape measure "
                "during the site survey prior to commencement, in line with the terms below.")
            pdf.ln(3)

        # ── Material Specification ───────────────────────────────────────
        if d["materials"]:
            section_title(pdf, "MATERIAL SPECIFICATION")
            cols_ms = [("Material", 65, "L"), ("Quantity", 35, "L"), ("Purpose / Notes", 65, "L")]
            table_header(pdf, cols_ms)
            for m in d["materials"]:
                table_row(pdf, [
                    (m["desc"], 65, "L"),
                    (m["qty"], 35, "L"),
                    (m.get("notes", ""), 65, "L"),
                ])
            pdf.ln(2)
            for note_text in d.get("material_notes", []):
                sf(pdf, C.STYLE_ITALIC, 6.5)
                pdf.multi_cell(0, 3.5, f"Note: {note_text}")
                pdf.ln(1)
            pdf.ln(2)

        # ── Quotation Breakdown ──────────────────────────────────────────
        section_title(pdf, "QUOTATION BREAKDOWN")
        cols = [("Item / Description", 70, "L"), ("Qty / Spec", 40, "L"), ("Cost (ZAR)", 30, "R"), ("Notes", 30, "L")]
        table_header(pdf, cols)

        # Measurements
        if d["measurements"]:
            table_row(pdf, [("MEASUREMENTS", 170, "L")], bold=True, fill=True)
            for m in d["measurements"]:
                table_row(pdf, [
                    (m["element"], 70, "L"),
                    (m["dimension"], 40, "L"),
                    (m.get("area", "as measured"), 30, "R"),
                    ("", 30, "L"),
                ])
            pdf.ln(1)

        # Materials
        table_row(pdf, [("MATERIALS", 170, "L")], bold=True, fill=True)
        mat_total = 0.0
        for m in d["materials"]:
            cost = float(m["cost"])
            mat_total += cost
            table_row(pdf, [
                (m["desc"], 70, "L"),
                (m["qty"], 40, "L"),
                (f"R {cost:,.2f}", 30, "R"),
                (m.get("notes", "")[:25], 30, "L"),
            ])
        table_row(pdf, [
            ("Materials subtotal", 70, "L"),
            ("", 40, "L"),
            (f"R {mat_total:,.2f}", 30, "R"),
            ("", 30, "L"),
        ], bold=True, fill=True)
        pdf.ln(1)

        # Labour
        table_row(pdf, [("LABOUR (payable to BuildRight Solutions)", 170, "L")], bold=True, fill=True)
        lab_total = 0.0
        for item in d["labour"]:
            cost = float(item["cost"])
            lab_total += cost
            table_row(pdf, [
                (item["desc"], 70, "L"),
                (item["qty"], 40, "L"),
                (f"R {cost:,.2f}", 30, "R"),
                (item.get("notes", "")[:25], 30, "L"),
            ])

        # Discount
        discount = float(d.get("discount_amount", 0))
        if discount > 0:
            table_row(pdf, [
                (d.get("discount_label", "Discount"), 70, "L"),
                ("", 40, "L"),
                (f"- R {discount:,.2f}", 30, "R"),
                ("", 30, "L"),
            ])

        lab_total -= discount
        table_row(pdf, [
            ("Labour subtotal (payable to BuildRight)", 70, "L"),
            ("", 40, "L"),
            (f"R {lab_total:,.2f}", 30, "R"),
            ("", 30, "L"),
        ], bold=True, fill=True)
        pdf.ln(1)

        # Grand Total
        grand = mat_total + lab_total
        total_row(pdf, "GRAND TOTAL",
                  f"R {grand:,.2f}",
                  cols)
        sf(pdf, C.STYLE_ITALIC, 6)
        note = "Incl. all materials & labour"
        if discount > 0:
            note += " · discount applied"
        pdf.cell(0, 3, note, new_x="LMARGIN", new_y="NEXT")

        # ── Page 2 — Terms & Conditions ──────────────────────────────────
        pdf.add_page()
        _add_terms_and_conditions(pdf)

        self.pdf = pdf


# ── Terms & Conditions (shared) ─────────────────────────────────────────────

def _add_terms_and_conditions(pdf: FPDF):
    section_title(pdf, "TERMS & CONDITIONS")
    terms = [
        "1.  This quotation is valid for the period stated above. After expiry, prices may be revised.",
        "2.  A 50% deposit is required for material procurement before any work commences. The balance is payable upon practical completion.",
        "3.  All materials listed are supplied by BuildRight Solutions unless otherwise stated.",
        "4.  Final quantities and areas may be adjusted after the on-site survey. Any variation will be communicated and agreed upon in writing before commencement.",
        "5.  The projected start date is subject to confirmation following the site survey and receipt of deposit.",
        "6.  Any changes to scope after commencement may result in a variation order with adjusted pricing.",
        "7.  A minimum 48-hour notice is required for cancellation. Material costs already incurred will be billed.",
        "8.  BuildRight Solutions carries general liability insurance. Proof available on request.",
        "9.  All prices are inclusive of VAT where applicable.",
        "10. Payment to be made via EFT to the banking details provided. Proof of payment to be sent to the email above.",
    ]
    sf(pdf, "", 7.5)
    for t in terms:
        pdf.multi_cell(0, 4, t)
        pdf.ln(1)
    pdf.ln(3)

    # Banking details
    bank_details_block(pdf)
