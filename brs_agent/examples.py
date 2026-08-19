"""
Example Data — Pre-filled quotation/payment-request data matching real documents.
These serve as both documentation and ready-to-generate templates.
"""

# ══════════════════════════════════════════════════════════════════════════════
# EXAMPLE 1 — Sundowner Crack Repair & Painting (Style A)
# Matches: BuildRight_Quotation_Sundowner_2_latest.pdf
# ══════════════════════════════════════════════════════════════════════════════

SUNDAOWNER_QUOTATION = {
    "style": "A",
    "project_title": "Crack Repair, Painting, Skirting & Cornice Works",
    "project_letter": "E",
    "client_name": "[Client Name]",
    "client_address": "Sundowner, 2161, Randburg, Gauteng",
    "project_description": (
        "Exterior crack repair and painting, together with interior finishing works, "
        "at the client's residential property in Sundowner, Randburg. The scope covers "
        "four areas: (1) exterior wall crack patching and repaint, (2) skirting repair, "
        "sealing and painting including a 300 mm make-up section, (3) supply and "
        "installation of two slim cornice lengths to the kitchen, and (4) painting of "
        "the stairwell balustrade and stairwell ceiling. All materials listed below are "
        "supplied by BuildRight Solutions and are included in the quoted totals."
    ),
    "measurements": [
        {"element": "Wall section 1 — crack patch & paint", "dimension": "360 mm span", "area": "as measured"},
        {"element": "Wall section 2 — crack patch & paint", "dimension": "380 mm span", "area": "as measured"},
        {"element": "Wall section 3 — crack patch & paint", "dimension": "390 mm span", "area": "as measured"},
        {"element": "Skirting — make-up section, seal & paint", "dimension": "300 mm insert", "area": "as measured"},
        {"element": "Kitchen cornice — slim profile", "dimension": "2 lengths", "area": "as measured"},
        {"element": "Stairwell balustrade — paint", "dimension": "400 span", "area": "as measured"},
        {"element": "Stairwell ceiling — paint", "dimension": "—", "area": "4.0 m²"},
    ],
    "materials": [
        {"desc": "Paint — white colour match, matt (non-sheen)", "qty": "5 L", "cost": 395.00},
        {"desc": "Paint — brown, exterior walls", "qty": "10 L", "cost": 950.00},
        {"desc": "Paint — black, balustrade", "qty": "1 L", "cost": 165.00},
        {"desc": "Cemex F", "qty": "5 L", "cost": 365.00},
        {"desc": "Densilar — crack filling & preparation", "qty": "5 L", "cost": 320.00},
        {"desc": "Cornice — slim profile, kitchen", "qty": "2 lengths", "cost": 150.00},
        {"desc": "Cornice adhesive", "qty": "1 L", "cost": 110.00},
        {"desc": "Skirting — make-up length", "qty": "300 mm section", "cost": 120.00},
        {"desc": "Silicone sealant — wood grade, skirting", "qty": "1 tube", "cost": 95.00},
        {"desc": "Masking tape & plastic drop sheet", "qty": "1 set", "cost": 50.00},
    ],
    "labour": [
        {"desc": "Crack patching and exterior wall preparation", "qty": "3 wall sections", "cost": 750.00},
        {"desc": "Exterior wall painting", "qty": "3 wall sections", "cost": 900.00},
        {"desc": "Skirting — make-up section, silicone seal and paint", "qty": "All areas", "cost": 450.00},
        {"desc": "Cornice supply and installation", "qty": "Kitchen — 2 lengths", "cost": 400.00},
        {"desc": "Balustrade preparation and painting", "qty": "Stairwell", "cost": 400.00},
        {"desc": "Stairwell ceiling painting", "qty": "4.0 m²", "cost": 300.00},
    ],
}


# ══════════════════════════════════════════════════════════════════════════════
# EXAMPLE 2 — Vinodha Tiling (Style B)
# Matches: BuildRight_Quotation_Vinodha_Tiling (18).pdf
# ══════════════════════════════════════════════════════════════════════════════

