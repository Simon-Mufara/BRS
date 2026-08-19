#!/usr/bin/env python3
"""
BuildRight Solutions — Document Automation GUI
================================================
Professional desktop application for generating PDFs.

Run:
    python brs_agent/gui.py
"""

from __future__ import annotations

import json
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from datetime import date, timedelta
from typing import Any

# ── Path setup ──────────────────────────────────────────────────────────────
_HERE = os.path.dirname(os.path.abspath(__file__))
_OUTPUT = os.path.join(_HERE, "output")
_CLIENTS_DB = os.path.join(_HERE, "data", "clients.json")
os.makedirs(_OUTPUT, exist_ok=True)
os.makedirs(os.path.dirname(_CLIENTS_DB), exist_ok=True)

# Add parent to path for imports
sys.path.insert(0, os.path.dirname(_HERE))

from brs_agent import config as C
from brs_agent.quotation import QuotationGenerator
from brs_agent.payment_request import PaymentRequestGenerator
from brs_agent.invoice import InvoiceGenerator
from brs_agent.delivery_note import DeliveryNoteGenerator
from brs_agent.scope_of_works import ScopeOfWorksGenerator


# ── Colour Palette ──────────────────────────────────────────────────────────
BG_DARK      = "#1e1e2e"   # dark background
BG_SIDEBAR   = "#2b2b3d"   # sidebar
BG_CARD      = "#363649"   # card/panel
BG_INPUT     = "#44445a"   # input field
FG_PRIMARY   = "#16a085"   # teal accent
FG_WHITE     = "#e0e0e0"   # text
FG_GREY      = "#8888aa"   # muted text
FG_ACCENT    = "#f39c12"   # orange accent
BG_HOVER     = "#3d3d55"   # hover
BG_BUTTON    = "#16a085"   # button
FG_BUTTON    = "#ffffff"   # button text
FONT_FAMILY  = "Segoe UI"


# ── Client Database ─────────────────────────────────────────────────────────

def load_clients() -> dict:
    if os.path.exists(_CLIENTS_DB):
        with open(_CLIENTS_DB) as f:
            return json.load(f)
    return {}


def save_clients(clients: dict):
    with open(_CLIENTS_DB, "w") as f:
        json.dump(clients, f, indent=2)


# ── Styled Widgets ──────────────────────────────────────────────────────────

class StyledEntry(tk.Entry):
    """Dark-themed entry widget."""
    def __init__(self, master, **kw):
        kw.setdefault("bg", BG_INPUT)
        kw.setdefault("fg", FG_WHITE)
        kw.setdefault("insertbackground", FG_WHITE)
        kw.setdefault("font", (FONT_FAMILY, 10))
        kw.setdefault("relief", "flat")
        kw.setdefault("bd", 0)
        kw.setdefault("highlightthickness", 1)
        kw.setdefault("highlightbackground", "#555570")
        kw.setdefault("highlightcolor", FG_PRIMARY)
        super().__init__(master, **kw)


class StyledLabel(tk.Label):
    """Dark-themed label."""
    def __init__(self, master, **kw):
        kw.setdefault("bg", BG_CARD)
        kw.setdefault("fg", FG_WHITE)
        kw.setdefault("font", (FONT_FAMILY, 10))
        super().__init__(master, **kw)


class StyledButton(tk.Button):
    """Teal-themed button."""
    def __init__(self, master, **kw):
        kw.setdefault("bg", BG_BUTTON)
        kw.setdefault("fg", FG_BUTTON)
        kw.setdefault("font", (FONT_FAMILY, 10, "bold"))
        kw.setdefault("relief", "flat")
        kw.setdefault("cursor", "hand2")
        kw.setdefault("activebackground", FG_PRIMARY)
        kw.setdefault("activeforeground", FG_BUTTON)
        kw.setdefault("bd", 0)
        kw.setdefault("padx", 16)
        kw.setdefault("pady", 8)
        super().__init__(master, **kw)
        self.bind("<Enter>", lambda e: self.configure(bg="#1abc9c"))
        self.bind("<Leave>", lambda e: self.configure(bg=BG_BUTTON))


class StyledCombo(ttk.Combobox):
    """Themed combobox."""
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        style = ttk.Style()
        style.configure("Dark.TCombobox",
                        fieldbackground=BG_INPUT,
                        background=BG_INPUT,
                        foreground=FG_WHITE,
                        selectbackground=FG_PRIMARY)
        self.configure(style="Dark.TCombobox")


class StyledText(scrolledtext.ScrolledText):
    """Dark-themed scrolled text."""
    def __init__(self, master, **kw):
        kw.setdefault("bg", BG_INPUT)
        kw.setdefault("fg", FG_WHITE)
        kw.setdefault("insertbackground", FG_WHITE)
        kw.setdefault("font", (FONT_FAMILY, 10))
        kw.setdefault("relief", "flat")
        kw.setdefault("bd", 0)
        kw.setdefault("wrap", "word")
        super().__init__(master, **kw)


# ── Form Builder Helpers ────────────────────────────────────────────────────

def add_label(parent, text, row, col=0, **kw):
    lbl = StyledLabel(parent, text=text, **kw)
    lbl.grid(row=row, column=col, sticky="w", padx=(10, 5), pady=4)
    return lbl


