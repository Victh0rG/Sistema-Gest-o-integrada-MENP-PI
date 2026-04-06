"""
ui/components/sidebar.py
Menu lateral de navegação do MENP-PI.
"""
import tkinter as tk
from ui.theme import C, frame, label

NAV_ITEMS = [
    ("🏠", "Dashboard"),
    ("📋", "Atendimentos"),
    ("📅", "Calendário"),
    ("📄", "Documentos"),
    ("🤖", "IA / Upload"),
    ("🔍", "Busca"),
    ("⚙",  "Configurações"),
]


class Sidebar(tk.Frame):
    """
    Menu lateral fixo com itens de navegação clicáveis.
    Chama on_nav(name) ao clicar em um item.
    """

    def __init__(self, parent, on_nav: callable,
                 on_logout: callable = None,
                 user_info: dict = None):
        super().__init__(parent, bg=C["sidebar"], width=210)
        self.pack_propagate(False)
        self.on_nav = on_nav
        self.on_logout = on_logout
        self.user_info = user_info or {}
        self.active = "Dashboard"
        self.btns: dict[str, tuple] = {}
        self._build()

    # ── build ──────────────────────────────
    def _build(self):
        self._logo()
        divider = tk.Frame(self, bg=C["border"], height=1)
        divider.pack(fill="x", padx=16, pady=10)
        label(self, "NAVEGAÇÃO", fg=C["text3"], bg=C["sidebar"],
              size=7).pack(anchor="w", padx=20, pady=(0, 6))
        for icon, name in NAV_ITEMS:
            self._nav_item(icon, name)
        self._user_info()

    def _logo(self):
        f = frame(self, bg=C["sidebar"])
        f.pack(fill="x", padx=20, pady=(24, 8))
        label(f, "MENP-PI", fg=C["accent"], bg=C["sidebar"],
              size=14, bold=True).pack(anchor="w")
        label(f, "Sistema de Gestão", fg=C["text3"], bg=C["sidebar"],
              size=8).pack(anchor="w")

    def _nav_item(self, icon: str, name: str):
        is_active = (name == self.active)
        bg     = C["surface3"] if is_active else C["sidebar"]
        fg     = C["text"]     if is_active else C["text2"]
        bar_bg = C["accent"]   if is_active else C["sidebar"]

        outer = frame(self, bg=C["sidebar"])
        outer.pack(fill="x", padx=10, pady=1)

        inner = tk.Frame(outer, bg=bg, cursor="hand2")
        inner.pack(fill="x")

        bar = tk.Frame(inner, bg=bar_bg, width=3)
        bar.pack(side="left", fill="y")

        lbl = label(inner, f"{icon}  {name}", fg=fg, bg=bg, size=9)
        lbl.pack(side="left", padx=10, pady=9)

        # bind clique em todos os sub-widgets
        for w in (outer, inner, bar, lbl):
            w.bind("<Button-1>", lambda e, n=name: self._on_click(n))

        self.btns[name] = (outer, inner, bar, lbl)

    def _user_info(self):
        tk.Frame(self, bg=C["border"], height=1).pack(
            fill="x", padx=16, pady=(20, 6), side="bottom")

        # botão sair
        if self.on_logout:
            logout_btn = tk.Label(
                self, text="  ↩  Sair", fg=C["text3"], bg=C["sidebar"],
                font=("Segoe UI", 8), cursor="hand2",
            )
            logout_btn.pack(side="bottom", anchor="w", padx=20, pady=(0, 6))
            logout_btn.bind("<Button-1>", lambda e: self.on_logout())
            logout_btn.bind("<Enter>", lambda e: logout_btn.config(fg=C["danger"]))
            logout_btn.bind("<Leave>", lambda e: logout_btn.config(fg=C["text3"]))

        # info do usuário
        f = frame(self, bg=C["sidebar"])
        f.pack(fill="x", padx=14, pady=(0, 6), side="bottom")

        name  = self.user_info.get("name",  "Usuário")
        email = self.user_info.get("email", "")
        # iniciais para o avatar
        initials = "".join(p[0].upper() for p in name.split()[:2]) or "U"

        av = tk.Canvas(f, width=32, height=32, bg=C["sidebar"],
                       highlightthickness=0)
        av.pack(side="left")
        av.create_oval(1, 1, 31, 31, fill=C["surface3"], outline=C["border"])
        av.create_text(16, 16, text=initials, fill=C["accent"],
                       font=("Segoe UI", 8, "bold"))

        info = frame(f, bg=C["sidebar"])
        info.pack(side="left", padx=8)
        label(info, name,  fg=C["text"],  bg=C["sidebar"], size=9, bold=True).pack(anchor="w")
        label(info, email, fg=C["text3"], bg=C["sidebar"], size=7).pack(anchor="w")

    # ── public ─────────────────────────────
    def set_active(self, name: str):
        """Atualiza o item ativo visualmente."""
        self.active = name
        for n, (outer, inner, bar, lbl) in self.btns.items():
            is_active = (n == name)
            bg     = C["surface3"] if is_active else C["sidebar"]
            fg     = C["text"]     if is_active else C["text2"]
            bar_bg = C["accent"]   if is_active else C["sidebar"]
            inner.config(bg=bg)
            bar.config(bg=bar_bg)
            lbl.config(bg=bg, fg=fg)

    # ── private ────────────────────────────
    def _on_click(self, name: str):
        self.set_active(name)
        self.on_nav(name)