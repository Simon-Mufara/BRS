# AGENT MISSION BRIEF — BuildRight Solutions Document Automation

> **You are operating as a Senior Software Engineer.**
> **Full authority granted. Fix bugs, add features, refactor, improve — ship production-quality code.**
> **The business owner is sleeping. When they wake up, this system must be solid, polished, and ready to use.**

---

## 1. PROJECT OVERVIEW

**Company:** BuildRight Solutions (Pty) Ltd — a construction/tiling/painting company in Gauteng, South Africa.
**Purpose:** Automate the generation of business documents (quotations, payment requests, invoices, delivery notes, scope of works) as professional PDFs.
**Stack:** Python 3.13, fpdf2 (PDF generation), tkinter (GUI), no external database (JSON files for client storage).
**Codebase:** 3,360 lines of Python across 13 files in `brs_agent/`.

### File Inventory
```
brs_agent/
  config.py              78 lines   — Company details, banking, brand colours, ref number generation
  quotation.py          433 lines   — 2 quotation styles (A=tabular, B=clean header)
  payment_request.py    137 lines   — Deposit / final balance payment requests
  invoice.py            178 lines   — Auto-numbered invoices with VAT support
  delivery_note.py      139 lines   — Material delivery tracking
  scope_of_works.py     160 lines   — Multi-section scope documents
  mailer.py             141 lines   — Email sending with PDF attachments (SMTP)
  examples.py           293 lines   — 6 pre-filled examples matching real documents
  gui.py               1069 lines   — tkinter dark-themed desktop GUI
  cli.py                528 lines   — Interactive CLI menu
  utils/__init__.py     187 lines   — PDF drawing primitives, BRSBase class, safe_text
  data/                            — JSON templates, counters, client database
  output/                          — Generated PDFs
```

---

## 2. KNOWN BUGS TO FIX (CRITICAL — DO THESE FIRST)

### BUG 1: `email.py` was renamed to `mailer.py` but references may be stale
- **Status:** FIXED by renaming, but check all imports. The file was `email.py` which shadowed Python's built-in `email` module, breaking ALL imports (fpdf2, smtplib, etc.).
- **Verify:** Run `python -c "from brs_agent.mailer import send_email"` — must succeed.
- **Check:** No file should be named `email.py` inside `brs_agent/`.

### BUG 2: Payment request deposit percentage calculation
- In `TRISHAN_DEPOSIT` example data, `payment_pct` is set to `57.6` to get R13,585 from R23,585. But the percentage display shows "57.6% deposit" which looks odd. The real documents show specific rand amounts, not percentages. Consider making payment amounts configurable by Rand value, not just percentage.
- **File:** `brs_agent/examples.py` line ~185, `brs_agent/payment_request.py`

### BUG 3: Invoice counter state not reset between runs
- `invoice_counter.json` and `dn_counter.json` persist across runs. If someone deletes the output files but not the counter, numbers jump. This is by design but could confuse users. Consider adding a "reset counter" option.

### BUG 4: Unicode `·` (middle dot) in headers
- The BRSBase header uses `·` (U+00B7) which IS in latin-1 so it works, but this is fragile. The `safe_text` function in utils should handle any edge cases. Verify all documents render without Unicode errors.

### BUG 5: GUI scrollbar mousewheel binding is global
- In `_show_quotation` and `_show_scope`, `canvas.bind_all("<MouseWheel>", ...)` binds globally, meaning mousewheel scrolls ALL canvases. Should use `canvas.bind()` on the specific canvas instead.

---

## 3. IMPROVEMENTS TO MAKE (Priority Order)

### P0 — Must Have (before owner wakes up)
1. **Fix all known bugs above**
2. **Add `__all__` exports to `__init__.py`** so `from brs_agent import QuotationGenerator` works cleanly
3. **Add a `requirements.txt`** file (fpdf2, PyPDF2 for reading, python-docx for future)
4. **Add proper error handling** in all generators — validate required fields before building PDF
5. **Test every generator** with the example data and verify PDFs are non-empty and have correct page counts

### P1 — Should Have (high value)
6. **Measurement table for Style B quotations** — currently Style B has measurements but no measurement table section in the breakdown. Add it.
7. **Discount in Style B** — the discount display in Style B quotation breakdown needs a negative sign prefix
8. **Material notes in Style A** — Style A doesn't render material_notes. Add support.
9. **Add a "preview" feature to the GUI** — use `os.startfile()` on Windows to open the generated PDF in the default viewer
10. **Add keyboard shortcuts** to GUI (Ctrl+G = generate, Ctrl+S = save client)
11. **GUI: Populate client presets dynamically** — when clients are added/deleted, refresh the quotation form dropdown

### P2 — Nice to Have
12. **Add company logo support** — allow specifying a logo image in config.py, render it in BRSBase header
13. **Add a "variation order" document type** — for scope changes mid-project
14. **Add a "completion certificate" document type** — for project sign-off
15. **Batch generation from CSV** — read a CSV file and generate multiple quotations at once
16. **Add a database** (SQLite) for tracking quotation status (sent, accepted, expired, invoiced)
17. **Add report generation** — monthly summary of quotations sent, revenue, etc.
18. **Add unit tests** — test each generator with known inputs and verify output

### P3 — Polish
19. **Add dark mode toggle to GUI** (light/dark theme)
20. **Add a splash screen** or loading animation
21. **Add export to DOCX** alongside PDF (using python-docx)
22. **Add multi-language support** (English + Afrikaans for SA market)
23. **Add WhatsApp integration** — generate a shareable image/link for quotations

---

## 4. ARCHITECTURE NOTES

