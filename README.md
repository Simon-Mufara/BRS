# BuildRight Solutions — Document Automation Agent

> "We Nail It, You Enjoy It!"

Automatically generate professional PDFs for **BuildRight Solutions (Pty) Ltd**:
- **Quotations** (two document styles)
- **Payment Requests** (deposit / final balance)
- **Invoices**
- **Delivery Notes**
- **Scope of Works**

---

## Quick Start

### Generate all example documents
```bash
python -m brs_agent.cli --quick
```

This produces all pre-filled example PDFs in `brs_agent/output/`.

### Interactive menu
```bash
python -m brs_agent.cli
```

### From Python code
```python
from brs_agent.quotation import QuotationGenerator
from brs_agent.examples import VINODHA_QUOTATION

gen = QuotationGenerator()
gen.build(VINODHA_QUOTATION)
gen.save("my_quotation.pdf")
```

---

## Document Types

### 1. Quotation (Style A — Tabular)
Traditional "OFFICIAL QUOTATION" layout with measurements, breakdown, totals.
Used for: Crack repair, painting, skirting, cornice works.

```python
from brs_agent.quotation import QuotationGenerator

data = {
    "style": "A",
    "project_title": "Crack Repair, Painting, Skirting & Cornice Works",
    "client_name": "John Smith",
    "client_address": "123 Main St, Sundowner, Randburg",
    "project_description": "Exterior crack repair and painting...",
    "materials": [
        {"desc": "Paint — white, matt", "qty": "5 L", "cost": 395.00},
        {"desc": "Cemex F", "qty": "5 L", "cost": 365.00},
    ],
    "labour": [
        {"desc": "Exterior wall painting", "qty": "3 wall sections", "cost": 900.00},
    ],
}

gen = QuotationGenerator()
gen.build(data)
gen.save("output/quotation.pdf")
```

### 2. Quotation (Style B — Clean)
Modern BUILD RIGHT header with separate Material Specification section.
Used for: Tiling, waterproofing, multi-scope, painting jobs.

```python
from brs_agent.quotation import QuotationGenerator

data = {
    "style": "B",
    "client_name": "Vinodha Naidoo",
    "client_address": "23 Lords Avenue, Windsor West, Randburg",
    "project_description": "Strip-out of existing tiling, waterproofing and re-tiling...",
    "materials": [
        {"desc": "Cemex waterproofing compound", "qty": "10 L", "cost": 695.00, "notes": "Waterproofing"},
    ],
    "labour": [
        {"desc": "Tile installation", "qty": "All areas", "cost": 1450.00},
    ],
}

gen = QuotationGenerator()
gen.build(data)
gen.save("output/tiling_quotation.pdf")
```

### 3. Payment Request

```python
from brs_agent.payment_request import PaymentRequestGenerator

data = {
    "client_name": "Trishan",
    "client_address": "385 Cork Avenue, Ferndale, Randburg",
    "quotation_ref": "BRS-2026-0816-T1",
    "total_project_value": 23585.00,
    "payment_type": "deposit",
    "payment_pct": 57.6,
    "deposit_description": "Deposit — Material Procurement & Delivery",
    "works_start": "Wednesday, 19 August 2026",
    "payment_ref": "BRS-T1",
}

gen = PaymentRequestGenerator()
gen.build(data)
gen.save("output/payment_request.pdf")
```

### 4. Invoice

```python
from brs_agent.invoice import InvoiceGenerator

data = {
    "client_name": "Michelle",
    "client_address": "Cottonwoods, 19 Argyle Avenue, Craighall",
    "quotation_ref": "BRS-2026-0809-P",
    "project_title": "Wall Painting — Cottonwoods",
    "line_items": [
        {"desc": "Wall preparation & painting", "qty": "234 m²", "rate": 30.0},
        {"desc": "Premium paint (80L)", "qty": "80 L", "rate": 125.0},
    ],
    "vat_rate": 0.0,
    "notes": "Payment due within 30 days of invoice date.",
}

gen = InvoiceGenerator()
gen.build(data)
gen.save("output/invoice.pdf")
```

