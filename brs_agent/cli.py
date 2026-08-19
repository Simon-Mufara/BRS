#!/usr/bin/env python3
"""
BuildRight Solutions - Document Automation Agent (CLI)
=====================================================
Interactive menu to generate professional PDFs:
  1. Quotation (from template or custom data)
  2. Payment Request (deposit / final balance)
  3. Invoice
  4. Delivery Note
  5. Scope of Works

Run:
    python -m brs_agent.cli          # interactive menu
    python -m brs_agent.cli --quick  # generate all example docs in one shot
"""

from __future__ import annotations

import json
import os
import sys
from datetime import date

# Resolve paths relative to this file
_HERE = os.path.dirname(os.path.abspath(__file__))
_OUTPUT = os.path.join(_HERE, "output")
os.makedirs(_OUTPUT, exist_ok=True)

from . import config as C
from .quotation import QuotationGenerator
from .payment_request import PaymentRequestGenerator
from .invoice import InvoiceGenerator
from .delivery_note import DeliveryNoteGenerator
from .scope_of_works import ScopeOfWorksGenerator
from .mailer import send_document_email


# ==== Helpers ============================================================

def _out_path(name: str) -> str:
    return os.path.join(_OUTPUT, name)


def _print_banner():
    os.system("cls" if os.name == "nt" else "clear")
    print()
    print("  +============================================================+")
    print("  |   BUILD RIGHT SOLUTIONS  -  Document Automation Agent      |")
    print("  |   \"We Nail It, You Enjoy It!\"                              |")
    print("  |   Reg. 2026/110944/07                                      |")
    print("  +============================================================+")
    print()


def _input(prompt: str, default: str = "") -> str:
    try:
        val = input(f"  {prompt}" + (f" [{default}]" if default else "") + ": ").strip()
        return val if val else default
    except EOFError:
        # Handle non-interactive mode (e.g., when called from script)
        return default if default else ""


def _input_float(prompt: str, default: float = 0.0) -> float:
    val = _input(prompt, str(default))
    try:
        return float(val.replace(",", "").replace("R", "").strip())
    except ValueError:
        return default


def _confirm(prompt: str) -> bool:
    try:
        return _input(prompt, "y").lower().startswith("y")
    except:
        # In case of any error, default to False (don't proceed)
        return False


def _ask_email_details(document_path: str, document_type: str, client_name: str) -> None:
    """Ask user if they want to email the document and send it if they choose to."""
    if not _confirm("\n  Email this document?"):
        return

    print("\n  -- EMAIL SETTINGS -------------------------------")
    to_email = _input("  Recipient email address")
    if not to_email:
        print("  [ERROR] No recipient email provided")
        return

    # Optional: customize message
    additional_message = _input("  Additional message (optional)", "")

    # Try to send email
    print("\n  Sending email...")
    try:
        success = send_document_email(
            to_email=to_email,
            document_path=document_path,
            document_type=document_type,
            client_name=client_name,
            additional_message=additional_message
        )
        if success:
            print(f"  [SUCCESS] Email sent successfully to {to_email}")
        else:
            print(f"  [ERROR] Failed to send email to {to_email}")
    except Exception as e:
        print(f"  [ERROR] Error sending email: {e}")


# ==== Quotation Flow ===========================================================

