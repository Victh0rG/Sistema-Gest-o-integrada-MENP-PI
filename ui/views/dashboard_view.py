import customtkinter as ctk
from theme import Colors, Fonts
"""
ui/views/dashboard_view.py
Tela inicial — Dashboard com estatísticas, reuniões, documentos e alertas.
"""
import tkinter as tk
from tkinter import ttk
import datetime
from ui.theme import C, frame, label, section_header
from ui.components.notification_bar import NotificationBar
from ui.components.data_table import DataTable

# ── dados de exemplo ─────────────────────
STATS = [
    ("Atendimentos", "284", "+12 este mês",    C["accent"],  "📋"),
    ("Reuniões",     "47",  "3 esta semana",    C["success"], "📅"),
    ("Documentos",   "1.2k","+38 este mês",     C["warning"], "📄"),
    ("Pendências",   "6",   "arquivos faltando", C["danger"],  "⚠"),
]

MEETINGS_COLS = [
    {"header": "Reunião",   "key": "nome",     "width_chars": 30},
    {"header": "Data",      "key": "data",     "width_chars": 12},
    {"header": "Arquivos",  "key": "arquivos", "width_chars": 10},
    {"header": "Status",    "key": "status",   "width_chars": 0,
     "type": "badge", "align": "right", "badge_bg": C["surface3"]},
]

MEETINGS_ROWS = [
    {"nome": "Reunião Ordinária",      "data": "03/06/2025",
     "arquivos": ("3 / 3", C["success"]), "status": ("Completo", C["success"])},
    {"nome": "Reunião Extraordinária", "data": "11/06/2025",
     "arquivos": ("2 / 5", C["warning"]), "status": ("Pendente", C["warning"])},
    {"nome": "Atendimento Coletivo",   "data": "18/06/2025",
     "arquivos": ("5 / 5", C["success"]), "status": ("Completo", C["success"])},
    {"nome": "Reunião Plenária",       "data": "25/06/2025",
     "arquivos": ("0 / 4", C["danger"]),  "status": ("Pendente", C["warning"])},
]

DOCS_COLS = [
    {"header": "Documento",  "key": "nome",    "width_chars": 34},
    {"header": "Tamanho",    "key": "tamanho", "width_chars": 10},
    {"header": "Status",     "key": "status",  "width_chars": 0,
     "type": "badge", "align": "right", "badge_bg": C["surface3"]},
]

DOCS_ROWS = [
    {"nome": "Ata_Reuniao_Jun2025.pdf",      "tamanho": "2.4 MB",
     "status": ("✓ Processado", C["success"])},
    {"nome": "Relatorio_Atendimentos.docx",  "tamanho": "845 KB",
     "status": ("↑ Enviando",   C["accent"])},
    {"nome": "Planilha_Processos_2025.xlsx", "tamanho": "1.1 MB",
     "status": ("Aguardando",   C["text3"])},
    {"nome": "Ata_Reuniao_Mai2025.pdf",      "tamanho": "1.8 MB",
     "status": ("✓ Processado", C["success"])},
]

NOTIFICATIONS = [
    {"icon": "⚠", "title": "Reunião Plenária (25/06)",
     "body": "Esperados: 4 arquivos — Recebidos: 0", "color": C["warning"]},
    {"icon": "⚠", "title": "Reunião Extraordinária (11/06)",
     "body": "Esperados: 5 arquivos — Recebidos: 2", "color": C["warning"]},
    {"icon": "✅", "title": "IA processou Ata_Jun2025.pdf",
     "body": "Dados prontos para revisão",            "color": C["success"]},
]


class _StatCard(tk.Frame):
    def __init__(self, parent, title, value, sub, color, icon):
        super().__init__(parent, bg=C["surface"], padx=18, pady=16,
                         highlightbackground=C["border"], highlightthickness=1)
        top = frame(self, bg=C["surface"])
        top.pack(fill="x")
        tk.Label(top, text=icon, bg=C["surface2"], fg=color,
                 font=("Segoe UI", 14), padx=8, pady=4).pack(side="left")
        label(top, title, fg=C["text2"], bg=C["surface"], size=8).pack(
            side="left", padx=10)
        label(self, value, fg=C["text"], bg=C["surface"],
              size=22, bold=True).pack(anchor="w", pady=(10, 2))
        sf = frame(self, bg=C["surface"])
        sf.pack(anchor="w")
        tk.Label(sf, text="●", fg=color, bg=C["surface"],
                 font=("Segoe UI", 6)).pack(side="left")
        label(sf, f"  {sub}", fg=C["text3"], bg=C["surface"], size=8).pack(side="left")