def add_entry(parent, row, col=1, width=35, **kw):
    entry = StyledEntry(parent, width=width, **kw)
    entry.grid(row=row, column=col, sticky="ew", padx=(0, 10), pady=4)
    return entry


def add_combo(parent, row, values, col=1, width=33):
    combo = StyledCombo(parent, values=values, width=width, state="readonly")
    combo.grid(row=row, column=col, sticky="ew", padx=(0, 10), pady=4)
    combo.current(0)
    return combo


def add_text(parent, row, height=5, col=1, **kw):
    txt = StyledText(parent, height=height, **kw)
    txt.grid(row=row, column=col, sticky="ew", padx=(0, 10), pady=4)
    return txt


# ── Line Item Table ─────────────────────────────────────────────────────────

class LineItemTable(tk.Frame):
    """Editable table for materials, labour, or line items."""
    def __init__(self, master, columns: list[str], **kw):
        super().__init__(master, bg=BG_CARD, **kw)
        self.columns = columns
        self.rows: list[dict] = []
        self._build_header()
        self.add_row()  # start with one empty row

    def _build_header(self):
        for i, col in enumerate(self.columns):
            lbl = StyledLabel(self, text=col, font=(FONT_FAMILY, 9, "bold"),
                              bg=BG_SIDEBAR, fg=FG_PRIMARY)
            lbl.grid(row=0, column=i, sticky="ew", padx=1, pady=1)
            self.columnconfigure(i, weight=1)

    def add_row(self, values: dict | None = None):
        row_idx = len(self.rows) + 1
        row_data = {}
        for i, col in enumerate(self.columns):
            val = values.get(col, "") if values else ""
            entry = StyledEntry(self, width=15)
            entry.grid(row=row_idx, column=i, sticky="ew", padx=1, pady=1)
            entry.insert(0, str(val))
            row_data[col] = entry
        # Delete button
        del_btn = tk.Button(self, text="X", bg="#c0392b", fg="white",
                            font=(FONT_FAMILY, 8, "bold"), relief="flat",
                            command=lambda: self._delete_row(row_data),
                            width=3, cursor="hand2")
        del_btn.grid(row=row_idx, column=len(self.columns), padx=2, pady=1)
        row_data["_btn"] = del_btn
        self.rows.append(row_data)

    def _delete_row(self, row_data):
        if len(self.rows) <= 1:
            return
        for col in self.columns:
            row_data[col].destroy()
        row_data["_btn"].destroy()
        self.rows.remove(row_data)
        self._regrid()

    def _regrid(self):
        for i, row_data in enumerate(self.rows, 1):
            for j, col in enumerate(self.columns):
                row_data[col].grid(row=i, column=j, sticky="ew", padx=1, pady=1)
            row_data["_btn"].grid(row=i, column=len(self.columns), padx=2, pady=1)

    def get_rows(self) -> list[dict]:
        result = []
        for row_data in self.rows:
            row = {}
            for col in self.columns:
                row[col] = row_data[col].get().strip()
            # skip completely empty rows
            if any(row.values()):
                result.append(row)
        return result

    def clear(self):
        for row_data in self.rows:
            for col in self.columns:
                row_data[col].destroy()
            row_data["_btn"].destroy()
        self.rows.clear()
        self.add_row()


# ── Sidebar Button ──────────────────────────────────────────────────────────

class SidebarButton(tk.Button):
    def __init__(self, master, text, icon, command=None, **kw):
        super().__init__(master,
                         text=f"  {icon}  {text}",
                         bg=BG_SIDEBAR,
                         fg=FG_WHITE,
                         font=(FONT_FAMILY, 11),
                         anchor="w",
                         relief="flat",
                         bd=0,
                         padx=20,
                         pady=12,
                         cursor="hand2",
                         activebackground=BG_HOVER,
                         activeforeground=FG_PRIMARY,
                         command=command,
                         **kw)
        self.bind("<Enter>", lambda e: self.configure(bg=BG_HOVER))
        self.bind("<Leave>", lambda e: self.configure(bg=BG_SIDEBAR))


# ══════════════════════════════════════════════════════════════════════════════
# MAIN APPLICATION
# ══════════════════════════════════════════════════════════════════════════════

class BRSApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BuildRight Solutions - Document Automation Agent")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        self.root.configure(bg=BG_DARK)

        # Try to set dark title bar on Windows
        try:
            import ctypes
            hwnd = ctypes.windll.user32.GetForegroundWindow()
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd, 20, ctypes.byref(ctypes.c_int(1)), 4)
        except Exception:
            pass

        self.current_panel = None
        self.clients = load_clients()
        self.output_dir = _OUTPUT

        self._build_ui()

    def _build_ui(self):
        # ── Sidebar ──────────────────────────────────────────────────────
        sidebar = tk.Frame(self.root, bg=BG_SIDEBAR, width=260)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Logo area
        logo_frame = tk.Frame(sidebar, bg=BG_SIDEBAR)
        logo_frame.pack(fill="x", pady=(20, 10))

        tk.Label(logo_frame, text="BUILD", bg=BG_SIDEBAR, fg=FG_PRIMARY,
                 font=(FONT_FAMILY, 22, "bold")).pack(anchor="w", padx=20)
        tk.Label(logo_frame, text="RIGHT", bg=BG_SIDEBAR, fg=FG_WHITE,
                 font=(FONT_FAMILY, 22, "bold")).pack(anchor="w", padx=20)

        tk.Label(logo_frame, text="Document Automation",
                 bg=BG_SIDEBAR, fg=FG_GREY,
                 font=(FONT_FAMILY, 9)).pack(anchor="w", padx=20, pady=(2, 0))

        # Separator
        tk.Frame(sidebar, bg="#44445a", height=1).pack(fill="x", padx=15, pady=10)

        # Navigation buttons
        nav_items = [
            ("Quotation",         "\u270D",  self._show_quotation),
            ("Payment Request",   "\u2B50",  self._show_payment),
            ("Invoice",           "\u2709",  self._show_invoice),
            ("Delivery Note",     "\u270B",  self._show_delivery),
            ("Scope of Works",    "\u2611",  self._show_scope),
        ]

        for text, icon, cmd in nav_items:
            btn = SidebarButton(sidebar, text, icon, command=cmd)
            btn.pack(fill="x", padx=10, pady=2)

        # Separator
        tk.Frame(sidebar, bg="#44445a", height=1).pack(fill="x", padx=15, pady=10)

        # Client Manager button
        SidebarButton(sidebar, "Client Manager", "\u2615",
                      command=self._show_clients).pack(fill="x", padx=10, pady=2)

        # Output folder
        SidebarButton(sidebar, "Output Folder", "\u2630",
                      command=self._open_output).pack(fill="x", padx=10, pady=2)

        # Bottom info
        tk.Frame(sidebar, bg="#44445a", height=1).pack(fill="x", padx=15, pady=10)
        tk.Label(sidebar, text=f'"We Nail It, You Enjoy It!"',
                 bg=BG_SIDEBAR, fg=FG_GREY, font=(FONT_FAMILY, 8, "italic")).pack(pady=5)
        tk.Label(sidebar, text=f"Reg. {C.REG_NUMBER}",
                 bg=BG_SIDEBAR, fg=FG_GREY, font=(FONT_FAMILY, 7)).pack()

        # ── Main Content Area ────────────────────────────────────────────
        self.main = tk.Frame(self.root, bg=BG_DARK)
        self.main.pack(side="left", fill="both", expand=True)

        # Start with quotation panel
        self._show_quotation()

    def _clear_main(self):
        if self.current_panel:
            self.current_panel.destroy()
        self.current_panel = tk.Frame(self.main, bg=BG_DARK)
        self.current_panel.pack(fill="both", expand=True, padx=20, pady=20)

    def _open_output(self):
        os.startfile(self.output_dir) if os.name == "nt" else os.system(f"xdg-open '{self.output_dir}'")

    # ══════════════════════════════════════════════════════════════════════
    # QUOTATION PANEL
    # ══════════════════════════════════════════════════════════════════════

    def _show_quotation(self):
        self._clear_main()
        panel = self.current_panel

        # Title
        tk.Label(panel, text="Generate Quotation", bg=BG_DARK, fg=FG_PRIMARY,
                 font=(FONT_FAMILY, 18, "bold")).pack(anchor="w", pady=(0, 15))

        # Scrollable canvas
        canvas = tk.Canvas(panel, bg=BG_DARK, highlightthickness=0)
        scrollbar = ttk.Scrollbar(panel, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=BG_DARK)

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind("<MouseWheel>", _on_mousewheel)

        f = scroll_frame

        # ── Style & Client ───────────────────────────────────────────────
        card1 = tk.Frame(f, bg=BG_CARD, padx=15, pady=10)
        card1.pack(fill="x", pady=(0, 10))

        tk.Label(card1, text="Document Settings", bg=BG_CARD, fg=FG_PRIMARY,
                 font=(FONT_FAMILY, 12, "bold")).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 8))

        add_label(card1, "Style:", 1, 0)
        self.q_style = add_combo(card1, 1, ["A - Tabular (painting, crack repair)", "B - Clean (tiling, multi-scope)"])

        add_label(card1, "Project Letter:", 2, 0)
        self.q_letter = add_entry(card1, 2, width=10)
        self.q_letter.insert(0, "E")

        add_label(card1, "Client:", 3, 0)
        self.q_client = add_entry(card1, 3)
        self.q_client.bind("<KeyRelease>", lambda e: self._on_client_select())

        add_label(card1, "Client Preset:", 4, 0)
        client_names = ["(type client name above to filter)"] + list(self.clients.keys())
        self.q_client_preset = add_combo(card1, 4, client_names)
        self.q_client_preset.bind("<<ComboboxSelected>>", lambda e: self._apply_client_preset())

        add_label(card1, "Address:", 5, 0)
        self.q_address = add_entry(card1, 5)

        add_label(card1, "Project Title:", 6, 0)
        self.q_title = add_entry(card1, 6)
        self.q_title.insert(0, "Tiling, Waterproofing & Painting")

        # ── Description ──────────────────────────────────────────────────
        card2 = tk.Frame(f, bg=BG_CARD, padx=15, pady=10)
        card2.pack(fill="x", pady=(0, 10))

        tk.Label(card2, text="Project Description", bg=BG_CARD, fg=FG_PRIMARY,
                 font=(FONT_FAMILY, 12, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))
        self.q_desc = add_text(card2, 1, height=4)
        card2.columnconfigure(1, weight=1)

        # ── Materials Table ──────────────────────────────────────────────
        card3 = tk.Frame(f, bg=BG_CARD, padx=15, pady=10)
        card3.pack(fill="x", pady=(0, 10))

        tk.Label(card3, text="Materials", bg=BG_CARD, fg=FG_PRIMARY,
                 font=(FONT_FAMILY, 12, "bold")).pack(anchor="w", pady=(0, 8))

        self.q_mat_table = LineItemTable(card3, ["desc", "qty", "cost"])
        self.q_mat_table.pack(fill="x")

        StyledButton(card3, text="+ Add Material",
                     command=lambda: self.q_mat_table.add_row()).pack(anchor="w", pady=5)

        # ── Labour Table ─────────────────────────────────────────────────
        card4 = tk.Frame(f, bg=BG_CARD, padx=15, pady=10)
        card4.pack(fill="x", pady=(0, 10))

        tk.Label(card4, text="Labour", bg=BG_CARD, fg=FG_PRIMARY,
                 font=(FONT_FAMILY, 12, "bold")).pack(anchor="w", pady=(0, 8))

        self.q_lab_table = LineItemTable(card4, ["desc", "qty", "cost"])
        self.q_lab_table.pack(fill="x")

        StyledButton(card4, text="+ Add Labour Item",
                     command=lambda: self.q_lab_table.add_row()).pack(anchor="w", pady=5)

        # ── Discount ─────────────────────────────────────────────────────
        card5 = tk.Frame(f, bg=BG_CARD, padx=15, pady=10)
        card5.pack(fill="x", pady=(0, 10))

        tk.Label(card5, text="Discount (Optional)", bg=BG_CARD, fg=FG_PRIMARY,
                 font=(FONT_FAMILY, 12, "bold")).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 8))

        add_label(card5, "Label:", 1, 0)
        self.q_disc_label = add_entry(card5, 1, width=20)

        add_label(card5, "Amount (R):", 2, 0)
        self.q_disc_amount = add_entry(card5, 2, width=15)
        self.q_disc_amount.insert(0, "0")

        # ── Output ───────────────────────────────────────────────────────
        card6 = tk.Frame(f, bg=BG_CARD, padx=15, pady=10)
        card6.pack(fill="x", pady=(0, 10))

        tk.Label(card6, text="Output", bg=BG_CARD, fg=FG_PRIMARY,
                 font=(FONT_FAMILY, 12, "bold")).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 8))

        add_label(card6, "Filename:", 1, 0)
        self.q_filename = add_entry(card6, 1, width=35)
        self.q_filename.insert(0, "Quotation.pdf")

        # ── Generate Button ──────────────────────────────────────────────
        btn_frame = tk.Frame(f, bg=BG_DARK)
        btn_frame.pack(fill="x", pady=10)

        StyledButton(btn_frame, text="  GENERATE QUOTATION  ",
                     command=self._generate_quotation,
                     font=(FONT_FAMILY, 12, "bold"),
                     padx=30, pady=12).pack(side="left")

        StyledButton(btn_frame, text="  Clear Form  ",
                     command=lambda: self._clear_quotation_form(),
                     bg="#555570", padx=20).pack(side="left", padx=10)

    def _on_client_select(self):
        name = self.q_client.get().strip()
        if name in self.clients:
            c = self.clients[name]
            self.q_address.delete(0, "end")
            self.q_address.insert(0, c.get("address", ""))

    def _apply_client_preset(self):
        name = self.q_client_preset.get()
        if name.startswith("("):
            return
        if name in self.clients:
            c = self.clients[name]
            self.q_client.delete(0, "end")
            self.q_client.insert(0, name)
            self.q_address.delete(0, "end")
            self.q_address.insert(0, c.get("address", ""))

    def _clear_quotation_form(self):
        self.q_client.delete(0, "end")
        self.q_address.delete(0, "end")
        self.q_desc.delete("1.0", "end")
        self.q_mat_table.clear()
        self.q_lab_table.clear()
        self.q_disc_label.delete(0, "end")
        self.q_disc_amount.delete(0, "end")
        self.q_disc_amount.insert(0, "0")

    def _generate_quotation(self):
        style = "A" if self.q_style.get().startswith("A") else "B"
        materials = [{"desc": r["desc"], "qty": r["qty"], "cost": float(r["cost"] or 0)}
                     for r in self.q_mat_table.get_rows()]
        labour = [{"desc": r["desc"], "qty": r["qty"], "cost": float(r["cost"] or 0)}
                  for r in self.q_lab_table.get_rows()]

        data = {
            "style": style,
            "project_letter": self.q_letter.get().strip() or "E",
            "client_name": self.q_client.get().strip() or "[Client Name]",
            "client_address": self.q_address.get().strip() or "[Address]",
            "project_title": self.q_title.get().strip(),
            "project_description": self.q_desc.get("1.0", "end").strip(),
            "materials": materials,
            "labour": labour,
            "discount_label": self.q_disc_label.get().strip() or None,
            "discount_amount": float(self.q_disc_amount.get().strip() or 0),
        }

        filename = self.q_filename.get().strip() or "Quotation.pdf"
        if not filename.endswith(".pdf"):
            filename += ".pdf"
        path = os.path.join(self.output_dir, filename)

        try:
            gen = QuotationGenerator()
            gen.build(data)
            gen.save(path)
            messagebox.showinfo("Success", f"Quotation saved!\n\n{path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate quotation:\n\n{e}")

    # ══════════════════════════════════════════════════════════════════════
    # PAYMENT REQUEST PANEL
    # ══════════════════════════════════════════════════════════════════════

    def _show_payment(self):
        self._clear_main()
        panel = self.current_panel

        tk.Label(panel, text="Generate Payment Request", bg=BG_DARK, fg=FG_PRIMARY,
                 font=(FONT_FAMILY, 18, "bold")).pack(anchor="w", pady=(0, 15))

        f = tk.Frame(panel, bg=BG_DARK)
        f.pack(fill="both", expand=True)

        card = tk.Frame(f, bg=BG_CARD, padx=15, pady=15)
        card.pack(fill="x", pady=(0, 10))

        tk.Label(card, text="Payment Details", bg=BG_CARD, fg=FG_PRIMARY,
                 font=(FONT_FAMILY, 12, "bold")).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 10))

        add_label(card, "Client Name:", 1, 0)
        self.p_client = add_entry(card, 1)

        add_label(card, "Client Address:", 2, 0)
        self.p_address = add_entry(card, 2)

        add_label(card, "Quotation Ref:", 3, 0)
        self.p_ref = add_entry(card, 3)

        add_label(card, "Total Project Value (R):", 4, 0)
        self.p_total = add_entry(card, 4, width=20)

        add_label(card, "Payment Type:", 5, 0)
        self.p_type = add_combo(card, 5, ["Deposit", "Final Balance", "Progress Payment"])

        add_label(card, "Payment %:", 6, 0)
        self.p_pct = add_entry(card, 6, width=10)
        self.p_pct.insert(0, "50")

        add_label(card, "Payment Amount (R):", 7, 0)
        self.p_amount = add_entry(card, 7, width=10)
        self.p_amount.insert(0, "")

        add_label(card, "Description:", 7, 0)
        self.p_desc = add_entry(card, 7)
        self.p_desc.insert(0, "Deposit - Material Procurement & Delivery")

        add_label(card, "Works Start:", 8, 0)
        self.p_start = add_entry(card, 8)

        add_label(card, "Bank:", 9, 0)
        self.p_bank = add_combo(card, 9, ["fnb", "capitec"])

        add_label(card, "Payment Ref:", 10, 0)
        self.p_payref = add_entry(card, 10)

        add_label(card, "Custom Note:", 11, 0)
        self.p_note = add_entry(card, 11)

        add_label(card, "Filename:", 12, 0)
        self.p_filename = add_entry(card, 12)
        self.p_filename.insert(0, "PaymentRequest.pdf")

        # Auto-calculate percentage when type changes
        def _on_type_change(event=None):
            t = self.p_type.get()
            if "Deposit" in t:
                self.p_pct.delete(0, "end")
                self.p_pct.insert(0, "50")
                self.p_amount.delete(0, "end")  # Clear amount when type changes
            elif "Final" in t:
                self.p_pct.delete(0, "end")
                self.p_pct.insert(0, "100")
                self.p_amount.delete(0, "end")  # Clear amount when type changes

        self.p_type.bind("<<ComboboxSelected>>", _on_type_change)

        # Generate button
        btn_frame = tk.Frame(f, bg=BG_DARK)
        btn_frame.pack(fill="x", pady=10)

        StyledButton(btn_frame, text="  GENERATE PAYMENT REQUEST  ",
                     command=self._generate_payment,
                     font=(FONT_FAMILY, 12, "bold"), padx=30, pady=12).pack(side="left")

    def _generate_payment(self):
        data = {
            "client_name": self.p_client.get().strip(),
            "client_address": self.p_address.get().strip(),
            "quotation_ref": self.p_ref.get().strip(),
            "total_project_value": float(self.p_total.get().strip() or 0),
            "payment_type": self.p_type.get().lower().replace(" ", "_"),
            "payment_pct": float(self.p_pct.get().strip() or 50),
            "payment_amount": float(self.p_amount.get().strip()) if self.p_amount.get().strip() else None,
            "deposit_description": self.p_desc.get().strip(),
            "works_start": self.p_start.get().strip(),
            "bank": self.p_bank.get(),
            "payment_ref": self.p_payref.get().strip(),
            "custom_note": self.p_note.get().strip(),
        }

        filename = self.p_filename.get().strip() or "PaymentRequest.pdf"
        if not filename.endswith(".pdf"):
            filename += ".pdf"
        path = os.path.join(self.output_dir, filename)

        try:
            gen = PaymentRequestGenerator()
            gen.build(data)
            gen.save(path)
            messagebox.showinfo("Success", f"Payment request saved!\n\n{path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate payment request:\n\n{e}")

    # ══════════════════════════════════════════════════════════════════════
    # INVOICE PANEL
    # ══════════════════════════════════════════════════════════════════════

    def _show_invoice(self):
        self._clear_main()
        panel = self.current_panel

        tk.Label(panel, text="Generate Invoice", bg=BG_DARK, fg=FG_PRIMARY,
                 font=(FONT_FAMILY, 18, "bold")).pack(anchor="w", pady=(0, 15))

        f = tk.Frame(panel, bg=BG_DARK)
        f.pack(fill="both", expand=True)

        card = tk.Frame(f, bg=BG_CARD, padx=15, pady=10)
        card.pack(fill="x", pady=(0, 10))

        tk.Label(card, text="Invoice Details", bg=BG_CARD, fg=FG_PRIMARY,
                 font=(FONT_FAMILY, 12, "bold")).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 10))

        add_label(card, "Client Name:", 1, 0)
        self.i_client = add_entry(card, 1)

        add_label(card, "Address:", 2, 0)
        self.i_address = add_entry(card, 2)

        add_label(card, "Quotation Ref:", 3, 0)
        self.i_ref = add_entry(card, 3)

        add_label(card, "Invoice No (auto):", 4, 0)
        self.i_number = add_entry(card, 4)
        self.i_number.insert(0, "(auto-generated)")

        add_label(card, "VAT Rate:", 5, 0)
        self.i_vat = add_combo(card, 5, ["0.0 (No VAT)", "0.15 (15% VAT)"])

        add_label(card, "Notes:", 6, 0)
        self.i_notes = add_entry(card, 6)

        add_label(card, "Filename:", 7, 0)
        self.i_filename = add_entry(card, 7)
        self.i_filename.insert(0, "Invoice.pdf")

        # Line items table
        card2 = tk.Frame(f, bg=BG_CARD, padx=15, pady=10)
        card2.pack(fill="x", pady=(0, 10))

        tk.Label(card2, text="Line Items", bg=BG_CARD, fg=FG_PRIMARY,
                 font=(FONT_FAMILY, 12, "bold")).pack(anchor="w", pady=(0, 8))

        self.i_table = LineItemTable(card2, ["desc", "qty", "rate"])
        self.i_table.pack(fill="x")

        StyledButton(card2, text="+ Add Line Item",
                     command=lambda: self.i_table.add_row()).pack(anchor="w", pady=5)

        btn_frame = tk.Frame(f, bg=BG_DARK)
        btn_frame.pack(fill="x", pady=10)

        StyledButton(btn_frame, text="  GENERATE INVOICE  ",
                     command=self._generate_invoice,
                     font=(FONT_FAMILY, 12, "bold"), padx=30, pady=12).pack(side="left")

    def _generate_invoice(self):
        items = []
        for r in self.i_table.get_rows():
            rate = float(r.get("rate", 0) or 0)
            qty = float(r.get("qty", 1) or 1)
            items.append({"desc": r["desc"], "qty": str(int(qty)) if qty == int(qty) else str(qty),
                          "rate": rate, "amount": rate * qty})

        vat_str = self.i_vat.get()
        vat_rate = 0.15 if "15%" in vat_str else 0.0

        inv_no = self.i_number.get().strip()
        if inv_no.startswith("(") or not inv_no:
            inv_no = None

        data = {
            "client_name": self.i_client.get().strip(),
            "client_address": self.i_address.get().strip(),
            "quotation_ref": self.i_ref.get().strip(),
            "invoice_number": inv_no,
            "line_items": items,
            "vat_rate": vat_rate,
            "notes": self.i_notes.get().strip(),
        }

        filename = self.i_filename.get().strip() or "Invoice.pdf"
        if not filename.endswith(".pdf"):
            filename += ".pdf"
        path = os.path.join(self.output_dir, filename)

        try:
            gen = InvoiceGenerator()
            gen.build(data)
            gen.save(path)
            messagebox.showinfo("Success", f"Invoice saved!\n\n{path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate invoice:\n\n{e}")

    # ══════════════════════════════════════════════════════════════════════
    # DELIVERY NOTE PANEL
    # ══════════════════════════════════════════════════════════════════════

    def _show_delivery(self):
        self._clear_main()
        panel = self.current_panel

        tk.Label(panel, text="Generate Delivery Note", bg=BG_DARK, fg=FG_PRIMARY,
                 font=(FONT_FAMILY, 18, "bold")).pack(anchor="w", pady=(0, 15))

        f = tk.Frame(panel, bg=BG_DARK)
        f.pack(fill="both", expand=True)

        card = tk.Frame(f, bg=BG_CARD, padx=15, pady=10)
        card.pack(fill="x", pady=(0, 10))

        tk.Label(card, text="Delivery Details", bg=BG_CARD, fg=FG_PRIMARY,
                 font=(FONT_FAMILY, 12, "bold")).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 10))

        add_label(card, "Client Name:", 1, 0)
        self.d_client = add_entry(card, 1)

        add_label(card, "Site Address:", 2, 0)
        self.d_address = add_entry(card, 2)

        add_label(card, "Quotation Ref:", 3, 0)
        self.d_ref = add_entry(card, 3)

        add_label(card, "Delivered By:", 4, 0)
        self.d_delivered = add_entry(card, 4)
        self.d_delivered.insert(0, C.DIRECTOR_NAME)

        add_label(card, "Vehicle Ref:", 5, 0)
        self.d_vehicle = add_entry(card, 5)

        add_label(card, "Notes:", 6, 0)
        self.d_notes = add_entry(card, 6)

        add_label(card, "Filename:", 7, 0)
        self.d_filename = add_entry(card, 7)
        self.d_filename.insert(0, "DeliveryNote.pdf")

        # Items table
        card2 = tk.Frame(f, bg=BG_CARD, padx=15, pady=10)
        card2.pack(fill="x", pady=(0, 10))

        tk.Label(card2, text="Items to Deliver", bg=BG_CARD, fg=FG_PRIMARY,
                 font=(FONT_FAMILY, 12, "bold")).pack(anchor="w", pady=(0, 8))

        self.d_table = LineItemTable(card2, ["desc", "qty", "unit"])
        self.d_table.pack(fill="x")

        StyledButton(card2, text="+ Add Item",
                     command=lambda: self.d_table.add_row()).pack(anchor="w", pady=5)

        btn_frame = tk.Frame(f, bg=BG_DARK)
        btn_frame.pack(fill="x", pady=10)

        StyledButton(btn_frame, text="  GENERATE DELIVERY NOTE  ",
                     command=self._generate_delivery,
                     font=(FONT_FAMILY, 12, "bold"), padx=30, pady=12).pack(side="left")

    def _generate_delivery(self):
        items = [{"desc": r["desc"], "qty": r["qty"], "unit": r["unit"]}
                 for r in self.d_table.get_rows()]

        data = {
            "client_name": self.d_client.get().strip(),
            "client_address": self.d_address.get().strip(),
            "quotation_ref": self.d_ref.get().strip(),
            "delivered_by": self.d_delivered.get().strip(),
            "vehicle_ref": self.d_vehicle.get().strip(),
            "items": items,
            "notes": self.d_notes.get().strip(),
        }

        filename = self.d_filename.get().strip() or "DeliveryNote.pdf"
        if not filename.endswith(".pdf"):
            filename += ".pdf"
        path = os.path.join(self.output_dir, filename)

        try:
            gen = DeliveryNoteGenerator()
            gen.build(data)
            gen.save(path)
            messagebox.showinfo("Success", f"Delivery note saved!\n\n{path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate delivery note:\n\n{e}")

    # ══════════════════════════════════════════════════════════════════════
    # SCOPE OF WORKS PANEL
    # ══════════════════════════════════════════════════════════════════════

    def _show_scope(self):
        self._clear_main()
        panel = self.current_panel

        tk.Label(panel, text="Generate Scope of Works", bg=BG_DARK, fg=FG_PRIMARY,
                 font=(FONT_FAMILY, 18, "bold")).pack(anchor="w", pady=(0, 15))

        # Scrollable
        canvas = tk.Canvas(panel, bg=BG_DARK, highlightthickness=0)
        scrollbar = ttk.Scrollbar(panel, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=BG_DARK)
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind("<MouseWheel>", _on_mousewheel)

        f = scroll_frame

        card = tk.Frame(f, bg=BG_CARD, padx=15, pady=10)
        card.pack(fill="x", pady=(0, 10))

        tk.Label(card, text="Project Details", bg=BG_CARD, fg=FG_PRIMARY,
                 font=(FONT_FAMILY, 12, "bold")).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 10))

        add_label(card, "Client Name:", 1, 0)
        self.s_client = add_entry(card, 1)

        add_label(card, "Address:", 2, 0)
        self.s_address = add_entry(card, 2)

        add_label(card, "Quotation Ref:", 3, 0)
        self.s_ref = add_entry(card, 3)

        add_label(card, "Project Title:", 4, 0)
        self.s_title = add_entry(card, 4)
        self.s_title.insert(0, "Scope of Works")

        add_label(card, "Start Date:", 5, 0)
        self.s_start = add_entry(card, 5)
        self.s_start.insert(0, "TBC")

        add_label(card, "Duration:", 6, 0)
        self.s_duration = add_entry(card, 6)
        self.s_duration.insert(0, "TBC")

        add_label(card, "Filename:", 7, 0)
        self.s_filename = add_entry(card, 7)
        self.s_filename.insert(0, "ScopeOfWorks.pdf")

        card2 = tk.Frame(f, bg=BG_CARD, padx=15, pady=10)
        card2.pack(fill="x", pady=(0, 10))
        tk.Label(card2, text="Project Description", bg=BG_CARD, fg=FG_PRIMARY,
                 font=(FONT_FAMILY, 12, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))
        self.s_desc = add_text(card2, 1, height=3)
        card2.columnconfigure(1, weight=1)

        card3 = tk.Frame(f, bg=BG_CARD, padx=15, pady=10)
        card3.pack(fill="x", pady=(0, 10))
        tk.Label(card3, text="Exclusions", bg=BG_CARD, fg=FG_PRIMARY,
                 font=(FONT_FAMILY, 12, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))
        self.s_exclusions = add_text(card3, 1, height=3)
        card3.columnconfigure(1, weight=1)

        btn_frame = tk.Frame(f, bg=BG_DARK)
        btn_frame.pack(fill="x", pady=10)

        StyledButton(btn_frame, text="  GENERATE SCOPE OF WORKS  ",
                     command=self._generate_scope,
                     font=(FONT_FAMILY, 12, "bold"), padx=30, pady=12).pack(side="left")

    def _generate_scope(self):
        exclusions = [line.strip() for line in self.s_exclusions.get("1.0", "end").split("\n") if line.strip()]

        data = {
            "client_name": self.s_client.get().strip(),
            "client_address": self.s_address.get().strip(),
            "quotation_ref": self.s_ref.get().strip(),
            "project_title": self.s_title.get().strip(),
            "project_description": self.s_desc.get("1.0", "end").strip(),
            "projected_start": self.s_start.get().strip(),
            "estimated_duration": self.s_duration.get().strip(),
            "exclusions": exclusions,
        }

        filename = self.s_filename.get().strip() or "ScopeOfWorks.pdf"
        if not filename.endswith(".pdf"):
            filename += ".pdf"
        path = os.path.join(self.output_dir, filename)

        try:
            gen = ScopeOfWorksGenerator()
            gen.build(data)
            gen.save(path)
            messagebox.showinfo("Success", f"Scope of works saved!\n\n{path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate scope of works:\n\n{e}")

    # ══════════════════════════════════════════════════════════════════════
    # CLIENT MANAGER PANEL
    # ══════════════════════════════════════════════════════════════════════

    def _show_clients(self):
        self._clear_main()
        panel = self.current_panel

        tk.Label(panel, text="Client Manager", bg=BG_DARK, fg=FG_PRIMARY,
                 font=(FONT_FAMILY, 18, "bold")).pack(anchor="w", pady=(0, 15))

        # Add new client form
        card = tk.Frame(panel, bg=BG_CARD, padx=15, pady=10)
        card.pack(fill="x", pady=(0, 10))

        tk.Label(card, text="Add / Edit Client", bg=BG_CARD, fg=FG_PRIMARY,
                 font=(FONT_FAMILY, 12, "bold")).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 10))

        add_label(card, "Client Name:", 1, 0)
        self.c_name = add_entry(card, 1)

        add_label(card, "Address:", 2, 0)
        self.c_addr = add_entry(card, 2)

        add_label(card, "Phone:", 3, 0)
        self.c_phone = add_entry(card, 3)

        add_label(card, "Email:", 4, 0)
        self.c_email = add_entry(card, 4)

        btn_f = tk.Frame(card, bg=BG_CARD)
        btn_f.grid(row=5, column=1, sticky="w", pady=5)

        StyledButton(btn_f, text="Save Client", command=self._save_client).pack(side="left")
        StyledButton(btn_f, text="Delete Client", command=self._delete_client,
                     bg="#c0392b").pack(side="left", padx=5)

        # Client list
        card2 = tk.Frame(panel, bg=BG_CARD, padx=15, pady=10)
        card2.pack(fill="both", expand=True, pady=(0, 10))

        tk.Label(card2, text="Saved Clients", bg=BG_CARD, fg=FG_PRIMARY,
                 font=(FONT_FAMILY, 12, "bold")).pack(anchor="w", pady=(0, 8))

        self.client_list = tk.Listbox(card2, bg=BG_INPUT, fg=FG_WHITE,
                                      font=(FONT_FAMILY, 10), relief="flat",
                                      selectbackground=FG_PRIMARY,
                                      selectforeground="white")
        self.client_list.pack(fill="both", expand=True)
        self.client_list.bind("<<ListboxSelect>>", self._on_client_click)
        self._refresh_client_list()

    def _refresh_client_list(self):
        self.client_list.delete(0, "end")
        for name in sorted(self.clients.keys()):
            self.client_list.insert("end", name)

    def _on_client_click(self, event):
        sel = self.client_list.curselection()
        if not sel:
            return
        name = self.client_list.get(sel[0])
        c = self.clients.get(name, {})
        self.c_name.delete(0, "end")
        self.c_name.insert(0, name)
        self.c_addr.delete(0, "end")
        self.c_addr.insert(0, c.get("address", ""))
        self.c_phone.delete(0, "end")
        self.c_phone.insert(0, c.get("phone", ""))
        self.c_email.delete(0, "end")
        self.c_email.insert(0, c.get("email", ""))

    def _save_client(self):
        name = self.c_name.get().strip()
        if not name:
            messagebox.showwarning("Warning", "Client name is required.")
            return
        self.clients[name] = {
            "address": self.c_addr.get().strip(),
            "phone": self.c_phone.get().strip(),
            "email": self.c_email.get().strip(),
        }
        save_clients(self.clients)
        self._refresh_client_list()
        messagebox.showinfo("Saved", f"Client '{name}' saved.")

    def _delete_client(self):
        name = self.c_name.get().strip()
        if name in self.clients:
            if messagebox.askyesno("Confirm", f"Delete client '{name}'?"):
                del self.clients[name]
                save_clients(self.clients)
                self._refresh_client_list()
                self.c_name.delete(0, "end")
                self.c_addr.delete(0, "end")
                self.c_phone.delete(0, "end")
                self.c_email.delete(0, "end")

    # ══════════════════════════════════════════════════════════════════════
    # RUN
    # ══════════════════════════════════════════════════════════════════════

    def run(self):
        self.root.mainloop()


# ── Entry Point ─────────────────────────────────────────────────────────────

def main():
    app = BRSApp()
    app.run()


if __name__ == "__main__":
    main()