VINODHA_QUOTATION = {
    "style": "B",
    "project_letter": "D",
    "client_name": "Vinodha Naidoo",
    "client_address": "23 Lords Avenue, Windsor West, Randburg, Johannesburg, Gauteng",
    "projected_start": "TBC (subject to site survey)",
    "project_description": (
        "Strip-out of existing tiling, waterproofing and re-tiling at the client's "
        "residential property. The works are supplied and executed as a complete "
        "turnkey item — all materials listed below are supplied by BuildRight Solutions "
        "and are included in the quoted totals."
    ),
    "measurements": [
        {"element": "Tiling — run A", "dimension": "440 mm span", "area": "as measured"},
        {"element": "Tiling — run B", "dimension": "140 mm span", "area": "as measured"},
    ],
    "materials": [
        {"desc": "Cemex waterproofing compound", "qty": "10 L", "cost": 695.00, "notes": "Waterproofing application to substrate"},
        {"desc": "Tile adhesive — wall & floor", "qty": "8 × 20 kg bags", "cost": 810.00, "notes": "Fixing tiles to prepared surface"},
        {"desc": "Bonding liquid / tile mix additive", "qty": "5 L", "cost": 280.00, "notes": "Strengthens tile adhesive mix"},
        {"desc": "Waterproofing membrane cloth — long roll", "qty": "1 roll", "cost": 220.00, "notes": "Waterproofing membrane layer"},
    ],
    "material_notes": [
        "Waterproofing membrane cloth is priced at the standard roll estimate (1 roll). "
        "As a longer roll length is required for this job, this line item and the totals "
        "will be confirmed and adjusted once the exact run length is measured on site.",
        "Floor and wall tiles themselves are excluded — to be supplied by the client, or "
        "quoted separately once tile selection is confirmed. Tile grout, spacers and trims "
        "are also not included in the materials above.",
    ],
    "labour": [
        {"desc": "Removal and disposal of existing tiling", "qty": "All areas", "cost": 950.00},
        {"desc": "Waterproofing application — membrane and compound", "qty": "All areas", "cost": 1100.00},
        {"desc": "Tile installation", "qty": "All areas", "cost": 1450.00},
    ],
}


# ══════════════════════════════════════════════════════════════════════════════
# EXAMPLE 3 — Sundowner Discounted (Style A + discount)
# Matches: BuildRight_Quotation_Sundowner_Discounted.pdf
# ══════════════════════════════════════════════════════════════════════════════

SUNDAOWNER_DISCOUNTED = {
    **SUNDAOWNER_QUOTATION,
    "project_letter": "F",
    "project_description": (
        "Exterior crack repair and painting, together with interior finishing works, "
        "at the client's residential property in Sundowner, Randburg. The scope covers "
        "three areas: (1) exterior wall crack patching and repaint, (2) skirting repair, "
        "sealing and painting including a 300 mm make-up section, and (3) supply and "
        "installation of two slim cornice lengths to the kitchen, together with preparation "
        "and painting of the stairwell balustrade. All materials listed below are supplied "
        "by BuildRight Solutions and are included in the quoted totals.\n\n"
        "Revised quotation — client discount applied. Stairwell ceiling painting and "
        "exterior brown paint supply have been removed from scope, and labour has been "
        "discounted by R800.00."
    ),
    "measurements": [
        m for m in SUNDAOWNER_QUOTATION["measurements"]
        if "Stairwell ceiling" not in m["element"]
    ],
    # Materials: remove brown paint & masking tape
    "materials": [
        m for m in SUNDAOWNER_QUOTATION["materials"]
        if "brown" not in m["desc"].lower() and "masking" not in m["desc"].lower()
    ],
    "labour": [
        item for item in SUNDAOWNER_QUOTATION["labour"]
        if "ceiling" not in item["desc"].lower()
    ],
    "discount_label": "Client discount — Goodwill discount",
    "discount_amount": 800.00,
}


# ══════════════════════════════════════════════════════════════════════════════
# EXAMPLE 4 — Payment Request — Deposit (Trishan BRS-T1)
# Matches: PaymentRequest_Trishan_Deposit_BRS-T1.pdf
# ══════════════════════════════════════════════════════════════════════════════

TRISHAN_DEPOSIT = {
    "client_name": "Trishan",
    "client_address": "385 Cork Avenue, Ferndale, Randburg",
    "quotation_ref": "BRS-2026-0816-T1-FINALv3",
    "total_project_value": 23585.00,
    "payment_type": "deposit",
    "payment_pct": 57.6,  # R13,585 / R23,585 ≈ 57.6%
    "deposit_description": "Deposit — Material Procurement & Delivery",
    "works_start": "Wednesday, 19 August 2026",
    "bank": "fnb",
    "payment_ref": "BRS-T1",
    "custom_note": (
        "— this deposit covers both material procurement and delivery, "
        "so materials will be ordered and delivered promptly once payment "
        "reflects, with works beginning Wednesday 19 August 2026."
    ),
}