def _fill_quotation_interactive() -> dict:
    """Walk the user through filling in a quotation."""
    print("\n  --- NEW QUOTATION ---\n")

    data = {"style": _input("Document style (A = tabular, B = clean) [B]", "B")}

    print("\n  Client Details:")
    data["client_name"] = _input("Client name")
    data["client_address"] = _input("Client / property address")
    data["project_title"] = _input("Project title", "Tiling & Waterproofing")
    data["project_letter"] = _input("Project letter for ref (e.g. E, D, T1) [D]", "D")

    print("\n  Project Description (multi-line, end with empty line):")
    lines = []
    try:
        while True:
            line = input("  > ")
            if line == "":
                break
            lines.append(line)
    except EOFError:
        # Handle non-interactive mode or piped input
        pass
    if not lines:
        # Provide a default description to pass validation
        lines = ["Project description provided via CLI."]
    data["project_description"] = "\n".join(lines)

    if _confirm("\n  Add measurements?"):
        data["measurements"] = []
        while True:
            elem = _input("  Element name (empty to stop)")
            if not elem:
                break
            dim = _input("  Dimension")
            area = _input("  Area", "as measured")
            data["measurements"].append({"element": elem, "dimension": dim, "area": area})

    print("\n  Materials (empty desc to stop):")
    data["materials"] = []
    while True:
        desc = _input("  Material description")
        if not desc:
            break
        qty = _input("  Quantity")
        cost = _input_float("  Cost (ZAR)")
        data["materials"].append({"desc": desc, "qty": qty, "cost": cost})

    print("\n  Labour items (empty desc to stop):")
    data["labour"] = []
    while True:
        desc = _input("  Labour description")
        if not desc:
            break
        qty = _input("  Quantity / area")
        cost = _input_float("  Cost (ZAR)")
        data["labour"].append({"desc": desc, "qty": qty, "cost": cost})

    if _confirm("\n  Add a discount?"):
        data["discount_label"] = _input("  Discount label", "Client discount")
        data["discount_amount"] = _input_float("  Discount amount (ZAR)")

    return data


def _generate_quotation(data: dict | None = None, filename: str | None = None):
    """Generate a quotation PDF."""
    if data is None:
        data = _fill_quotation_interactive()

    gen = QuotationGenerator()
    gen.build(data)

    ref = data.get("ref") or C.generate_ref(data.get("project_letter", "D"))
    fname = filename or f"Quotation_{ref}.pdf"
    path = _out_path(fname)
    gen.save(path)
    print(f"\n  [SUCCESS] Quotation saved: {path}")

    # Ask to email the document
    _ask_email_details(path, "quotation", data.get("client_name", ""))

    return path


# ==== Payment Request Flow ===================================================

def _fill_payment_interactive() -> dict:
    print("\n  --- NEW PAYMENT REQUEST ---\n")
    data = {
        "client_name": _input("Client name"),
        "client_address": _input("Client / site address"),
        "quotation_ref": _input("Quotation reference"),
        "total_project_value": _input_float("Total project value (ZAR)"),
    }

    print("\n  Payment type:")
    print("    1. Deposit (50%)")
    print("    2. Final Balance")
    print("    3. Custom percentage")
    choice = _input("  Choice [1]", "1")

    if choice == "2":
        data["payment_type"] = "final_balance"
        data["payment_pct"] = 100
        data["deposit_description"] = "Final Balance - Works Completed"
    elif choice == "3":
        data["payment_type"] = _input("  Payment type name", "progress")
        data["payment_pct"] = _input_float("  Percentage (%)", 50)
        data["deposit_description"] = _input("  Description", "Progress Payment")
    else:
        data["payment_type"] = "deposit"
        data["payment_pct"] = 50
        data["deposit_description"] = "Deposit - Material Procurement & Delivery"

    data["works_start"] = _input("Works start date", "TBC")
    data["bank"] = _input("Bank (fnb / capitec)", C.DEFAULT_BANK)
    data["payment_ref"] = _input("Payment reference", "")
    return data


def _generate_payment_request(data: dict | None = None, filename: str | None = None):
    if data is None:
        data = _fill_payment_interactive()

    gen = PaymentRequestGenerator()
    gen.build(data)

    ref = data.get("quotation_ref", "UNK")
    fname = filename or f"PaymentRequest_{ref}.pdf"
    path = _out_path(fname)
    gen.save(path)
    print(f"\n  [SUCCESS] Payment request saved: {path}")

    # Ask to email the document
    _ask_email_details(path, "payment request", data.get("client_name", ""))

    return path


# ==== Invoice Flow ===========================================================

