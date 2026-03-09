# Autenticação OAuth2 Google
"""
auth/google_auth.py

Gerenciador de autenticação Google OAuth2 para app desktop.
Fluxo: loopback (localhost) com PKCE — padrão para App para Computador.

Dependências:
    pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

Arquivos necessários:
    credentials.json  — baixado do Google Cloud Console
    token.json        — gerado automaticamente após o primeiro login (não versionar)
"""

import logging
from pathlib import Path
from typing import Optional

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────
#  ESCOPOS DE ACESSO
# ─────────────────────────────────────────
# Adicione ou remova escopos conforme necessário.
# Toda alteração nos escopos exige novo login do usuário.
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",   # Ler e escrever em Sheets
    "https://www.googleapis.com/auth/drive",           # Ler, criar e enviar arquivos no Drive
    "https://www.googleapis.com/auth/userinfo.email",  # E-mail do usuário logado
    "https://www.googleapis.com/auth/userinfo.profile",# Nome e foto do usuário
    "openid",                                          # Identidade OpenID
]

# ─────────────────────────────────────────
#  CAMINHOS
# ─────────────────────────────────────────
BASE_DIR        = Path(__file__).resolve().parent.parent
CREDENTIALS_PATH = BASE_DIR / "credentials.json"
TOKEN_PATH       = BASE_DIR / "token.json"


class GoogleAuthManager:
    """
    Gerencia o ciclo de vida das credenciais OAuth2 do Google.

    Uso básico:
        auth = GoogleAuthManager()
        if auth.login():
            sheets = auth.get_sheets_service()
            drive  = auth.get_drive_service()
            user   = auth.get_user_info()
    """

    def __init__(
        self,
        credentials_path: Path = CREDENTIALS_PATH,
        token_path: Path = TOKEN_PATH,
        scopes: list[str] = SCOPES,
    ):
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.scopes = scopes
        self._creds: Optional[Credentials] = None

    # ── público ────────────────────────────────────────────

    def login(self) -> bool:
        """
        Realiza o login OAuth2.
        1. Tenta carregar token salvo em disco.
        2. Se expirado, renova silenciosamente via refresh token.
        3. Se não houver token, abre o browser para o fluxo de autorização.

        Retorna True se autenticado com sucesso, False caso contrário.
        """
        try:
            self._creds = self._load_token()

            if self._creds and self._creds.expired and self._creds.refresh_token:
                self._creds.refresh(Request())
                self._save_token()
                logger.info("Token expirado — renovando silenciosamente...")
                logger.info("Token renovado com sucesso.")
                return self._creds.valid

            # Abre o browser e persiste as credenciais atuais em token.json
            if not self._creds or not self._creds.valid:
                logger.info("Nenhum token válido — iniciando fluxo OAuth2...")
                self._creds = self._run_oauth_flow()
                self._save_token()
                logger.info("Login realizado com sucesso.")

            return self._creds is not None and self._creds.valid

        except FileNotFoundError:
            logger.error(
                "credentials.json não encontrado em: %s\n"
                "Baixe o arquivo no Google Cloud Console e coloque na raiz do projeto.",
                self.credentials_path,
            )
            return False
        except Exception as e:
            logger.error("Erro durante autenticação: %s", e)
            return False

    def logout(self):
        """Remove o token salvo e limpa as credenciais em memória."""
        self._creds = None
        if self.token_path.exists():
            self.token_path.unlink()
            logger.info("Token removido. Usuário deslogado.")

    @property
    def is_authenticated(self) -> bool:
        """True se há credenciais válidas em memória."""
        return self._creds is not None and self._creds.valid

    def get_user_info(self) -> dict:
        """
        Retorna informações básicas do usuário autenticado.
        Ex.: {"name": "João Silva", "email": "joao@gmail.com", "picture": "https://..."}
        """
        self._require_auth()
        try:
            service = build("oauth2", "v2", credentials=self._creds)
            info = service.userinfo().get().execute()
            return {
                "name":    info.get("name", ""),
                "email":   info.get("email", ""),
                "picture": info.get("picture", ""),
            }
        except Exception as e:
            logger.error("Erro ao obter informações do usuário: %s", e)
            return {}

    def get_sheets_service(self):
        """Retorna um cliente autenticado para a Google Sheets API v4."""
        self._require_auth()
        return build("sheets", "v4", credentials=self._creds)

    def get_drive_service(self):
        """Retorna um cliente autenticado para a Google Drive API v3."""
        self._require_auth()
        return build("drive", "v3", credentials=self._creds)

    # ── privado ────────────────────────────────────────────

    def _load_token(self) -> Optional[Credentials]:
        """Carrega credenciais salvas do token.json, se existir."""
        if self.token_path.exists():
            creds = Credentials.from_authorized_user_file(
                str(self.token_path), self.scopes
            )
            logger.info("Token carregado de: %s", self.token_path)
            return creds
        return None

    def _save_token(self):
        """Persiste as credenciais atuais em token.json."""
        if self._creds:
            with open(self.token_path, "w") as f:
                f.write(self._creds.to_json())
            logger.info("Token salvo em: %s", self.token_path)

    def _run_oauth_flow(self) -> Credentials:
        """
        Executa o fluxo OAuth2 para App para Computador.
        Abre o browser do usuário e sobe um servidor loopback
        temporário em localhost para capturar o código de autorização.
        """
        flow = InstalledAppFlow.from_client_secrets_file(
            str(self.credentials_path),
            scopes=self.scopes,
        )

        # run_local_server: abre o browser e captura o callback em localhost
        creds = flow.run_local_server(
            port=0,              # porta aleatória disponível
            prompt="consent",    # força exibir a tela de consentimento
            access_type="offline",  # garante refresh_token
        )
        return creds

    def _require_auth(self):
        """Lança exceção se não houver credenciais válidas."""
        if not self.is_authenticated:
            raise RuntimeError(
                "Usuário não autenticado. Chame login() antes de usar os serviços."
            )