# ══════════════════════════════════════════════════════════════════════════════
# EXAMPLE 5 — Ferndale Multi-Scope (Style B, complex)
# Matches: Ferndale_MultiScope_Quotation_Trishan.pdf
# ══════════════════════════════════════════════════════════════════════════════

FERNDALE_MULTISCOPE = {
    "style": "B",
    "project_letter": "T1",
    "client_name": "Trishan",
    "client_address": "385 Cork Avenue, Ferndale, Randburg",
    "projected_start": "Wed/Thu (19–20 Aug 2026, TBC)",
    "project_description": (
        "Multi-scope works at client's residential property located at 385 Cork Avenue, "
        "Ferndale, Randburg. This quotation covers four separate work areas: (1) downpipe "
        "plumbing, (2) wall preparation & painting, (3) tiling, and (4) a new built-in "
        "braai/bright place with bench seating and firepit, built to the approved concept "
        "design against the existing boundary wall. Materials may be purchased directly by "
        "the client, or by BuildRight Solutions on the client's behalf using deposit funds, "
        "as agreed between both parties. This is a referral quotation — material costs shown "
        "are indicative and may vary once final shop prices are confirmed at time of purchase. "
        "Labour costs are payable to BuildRight Solutions."
    ),
    "measurements": [],
    "materials": [
        # Section 1 - Plumbing
        {"desc": "50 mm PVC pipe (long length)", "qty": "1 length", "cost": 180.00, "notes": "Downpipe connection run"},
        {"desc": "50 mm elbow joint", "qty": "3 units", "cost": 105.00, "notes": "Directs water into downpipe"},
        {"desc": "PVC glue", "qty": "1 tin", "cost": 95.00, "notes": "Joining pipes & elbows"},
        # Section 2 - Painting
        {"desc": "Colour paint (inside)", "qty": "10 L", "cost": 950.00, "notes": "Interior finish coat"},
        {"desc": "Colour paint (outside)", "qty": "10 L", "cost": 950.00, "notes": "Exterior finish coat"},
        {"desc": "Plastic grill", "qty": "5 m", "cost": 120.00, "notes": "Surface trim / protection"},
        # Section 3 - Tiling
        {"desc": "Grey grout (2 kg)", "qty": "1 pack", "cost": 55.00, "notes": "Tile jointing"},
        {"desc": "Tile adhesive", "qty": "2 bags", "cost": 360.00, "notes": "Fixing tiles"},
        {"desc": "Tile spacers", "qty": "1 pack", "cost": 45.00, "notes": "Even tile spacing"},
        # Section 4 - Braai
        {"desc": "Mampara (clay stock) bricks", "qty": "1 pallet", "cost": 950.00, "notes": "Braai surround & bench walls"},
        {"desc": "Brickforce", "qty": "2 rolls", "cost": 360.00, "notes": "Reinforcing between brick courses"},
        {"desc": "Reinforcing bar (Y10, 3 m)", "qty": "1 unit", "cost": 150.00, "notes": "Structural reinforcement"},
        {"desc": "Sealant / adhesive", "qty": "1 tube", "cost": 120.00, "notes": "Sealing & bonding"},
        {"desc": "Cement", "qty": "10 bags", "cost": 1400.00, "notes": "Brickwork & foundation"},
        {"desc": "Building sand", "qty": "1 bag", "cost": 70.00, "notes": "Floor base mix"},
        {"desc": "Skim mix (Skidmix)", "qty": "0.5 tub", "cost": 175.00, "notes": "Floor leveling compound"},
        {"desc": "Filler paint", "qty": "10 L", "cost": 650.00, "notes": "Surface filler coat"},
        {"desc": "Colour paint (braai)", "qty": "10 L", "cost": 950.00, "notes": "Finish coat"},
        {"desc": "Concrete lintels", "qty": "5×1m + 5×1.8m", "cost": 1900.00, "notes": "Structural support"},
    ],
    "labour": [
        # Section 1
        {"desc": "Install elbows & connect to downpipe", "qty": "9 m²", "cost": 1153.00, "notes": "Plumbing installation"},
        # Section 2
        {"desc": "Wall preparation (inside & outside)", "qty": "15 m²", "cost": 2130.00, "notes": "Cleaning, sanding & patching"},
        {"desc": "Painting (inside & outside, 2 coats)", "qty": "15 m²", "cost": 3197.00, "notes": "Full paint application"},
        # Section 3
        {"desc": "Tile laying", "qty": "5 m²", "cost": 1597.00, "notes": "Full tiling installation"},
        # Section 4
        {"desc": "Foundation, brickwork, firepit & flooring construction", "qty": "13 m²", "cost": 5923.00, "notes": "Full structural build & finish"},
    ],
    "material_notes": [
        "This is a referral quotation — material costs are indicative and may vary once "
        "final shop prices are confirmed at time of purchase.",
    ],
}


