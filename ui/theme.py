# ui/theme.py

"""
ui/theme.py
Paleta de cores, fontes e helpers de widget compartilhados por toda a UI.
"""
import tkinter as tk

# ─────────────────────────────────────────
#  PALETA
# ─────────────────────────────────────────
C = {
    "bg":       "#1c2130",
    "surface":  "#232938",
    "surface2": "#2a3245",
    "surface3": "#313b52",
    "border":   "#3a4561",
    "border2":  "#4a5575",
    "accent":   "#4d9cf8",
    "accent_dk":"#3b82d4",
    "text":     "#e8edf5",
    "text2":    "#9aabc5",
    "text3":    "#5e7099",
    "success":  "#3ecf8e",
    "warning":  "#f5a623",
    "danger":   "#f06b6b",
    "sidebar":  "#1a1f2e",
}

# ─────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────
def frame(parent, bg=None, **kw):
    return tk.Frame(parent, bg=bg or C["bg"], **kw)

def label(parent, text, fg=None, bg=None, size=10, bold=False, **kw):
    f = ("Segoe UI", size, "bold" if bold else "normal")
    return tk.Label(parent, text=text,
                    fg=fg or C["text"],
                    bg=bg or C["bg"],
                    font=f, **kw)

def divider(parent, bg_parent=None):
    """Linha horizontal separadora."""
    return tk.Frame(parent, bg=C["border"], height=1)

def section_header(parent, title, link_text="Ver todos →", bg=None):
    bg = bg or C["bg"]
    f = frame(parent, bg=bg)
    label(f, title, fg=C["text"], bg=bg, size=10, bold=True).pack(side="left")
    tk.Label(f, text=link_text, fg=C["accent"], bg=bg,
             font=("Segoe UI", 8), cursor="hand2").pack(side="right")
    return f