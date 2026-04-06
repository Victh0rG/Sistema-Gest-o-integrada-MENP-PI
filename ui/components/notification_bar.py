# Alertas e notificações
"""
ui/components/notification_bar.py
Painel de alertas e notificações reutilizável.
"""
import tkinter as tk
from ui.theme import C, frame, label, section_header


class NotificationBar(tk.Frame):
    """
    Painel vertical de notificações.
    Recebe uma lista de dicts:
        [{"icon": "⚠", "title": "...", "body": "...", "color": C["warning"]}, ...]
    """

    def __init__(self, parent, notifications: list[dict] | None = None, bg=None):
        bg = bg or C["bg"]
        super().__init__(parent, bg=bg)
        self.bg = bg
        self.notifications = notifications or []
        self._build()

    def _build(self):
        # cabeçalho
        sh = section_header(self, "⚠  Pendências e Alertas",
                            link_text="Ver todas →", bg=self.bg)
        sh.pack(fill="x", pady=(0, 10))

        # container das notificações
        self.container = tk.Frame(
            self, bg=C["surface"],
            highlightbackground=C["border"], highlightthickness=1
        )
        self.container.pack(fill="x")

        for n in self.notifications:
            self._row(n)

        if not self.notifications:
            label(self.container, "Nenhuma pendência no momento 🎉",
                  fg=C["text3"], bg=C["surface"], size=9
                  ).pack(pady=20)

    def _row(self, n: dict):
        r = frame(self.container, bg=C["surface"])
        r.pack(fill="x", padx=12, pady=8)

        tk.Label(r, text=n.get("icon", "•"),
                 bg=C["surface"], font=("Segoe UI", 13)
                 ).pack(side="left", padx=(0, 10))

        body_f = frame(r, bg=C["surface"])
        body_f.pack(side="left", fill="x", expand=True)

        label(body_f, n.get("title", ""), fg=n.get("color", C["text2"]),
              bg=C["surface"], size=9, bold=True).pack(anchor="w")
        label(body_f, n.get("body", ""), fg=C["text2"],
              bg=C["surface"], size=8).pack(anchor="w")

        tk.Frame(self.container, bg=C["border"], height=1).pack(fill="x", padx=12)

    def update_notifications(self, notifications: list[dict]):
        """Atualiza a lista de notificações dinamicamente."""
        self.notifications = notifications
        for w in self.container.winfo_children():
            w.destroy()
        for n in self.notifications:
            self._row(n)
        if not self.notifications:
            label(self.container, "Nenhuma pendência no momento 🎉",
                  fg=C["text3"], bg=C["surface"], size=9).pack(pady=20)