def _fill_invoice_interactive() -> dict:
    print("\n  --- NEW INVOICE ---\n")
    data = {
        "client_name": _input("Client name"),
        "client_address": _input("Client address"),
        "quotation_ref": _input("Quotation reference", ""),
        "project_title": _input("Project / invoice description", "Works Completed"),
        "vat_rate": _input_float("VAT rate (0.0 or 0.15)", 0.0),
    }

    print("\n  Line items (empty desc to stop):")
    data["line_items"] = []
    while True:
        desc = _input("  Description")
        if not desc:
            break
        qty = _input("  Qty", "1")
        rate = _input_float("  Rate (ZAR)")
        data["line_items"].append({"desc": desc, "qty": qty, "rate": rate})

    if _confirm("\n  Add a discount?"):
        data["discount_label"] = _input("  Discount label", "Discount")
        data["discount_amount"] = _input_float("  Discount amount (ZAR)")

    data["notes"] = _input("Additional notes", "")
    return data


def _generate_invoice(data: dict | None = None, filename: str | None = None):
    if data is None:
        data = _fill_invoice_interactive()

    gen = InvoiceGenerator()
    gen.build(data)

    inv_no = data.get("invoice_number", "INV")
    fname = filename or f"Invoice_{inv_no}.pdf"
    path = _out_path(fname)
    gen.save(path)
    print(f"\n  [SUCCESS] Invoice saved: {path}")

    # Ask to email the document
    _ask_email_details(path, "invoice", data.get("client_name", ""))

    return path


# ==== Delivery Note Flow =====================================================

def _fill_delivery_interactive() -> dict:
    print("\n  --- NEW DELIVERY NOTE ---\n")
    data = {
        "client_name": _input("Client name"),
        "client_address": _input("Client address"),
        "site_address": _input("Delivery site address (if different)", ""),
        "quotation_ref": _input("Quotation reference", ""),
    }

    print("\n  Items to deliver (empty desc to stop):")
    data["items"] = []
    while True:
        desc = _input("  Item description")
        if not desc:
            break
        qty = _input("  Qty")
        unit = _input("  Unit (bags, L, rolls, etc.)", "")
        notes = _input("  Notes", "")
        data["items"].append({"desc": desc, "qty": qty, "unit": unit, "notes": notes})

    data["vehicle_ref"] = _input("Vehicle / registration", "")
    data["notes"] = _input("Additional notes", "")
    return data


def _generate_delivery_note(data: dict | None = None, filename: str | None = None):
    if data is None:
        data = _fill_delivery_interactive()

    gen = DeliveryNoteGenerator()
    gen.build(data)

    fname = filename or f"DeliveryNote_{date.today().strftime('%Y%m%d')}.pdf"
    path = _out_path(fname)
    gen.save(path)
    print(f"\n  [SUCCESS] Delivery note saved: {path}")

    # Ask to email the document
    _ask_email_details(path, "delivery note", data.get("client_name", ""))

    return path


# ==== Scope of Works Flow ====================================================

def _fill_scope_interactive() -> dict:
    print("\n  --- NEW SCOPE OF WORKS ---\n")
    data = {
        "client_name": _input("Client name"),
        "client_address": _input("Client address"),
        "quotation_ref": _input("Quotation reference"),
        "project_title": _input("Project title", "Scope of Works"),
        "projected_start": _input("Projected start date", "TBC"),
        "estimated_duration": _input("Estimated duration", "TBC"),
    }

    print("\n  Project description (multi-line, end with empty line):")
    lines = []
    while True:
        line = input("  > ")
        if line == "":
            break
        lines.append(line)
    data["project_description"] = "\n".join(lines)

    data["sections"] = []
    while _confirm("\n  Add a scope section?"):
        sec = {"name": _input("  Section name")}
        print("  Section description (multi-line, end with empty line):")
        sec_lines = []
        while True:
            line = input("  > ")
            if line == "":
                break
            sec_lines.append(line)
        sec["description"] = "\n".join(sec_lines)

        sec["tasks"] = []
        while _confirm("  Add a task?"):
            sec["tasks"].append({
                "desc": _input("    Task name"),
                "detail": _input("    Task detail"),
            })

        data["sections"].append(sec)

    print("\n  Exclusions (empty to stop):")
    data["exclusions"] = []
    while True:
        exc = _input("  Exclusion")
        if not exc:
            break
        data["exclusions"].append(exc)

    print("\n  Assumptions (empty to stop):")
    data["assumptions"] = []
    while True:
        asm = _input("  Assumption")
        if not asm:
            break
        data["assumptions"].append(asm)

    return data


