"""
ui/app.py
Janela principal do MENP-PI.
Gerencia autenticação OAuth2, layout raiz (sidebar + conteúdo) e navegação entre views.
"""
import tkinter as tk
from tkinter import ttk
import logging

from ui.theme import C, frame
from ui.components.sidebar import Sidebar
from ui.views.login_view import LoginView
from ui.views.dashboard_view import DashboardView
from ui.views.atendimento_view import AtendimentoView
from ui.views.ia_upload_view import IaUploadView
from ui.views.calendario_view import CalendarioView
from ui.views.arquivos_view import ArquivosView
from ui.views.busca_view import BuscaView
from auth.google_auth import GoogleAuthManager
from database.db import inicializar_banco
from services.reuniao_service import ReunioService

logger = logging.getLogger(__name__)

# Mapa: nome do item de navegação → classe da view
VIEW_MAP = {
    "Dashboard":    DashboardView,
    "Atendimentos": AtendimentoView,
    "IA / Upload":  IaUploadView,
    "Calendário":   CalendarioView,
    "Documentos":   ArquivosView,
    "Busca":        BuscaView,
}


class App(tk.Tk):
    """
    Janela raiz da aplicação MENP-PI.
    Fluxo de inicialização:
        1. Exibe LoginView
        2. Após login bem-sucedido, monta o layout principal e exibe o Dashboard
    """

    def __init__(self):
        super().__init__()
        self.title("MENP-PI — Sistema de Gestão Unificada")
        self.geometry("1280x760")
        self.minsize(1024, 640)
        self.configure(bg=C["bg"])
        self._center_window(1280, 760)
        self._configure_styles()

        # instância única do gerenciador de autenticação
        self.auth = GoogleAuthManager()
        inicializar_banco()
        self.reuniao_service = ReunioService()

        # estado
        self._views: dict[str, tk.Frame] = {}
        self._sidebar = None
        self._content = None
        self._user_info: dict = {}

        # inicia pelo login
        self._show_login()

    # ── setup ───────────────────────────────
    def _center_window(self, w: int, h: int):
        self.update_idletasks()
        x = (self.winfo_screenwidth()  - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Vertical.TScrollbar",
                        background=C["surface3"],
                        troughcolor=C["surface"],
                        bordercolor=C["surface"],
                        arrowcolor=C["text3"],
                        relief="flat")

    # ── autenticação ────────────────────────
    def _show_login(self):
        """Exibe a tela de login, destruindo qualquer conteúdo anterior."""
        for w in self.winfo_children():
            w.destroy()
        self._views.clear()
        self._sidebar = None
        self._content = None

        login = LoginView(self, auth=self.auth, on_success=self._on_login_success)
        login.pack(fill="both", expand=True)

    def _on_login_success(self, user_info: dict):
        """Chamado após login OAuth2 bem-sucedido."""
        self._user_info = user_info
        logger.info("Usuário autenticado: %s", user_info.get("email"))
        self._build_main_layout()
        self._navigate("Dashboard")

    def _logout(self):
        """Desloga o usuário e volta para a tela de login."""
        self.auth.logout()
        self._show_login()

    # ── layout principal ────────────────────
    def _build_main_layout(self):
        """Monta sidebar + área de conteúdo após autenticação."""
        for w in self.winfo_children():
            w.destroy()

        root = frame(self, bg=C["bg"])
        root.pack(fill="both", expand=True)

        # sidebar — passa callback de logout
        self._sidebar = Sidebar(root, self._navigate, on_logout=self._logout,
                                user_info=self._user_info)
        self._sidebar.pack(side="left", fill="y")

        # divisor vertical
        tk.Frame(root, bg=C["border"], width=1).pack(side="left", fill="y")

        # área de conteúdo
        self._content = frame(root, bg=C["bg"])
        self._content.pack(side="left", fill="both", expand=True)

    # ── navegação ───────────────────────────
    def _navigate(self, name: str):
        if self._content is None:
            return

        for child in self._content.winfo_children():
            child.pack_forget()

        if name not in self._views:
            view_class = VIEW_MAP.get(name)
            if view_class is None:
                return
            # passa auth para as views que precisam consumir APIs Google
            if name == "Calendário":
                self._views[name] = CalendarioView(self._content, reuniao_service=self.reuniao_service)
            else:
                self._views[name] = view_class(self._content)

        self._views[name].pack(fill="both", expand=True)

        if self._sidebar:
            self._sidebar.set_active(name)