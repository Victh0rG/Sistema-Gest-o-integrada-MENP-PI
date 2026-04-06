# Tabela reutilizavel
"""
ui/components/data_table.py
Tabela genérica e reutilizável para exibição de dados tabulares.
"""
import tkinter as tk
from ui.theme import C, frame, label


class DataTable(tk.Frame):
    """
    Tabela reutilizável com cabeçalho, linhas e hover.

    Parâmetros
    ----------
    columns : list[dict]
        Ex.: [{"header": "Nome", "width": 260, "key": "nome"}, ...]
    rows : list[dict]
        Ex.: [{"nome": "João", "status": ("Ativo", C["success"])}, ...]
        O valor pode ser uma string simples ou uma tupla (texto, cor).
    on_row_click : callable | None
        Chamado com o dict da linha ao clicar.
    """

    def __init__(self, parent, columns: list[dict], rows: list[dict],
                 on_row_click=None, bg=None):
        bg = bg or C["surface"]
        super().__init__(parent, bg=bg,
                         highlightbackground=C["border"], highlightthickness=1)
        self.columns = columns
        self.on_row_click = on_row_click
        self._build_header()
        self.set_rows(rows)

    # ── public ─────────────────────────────
    def set_rows(self, rows: list[dict]):
        """Substitui todas as linhas da tabela."""
        for w in self.winfo_children():
            if getattr(w, "_is_row", False):
                w.destroy()
        for row in rows:
            self._build_row(row)

    # ── private ────────────────────────────
    def _build_header(self):
        h = frame(self, bg=C["surface2"])
        h.pack(fill="x")
        for col in self.columns:
            tk.Label(
                h, text=col["header"],
                fg=C["text3"], bg=C["surface2"],
                font=("Segoe UI", 8),
                width=col.get("width_chars", 0),
                anchor="w"
            ).pack(side="left", padx=14, pady=8)

    def _build_row(self, row: dict):
        r = frame(self, bg=C["surface"])
        r._is_row = True
        r.pack(fill="x")

        for col in self.columns:
            key   = col["key"]
            value = row.get(key, "")

            # valor pode ser (texto, cor) ou string simples
            if isinstance(value, tuple):
                text, color = value
            else:
                text, color = str(value), C["text"]

            cell_type = col.get("type", "text")

            if cell_type == "badge":
                badge_bg = col.get("badge_bg", C["surface3"])
                tk.Label(r, text=f"  {text}  ", fg=color,
                         bg=badge_bg, font=("Segoe UI", 8, "bold"),
                         relief="flat", padx=4, pady=2
                         ).pack(side="right" if col.get("align") == "right" else "left",
                                padx=14, pady=8)
            else:
                tk.Label(r, text=text, fg=color, bg=C["surface"],
                         font=("Segoe UI", 9),
                         anchor="w"
                         ).pack(side="left", padx=14, pady=10)

        # hover
        r.bind("<Enter>", lambda e, w=r: w.config(bg=C["surface2"]))
        r.bind("<Leave>", lambda e, w=r: w.config(bg=C["surface"]))
        if self.on_row_click:
            r.bind("<Button-1>", lambda e, d=row: self.on_row_click(d))

        # divider
        div = tk.Frame(self, bg=C["border"], height=1)
        div._is_row = True
        div.pack(fill="x")