# ══════════════════════════════════════════════════════════════════════════════
# EXAMPLE 6 — Cottonwoods Painting (Style B)
# Matches: Cottonwoods_Quotation_Michelle.pdf
# ══════════════════════════════════════════════════════════════════════════════

COTTONWOODS_QUOTATION = {
    "style": "B",
    "project_letter": "P",
    "client_name": "Michelle",
    "client_address": "Cottonwoods, 19 Argyle Avenue, Craighall",
    "project_description": (
        "Wall preparation, patching and painting works at client's residential property "
        "located at Cottonwoods, 19 Argyle Avenue, Craighall. The scope covers full "
        "surface preparation (cleaning, sanding, crack and hole patching, filling of "
        "imperfections) followed by a complete paint finish across all specified walls. "
        "All materials are supplied by BuildRight Solutions and are included in the "
        "quoted total.\nTotal wall area: 234 m²"
    ),
    "materials": [
        {"desc": "Wall filler / crack patching compound", "qty": "15 kg", "cost": 1200.00, "notes": "Crack & hole patching"},
        {"desc": "Sandpaper (assorted)", "qty": "6 packs", "cost": 480.00, "notes": "Surface prep"},
        {"desc": "Primer / sealer", "qty": "40 L", "cost": 3600.00, "notes": "Seal patched areas"},
        {"desc": "Premium wall paint", "qty": "80 L", "cost": 10000.00, "notes": "2 finish coats"},
        {"desc": "Masking tape & plastic drop sheets", "qty": "6 sets", "cost": 360.00, "notes": "Surface & floor protection"},
    ],
    "labour": [
        {"desc": "Wall preparation, patching & sanding", "qty": "234 m²", "cost": 4680.00},
        {"desc": "Primer / sealer application", "qty": "234 m²", "cost": 2340.00},
        {"desc": "Premium paint application (2 coats)", "qty": "234 m²", "cost": 9360.00},
    ],
}


# ══════════════════════════════════════════════════════════════════════════════
# TEMPLATE — Blank Tiling Quotation (Style B)
# ══════════════════════════════════════════════════════════════════════════════

TILING_TEMPLATE = {
    "style": "B",
    "project_letter": "D",
    "client_name": "[Client Name]",
    "client_address": "[Property Address]",
    "projected_start": "TBC (subject to site survey)",
    "project_description": (
        "Strip-out of existing tiling, waterproofing and re-tiling at the client's "
        "residential property. The works are supplied and executed as a complete "
        "turnkey item — all materials listed below are supplied by BuildRight Solutions "
        "and are included in the quoted totals."
    ),
    "measurements": [
        {"element": "Tiling — run A", "dimension": "[dimension]", "area": "as measured"},
        {"element": "Tiling — run B", "dimension": "[dimension]", "area": "as measured"},
    ],
    "materials": [
        {"desc": "Cemex waterproofing compound", "qty": "10 L", "cost": 695.00, "notes": "Waterproofing application"},
        {"desc": "Tile adhesive — wall & floor", "qty": "[qty] × 20 kg bags", "cost": 0.00, "notes": "Fixing tiles"},
        {"desc": "Bonding liquid / tile mix additive", "qty": "5 L", "cost": 280.00, "notes": "Strengthens adhesive mix"},
        {"desc": "Waterproofing membrane cloth", "qty": "1 roll", "cost": 220.00, "notes": "Membrane layer"},
    ],
    "labour": [
        {"desc": "Removal and disposal of existing tiling", "qty": "All areas", "cost": 950.00},
        {"desc": "Waterproofing application", "qty": "All areas", "cost": 1100.00},
        {"desc": "Tile installation", "qty": "All areas", "cost": 1450.00},
    ],
}