### How the PDF generators work:
- All generators inherit from `BRSBase(FPDF)` which provides header/footer
- `sf(pdf, style, size)` is a helper that calls `pdf.set_font("Helvetica", style, size)`
- `safe_text()` in utils replaces Unicode chars (em-dash, bullets, checkmarks) with ASCII equivalents for the built-in Helvetica font
- Every generator follows: `gen = XxxGenerator(); gen.build(data_dict); gen.save(path)`
- Data dicts use `OPTIONAL_KEYS` defaults — you only need to pass the fields you want

### The `utils/__init__.py` module provides:
- `BRSBase` — FPDF subclass with header/footer and auto-sanitizing cell/multi_cell
- `sf()` — font setter shorthand
- `section_title()`, `subsection_title()` — teal bar headers
- `key_value()` — label/value pairs
- `table_header()`, `table_row()`, `total_row()` — table drawing
- `bank_details_block()` — renders FNB or Capitec details
- `signature_block()` — signature/date lines
- `safe_text()` — Unicode-to-ASCII sanitizer

### The GUI (`gui.py`):
- tkinter dark theme with custom colours
- 5 document panels + client manager
- `LineItemTable` widget — editable table with add/delete rows
- Client database stored in `brs_agent/data/clients.json`
- Each panel has its own form fields that map directly to generator data dicts

---

## 5. TESTING CHECKLIST

Run this after every significant change:
```python
cd brs_agent && python -c "
import sys; sys.path.insert(0, '..')
import os; os.makedirs('output', exist_ok=True)
from brs_agent.quotation import QuotationGenerator
from brs_agent.payment_request import PaymentRequestGenerator
from brs_agent.invoice import InvoiceGenerator
from brs_agent.delivery_note import DeliveryNoteGenerator
from brs_agent.scope_of_works import ScopeOfWorksGenerator
from brs_agent.mailer import send_email
from brs_agent.examples import *

# Test all 5 quotation examples
for name, data in [('sundowner', SUNDAOWNER_QUOTATION), ('vinodha', VINODHA_QUOTATION),
                    ('discounted', SUNDAOWNER_DISCOUNTED), ('ferndale', FERNDALE_MULTISCOPE),
                    ('cottonwoods', COTTONWOODS_QUOTATION)]:
    g = QuotationGenerator(); g.build(data); g.save(f'output/test_{name}.pdf')
    assert os.path.getsize(f'output/test_{name}.pdf') > 1000, f'{name} too small'
    print(f'[OK] {name}')

# Test payment request
g = PaymentRequestGenerator(); g.build(TRISHAN_DEPOSIT); g.save('output/test_payment.pdf')
print('[OK] payment request')

# Test invoice
g = InvoiceGenerator(); g.build({'client_name': 'Test', 'client_address': '123 St',
    'line_items': [{'desc': 'Work', 'qty': '1', 'rate': 10000}]}); g.save('output/test_invoice.pdf')
print('[OK] invoice')

# Test delivery note
g = DeliveryNoteGenerator(); g.build({'client_name': 'Test', 'client_address': '123 St',
    'items': [{'desc': 'Cement', 'qty': '5', 'unit': 'bags'}]}); g.save('output/test_delivery.pdf')
print('[OK] delivery note')

# Test scope of works
g = ScopeOfWorksGenerator(); g.build({'client_name': 'Test', 'client_address': '123 St',
    'sections': [{'name': 'Painting', 'tasks': [{'desc': 'Prep', 'detail': 'Sand walls'}]}]})
g.save('output/test_scope.pdf')
print('[OK] scope of works')

print()
print('ALL TESTS PASSED')
"
```

---

## 6. STYLE GUIDE

- **Colours:** Teal (#16a085) accent, dark backgrounds (#1e1e2e), white text (#e0e0e0)
- **Font:** Helvetica (built-in fpdf2 font), no custom fonts (Unicode not supported)
- **Naming:** `BRS-YYYY-MMDD-X` for quotation refs, `BRS-INV-NNNN` for invoices, `BRS-DN-NNNN` for delivery notes
- **Company voice:** Professional but friendly. "We Nail It, You Enjoy It!" tagline
- **Document structure:** Every PDF has page 1 (content) + page 2 (terms/banking/signature)

---

## 7. BUSINESS CONTEXT

The owner (Simon Mufara) runs a small construction company. He needs to:
1. Send quotations to clients quickly from his laptop
2. Track which quotations are pending/accepted
3. Send payment requests (50% deposit upfront, balance on completion)
4. Generate invoices for completed work
5. Track material deliveries to sites
6. Have professional-looking documents that match his brand

**The GUI is the primary interface** — he's not a developer. The CLI and Python API are secondary for power users or automation.

---

## 8. DEPLOYMENT NOTES

- This runs on **Windows** (owner's laptop)
- Python 3.13 installed via Windows Store
- Dependencies: `fpdf2` (pip install fpdf2), `PyPDF2` (pip install PyPDF2)
- No internet required for PDF generation
- Email sending requires SMTP credentials (Gmail app password)
- All output goes to `brs_agent/output/`
- Client database is `brs_agent/data/clients.json`

---

## 9. DIRECTIVES

1. **Read every file** in the project before making changes
2. **Run the testing checklist** after every significant change
3. **Don't break what works** — the PDF generators are tested and producing correct output
4. **Match existing code style** — follow the patterns already in the codebase
5. **Commit frequently** with descriptive messages
6. **If something is ambiguous, make the pragmatic choice** — this is a small business tool, not enterprise software
7. **When in doubt, test it** — generate a PDF and verify the output

---

**END OF MISSION BRIEF**

> Go build something great. The owner trusts you with full authority.
> When they wake up, they should be able to open the GUI, fill in a form, and generate a professional PDF in seconds.
