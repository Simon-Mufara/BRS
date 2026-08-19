"""
Scope of Works PDF Generator
==============================
Generates detailed scope-of-works documents for projects.
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
)


OPTIONAL_KEYS = {
    "client_name": "",
    "client_address": "",
    "quotation_ref": "",
    "project_title": "Scope of Works",
    "project_description": "",
    "date_issued": None,
    "projected_start": "TBC",
    "estimated_duration": "TBC",
    "sections": [],
    "exclusions": [],
    "assumptions": [],
    "health_safety": True,
    "prepared_by": C.DIRECTOR_NAME,
}


class ScopeOfWorksGenerator:

    def __init__(self):
        self.pdf: FPDF | None = None
        self.data: dict = {}

    def build(self, data: dict) -> FPDF:
        self.data = {**OPTIONAL_KEYS, **data}
        d = self.data

        # Validate required fields
        required_fields = ["client_name", "client_address", "quotation_ref", "project_title"]
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

        pdf = BRSBase()
        pdf.set_auto_page_break(auto=True, margin=22)
        pdf.add_page()

        # ── Title ────────────────────────────────────────────────────────
        sf(pdf, C.STYLE_BOLD, 16)
        pdf.set_text_color(*C.BRAND_ACCENT)
        pdf.cell(0, 10, "SCOPE OF WORKS", new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(*C.BRAND_DARK)

        sf(pdf, C.STYLE_BOLD, 11)
        pdf.cell(0, 6, d["project_title"], new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

        # ── Meta ─────────────────────────────────────────────────────────
        section_title(pdf, "PROJECT INFORMATION")
        key_value(pdf, "Client:", d["client_name"])
        key_value(pdf, "Address:", d["client_address"])
        key_value(pdf, "Quotation Ref:", d["quotation_ref"])
        key_value(pdf, "Date:", C.date_issued(d["date_issued"]))
        key_value(pdf, "Projected Start:", d["projected_start"])
        key_value(pdf, "Est. Duration:", d["estimated_duration"])
        key_value(pdf, "Prepared By:", d["prepared_by"])
        pdf.ln(3)

        # ── Project Description ──────────────────────────────────────────
        if d["project_description"]:
            section_title(pdf, "PROJECT DESCRIPTION")
            sf(pdf, "", 8)
            pdf.multi_cell(0, 4.5, d["project_description"])
            pdf.ln(3)

        # ── Scope Sections ───────────────────────────────────────────────
        for i, sec in enumerate(d["sections"], 1):
            subsection_title(pdf, f"SECTION {i}: {sec['name'].upper()}")
            if sec.get("description"):
                sf(pdf, "", 8)
                pdf.multi_cell(0, 4.5, sec["description"])
                pdf.ln(2)

            if sec.get("tasks"):
                cols = [("#", 8, "C"), ("Task", 50, "L"), ("Detail", 110, "L")]
                table_header(pdf, cols)
                for j, task in enumerate(sec["tasks"], 1):
                    table_row(pdf, [
                        (str(j), 8, "C"),
                        (task["desc"], 50, "L"),
                        (task.get("detail", ""), 110, "L"),
                    ])
                pdf.ln(3)

        # ── Exclusions ───────────────────────────────────────────────────
        if d["exclusions"]:
            section_title(pdf, "EXCLUSIONS")
            sf(pdf, "", 8)
            for exc in d["exclusions"]:
                pdf.cell(5, 4.5, "")
                pdf.cell(0, 4.5, f"•  {exc}", new_x="LMARGIN", new_y="NEXT")
            pdf.ln(3)

        # ── Assumptions ──────────────────────────────────────────────────
        if d["assumptions"]:
            section_title(pdf, "ASSUMPTIONS")
            sf(pdf, "", 8)
            for asm in d["assumptions"]:
                pdf.cell(5, 4.5, "")
                pdf.cell(0, 4.5, f"•  {asm}", new_x="LMARGIN", new_y="NEXT")
            pdf.ln(3)

        # ── Health & Safety ──────────────────────────────────────────────
        if d["health_safety"]:
            section_title(pdf, "HEALTH & SAFETY")
            sf(pdf, "", 8)
            hs_items = [
                "All work will be conducted in accordance with the Occupational Health and Safety Act (Act 85 of 1993).",
                "Personal protective equipment (PPE) will be worn by all personnel at all times.",
                "The work area will be kept clean and tidy throughout the project duration.",
                "Any hazardous materials will be handled and disposed of per SABS and municipal regulations.",
                "A site-specific risk assessment will be completed prior to commencement.",
            ]
            for item in hs_items:
                pdf.cell(5, 4.5, "")
                pdf.cell(0, 4.5, f"•  {item}", new_x="LMARGIN", new_y="NEXT")
            pdf.ln(3)

        # ── Acceptance ───────────────────────────────────────────────────
        section_title(pdf, "ACCEPTANCE & AUTHORISATION")
        sf(pdf, "", 8)
        pdf.multi_cell(0, 4.5,
            "By signing below, the client confirms they have read, understood, and accepted the scope of works "
            "as outlined above. Any changes to scope must be agreed upon in writing by both parties.")
        pdf.ln(8)

        sf(pdf, C.STYLE_BOLD, 8)
        pdf.cell(90, 5, f"Prepared by: {C.DIRECTOR_NAME}")
        pdf.cell(90, 5, "Accepted by: _______________________", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(3)
        sf(pdf, "", 7)
        pdf.cell(90, 5, f"{C.DIRECTOR_TITLE}, {C.COMPANY_SHORT}")
        pdf.cell(90, 5, "Signature: _______________________", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(3)
        pdf.cell(90, 5, "Date: _______________________")
        pdf.cell(90, 5, "Date: _______________________", new_x="LMARGIN", new_y="NEXT")

        self.pdf = pdf
        return pdf

    def save(self, path: str) -> str:
        if self.pdf is None:
            raise RuntimeError("Call build() before save()")
        self.pdf.output(path)
        return path