### 5. Delivery Note

```python
from brs_agent.delivery_note import DeliveryNoteGenerator

data = {
    "client_name": "Trishan",
    "client_address": "385 Cork Avenue, Ferndale, Randburg",
    "quotation_ref": "BRS-2026-0816-T1",
    "items": [
        {"desc": "50 mm PVC pipe", "qty": "1", "unit": "length"},
        {"desc": "Cement", "qty": "10", "unit": "bags"},
        {"desc": "Mampara bricks", "qty": "1", "unit": "pallet"},
    ],
}

gen = DeliveryNoteGenerator()
gen.build(data)
gen.save("output/delivery_note.pdf")
```

### 6. Scope of Works

```python
from brs_agent.scope_of_works import ScopeOfWorksGenerator

data = {
    "client_name": "Trishan",
    "client_address": "385 Cork Avenue, Ferndale, Randburg",
    "quotation_ref": "BRS-2026-0816-T1",
    "project_title": "Multi-Scope Works",
    "project_description": "Downpipe plumbing, wall preparation & painting, tiling, and built-in braai.",
    "sections": [
        {
            "name": "Downpipe / Plumbing",
            "description": "9 m² area",
            "tasks": [
                {"desc": "Install elbows", "detail": "Connect to existing downpipe"},
                {"desc": "Run PVC pipe", "detail": "9m connection run"},
            ],
        },
        {
            "name": "Wall Preparation & Painting",
            "description": "15 m² area",
            "tasks": [
                {"desc": "Preparation", "detail": "Cleaning, sanding & patching"},
                {"desc": "Painting", "detail": "2 coats, inside & outside"},
            ],
        },
    ],
    "exclusions": ["Tiles (to be supplied by client)", "Plumbing connections to municipal supply"],
    "assumptions": ["Access to site available during working hours", "All existing furniture to be moved by client"],
}

gen = ScopeOfWorksGenerator()
gen.build(data)
gen.save("output/scope_of_works.pdf")
```

---

## Using JSON Files

Save your data as a JSON file and generate from the CLI:

```json
{
  "type": "quotation",
  "style": "B",
  "project_letter": "D",
  "client_name": "New Client",
  "client_address": "123 Street, Suburb",
  "project_description": "Tiling and waterproofing works...",
  "materials": [
    {"desc": "Cemex waterproofing", "qty": "10 L", "cost": 695.00}
  ],
  "labour": [
    {"desc": "Tile installation", "qty": "All areas", "cost": 1450.00}
  ]
}
```

Then select option **7** from the CLI menu.

---

## Pre-filled Examples

All examples from your real documents are in `brs_agent/examples.py`:

| Example | Style | Ref | Matches |
|---------|-------|-----|---------|
| `SUNDAOWNER_QUOTATION` | A | BRS-2026-0729-E | `BuildRight_Quotation_Sundowner_2_latest.pdf` |
| `SUNDAOWNER_DISCOUNTED` | A | BRS-2026-0729-F | `BuildRight_Quotation_Sundowner_Discounted.pdf` |
| `VINODHA_QUOTATION` | B | BRS-2026-0728-D | `BuildRight_Quotation_Vinodha_Tiling (18).pdf` |
| `FERNDALE_MULTISCOPE` | B | BRS-2026-0816-T1 | `Ferndale_MultiScope_Quotation_Trishan.pdf` |
| `COTTONWOODS_QUOTATION` | B | BRS-2026-0809-P | `Cottonwoods_Quotation_Michelle.pdf` |
| `TRISHAN_DEPOSIT` | — | BRS-T1 | `PaymentRequest_Trishan_Deposit_BRS-T1.pdf` |

---

## Configuration

Edit `brs_agent/config.py` to update:
- Company name, registration number, address
- Banking details (FNB and Capitec)
- PDF colour scheme (brand colours)
- Quotation validity period
- Reference number format
- Director name and title

---

## Output

All generated PDFs are saved to `brs_agent/output/`.

## Requirements

- Python 3.10+
- `fpdf2` (pip install fpdf2)
- `python-docx` (pip install python-docx) — for DOCX support (future)