def _generate_scope(data: dict | None = None, filename: str | None = None):
    if data is None:
        data = _fill_scope_interactive()

    gen = ScopeOfWorksGenerator()
    gen.build(data)

    ref = data.get("quotation_ref", "SOW")
    fname = filename or f"ScopeOfWorks_{ref}.pdf"
    path = _out_path(fname)
    gen.save(path)
    print(f"\n  [SUCCESS] Scope of works saved: {path}")

    # Ask to email the document
    _ask_email_details(path, "scope of works", data.get("client_name", ""))

    return path


# -- Quick Generate All Examples ----------------------------------------------

def _quick_generate_all():
    """Generate all example documents in one shot."""
    from .examples import (
        SUNDAOWNER_QUOTATION,
        VINODHA_QUOTATION,
        SUNDAOWNER_DISCOUNTED,
        TRISHAN_DEPOSIT,
        FERNDALE_MULTISCOPE,
        COTTONWOODS_QUOTATION,
    )

    print("\n  Generating all example documents...\n")

    _generate_quotation(SUNDAOWNER_QUOTATION, "Quotation_Sundowner_E.pdf")
    _generate_quotation(VINODHA_QUOTATION, "Quotation_Vinodha_D.pdf")
    _generate_quotation(SUNDAOWNER_DISCOUNTED, "Quotation_Sundowner_Discounted_F.pdf")
    _generate_quotation(FERNDALE_MULTISCOPE, "Quotation_Ferndale_MultiScope_T1.pdf")
    _generate_quotation(COTTONWOODS_QUOTATION, "Quotation_Cottonwoods_P.pdf")
    _generate_payment_request(TRISHAN_DEPOSIT, "PaymentRequest_Trishan_BRS-T1.pdf")

    print(f"\n  [FOLDER] All documents saved to: {_OUTPUT}")
    print()


# -- Main Menu ----------------------------------------------------------------

def _menu():
    _print_banner()
    print("  Select document to generate:")
    print("  -------------------------------")
    print("    1. Quotation")
    print("    2. Payment Request")
    print("    3. Invoice")
    print("    4. Delivery Note")
    print("    5. Scope of Works")
    print("    6. Generate all example documents")
    print("    7. Load data from JSON file")
    print("    0. Exit")
    print()

    choice = _input("  Choice", "1")
    print()

    if choice == "1":
        _generate_quotation()
    elif choice == "2":
        _generate_payment_request()
    elif choice == "3":
        _generate_invoice()
    elif choice == "4":
        _generate_delivery_note()
    elif choice == "5":
        _generate_scope()
    elif choice == "6":
        _quick_generate_all()
    elif choice == "7":
        _load_from_json()
    else:
        print("  Goodbye!")
        return False

    print()
    input("  Press Enter to continue...")
    return True


def _load_from_json():
    """Load document data from a JSON file and generate it."""
    filepath = _input("  Path to JSON file")
    if not os.path.exists(filepath):
        print(f"  [ERROR] File not found: {filepath}")
        return

    with open(filepath) as f:
        data = json.load(f)

    doc_type = data.get("type", "quotation").lower()
    if doc_type == "quotation":
        _generate_quotation(data)
    elif doc_type == "payment_request":
        _generate_payment_request(data)
    elif doc_type == "invoice":
        _generate_invoice(data)
    elif doc_type == "delivery_note":
        _generate_delivery_note(data)
    elif doc_type == "scope_of_works":
        _generate_scope(data)
    else:
        print(f"  [ERROR] Unknown document type: {doc_type}")


# -- Entry Points -------------------------------------------------------------

def main():
    if "--help" in sys.argv or "-h" in sys.argv:
        print(__doc__)
        return
    if "--quick" in sys.argv:
        _quick_generate_all()
        return

    running = True
    while running:
        running = _menu()


if __name__ == "__main__":
    main()