class DashboardView(tk.Frame):
    """Tela principal — Dashboard."""

    def __init__(self, parent):
        super().__init__(parent, bg=C["bg"])
        self._build()

    def _build(self):
        self._topbar()
        tk.Frame(self, bg=C["border"], height=1).pack(fill="x")
        self._scrollable_content()

    def _topbar(self):
        top = frame(self, bg=C["surface"])
        top.pack(fill="x")
        label(top, "Dashboard", fg=C["text"], bg=C["surface"],
              size=13, bold=True).pack(side="left", padx=20, pady=14)
        now = datetime.datetime.now().strftime("%d/%m/%Y  %H:%M")
        label(top, now, fg=C["text3"], bg=C["surface"],
              size=8).pack(side="right", padx=20)
        # search bar decorativa
        sb = tk.Frame(top, bg=C["surface2"],
                      highlightbackground=C["border"], highlightthickness=1)
        sb.pack(side="right", padx=10, pady=10)
        tk.Label(sb, text="🔍  Buscar…", fg=C["text3"], bg=C["surface2"],
                 font=("Segoe UI", 9), padx=12, pady=5).pack(side="left")
        tk.Label(sb, text="⌘K", fg=C["text3"], bg=C["surface3"],
                 font=("Courier New", 8), padx=6, pady=3).pack(side="left", padx=4)

    def _scrollable_content(self):
        wrap = frame(self, bg=C["bg"])
        wrap.pack(fill="both", expand=True)

        cv = tk.Canvas(wrap, bg=C["bg"], highlightthickness=0)
        sb = ttk.Scrollbar(wrap, orient="vertical", command=cv.yview)
        inner = tk.Frame(cv, bg=C["bg"])

        inner.bind("<Configure>",
                   lambda e: cv.configure(scrollregion=cv.bbox("all")))
        cv.create_window((0, 0), window=inner, anchor="nw")
        cv.configure(yscrollcommand=sb.set)
        cv.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        cv.bind_all("<MouseWheel>",
                    lambda e: cv.yview_scroll(int(-1*(e.delta/120)), "units"))

        self._content(inner)

    def _content(self, p):
        PAD = dict(padx=24, pady=0)

        # saudação
        g = frame(p, bg=C["bg"])
        g.pack(fill="x", **PAD, pady=(20, 0))
        label(g, "Bom dia, Admin 👋", fg=C["text"], bg=C["bg"],
              size=14, bold=True).pack(anchor="w")
        label(g, "Resumo de hoje — " + datetime.date.today().strftime("%d/%m/%Y"),
              fg=C["text3"], bg=C["bg"], size=9).pack(anchor="w", pady=(2, 0))

        # stat cards
        cards = frame(p, bg=C["bg"])
        cards.pack(fill="x", **PAD, pady=(18, 0))
        for i, (title, value, sub, color, icon) in enumerate(STATS):
            c = _StatCard(cards, title, value, sub, color, icon)
            c.grid(row=0, column=i,
                   padx=(0, 12) if i < len(STATS)-1 else (0, 0),
                   sticky="nsew")
            cards.columnconfigure(i, weight=1)

        # tabelas
        mid = frame(p, bg=C["bg"])
        mid.pack(fill="x", **PAD, pady=(22, 0))
        mid.columnconfigure(0, weight=3)
        mid.columnconfigure(1, weight=2)

        left = frame(mid, bg=C["bg"])
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        section_header(left, "Reuniões Recentes").pack(fill="x", pady=(0, 10))
        DataTable(left, MEETINGS_COLS, MEETINGS_ROWS).pack(fill="x")

        right = frame(mid, bg=C["bg"])
        right.grid(row=0, column=1, sticky="nsew")
        section_header(right, "Documentos Recentes").pack(fill="x", pady=(0, 10))
        DataTable(right, DOCS_COLS, DOCS_ROWS).pack(fill="x")

        # notificações
        notif = frame(p, bg=C["bg"])
        notif.pack(fill="x", **PAD, pady=(22, 28))
        NotificationBar(notif, NOTIFICATIONS, bg=C["bg"]).pack(fill="x")