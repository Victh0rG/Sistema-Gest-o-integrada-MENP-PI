# Upload e vinculação de arquivos

"""
services/drive_service.py

Camada de serviço para a Google Drive API v3.
Encapsula todas as operações de pasta e arquivo utilizadas pelo MENP-PI.

Uso:
    from auth import GoogleAuthManager
    from services import DriveService

    auth  = GoogleAuthManager()
    auth.login()

    drive = DriveService(auth)

    # Criar estrutura de pastas
    root_id  = drive.create_folder("MENP-PI")
    year_id  = drive.create_folder("2025",        parent_id=root_id)
    month_id = drive.create_folder("06 - Junho",  parent_id=year_id)
    meet_id  = drive.create_folder("Reuniao Ordinaria 03-06", parent_id=month_id)

    # Enviar arquivo
    file_id = drive.upload_file("ata.pdf", meet_id)

    # Listar conteúdo
    items = drive.list_folder(meet_id)
"""

from infraestructure import google_auth
from infraestructure import Authenticate
from googleapiclient.errors import HttpError
from typing import Optional
import logging

FOLDER_MIME = "application/vnd.google-apps.folder"

logger = logging.getLogger()

class DriveService:
    def __init__(self):
        auth = google_auth.GoogleAuthManager()

        if auth.login():
            self._drive = auth.get_drive_service()

    def create_folder(self, name: str,
                      parent_id: Optional[str] = None) -> Optional[str]:
        """
        Cria uma pasta no Drive.

        Parâmetros
        ----------
        name      : nome da pasta
        parent_id : ID da pasta pai (None = raiz do Drive)

        Retorna o ID da pasta criada, ou None em caso de erro.

        Exemplo
        -------
        root_id = drive.create_folder("MENP-PI")
        ano_id  = drive.create_folder("2025", parent_id=root_id)
        """
        metadata = {
            "name":     name,
            "mimeType": FOLDER_MIME,
        }
        if parent_id:
            metadata["parents"] = [parent_id]

        try:
            folder = (
                self._drive.files()
                .create(body=metadata, fields="id, name")
                .execute()
            )
            logger.info("Pasta criada: '%s' (id=%s)", folder["name"], folder["id"])
            return folder["id"]

        except HttpError as e:
            logger.error("Erro ao criar pasta '%s': %s", name, e)
            return None


    def get_or_folder(self, name: str,
                              parent_id: Optional[str] = None) -> Optional[str]:
        """
        Busca uma pasta pelo nome dentro de um diretório pai.
        Se não existir, cria. Evita duplicatas ao rodar o app múltiplas vezes.

        Exemplo
        -------
        root_id = drive.get_or_create_folder("MENP-PI")
        """
        existing_id = self.find_folder(name, parent_id)
        if existing_id:
            logger.info("Pasta já existe: '%s' (id=%s)", name, existing_id)
        return existing_id
        # return self.create_folder(name, parent_id)

    def find_folder(self, name: str,
                    parent_id: Optional[str] = None) -> Optional[str]:
        """
        Procura uma pasta pelo nome exato dentro de um diretório pai.
        Retorna o ID da primeira ocorrência ou None se não encontrada.
        """
        # monta a query de busca
        query = (
            f"name = '{name}' "
            f"and mimeType = '{FOLDER_MIME}' "
            f"and trashed = false"
        )
        if parent_id:
            query += f" and '{parent_id}' in parents"

        try:
            result = (
                self._drive.files()
                .list(q=query, fields="files(id, name)", pageSize=1)
                .execute()
            )
            files = result.get("files", [])
            if files:
                return files[0]["id"]
            return None

        except HttpError as e:
            logger.error("Erro ao buscar pasta '%s': %s", name, e)
            return None

    def create_folder_path(self, path: str,
                           root_id: Optional[str] = None) -> Optional[str]:
        """
        Cria uma hierarquia de pastas a partir de um caminho estilo Unix.
        Usa get_or_create em cada nível, evitando duplicatas.

        Parâmetros
        ----------
        path    : caminho com '/' como separador. Ex.: "2025/06 - Junho/Reuniao Ordinaria"
        root_id : ID da pasta raiz onde começar (None = raiz do Drive)

        Retorna o ID da pasta folha (última do caminho).

        Exemplo
        -------
        pasta_id = drive.create_folder_path("2025/06 - Junho/Reuniao 03-06")
        """
        parts = [p for p in path.split("/") if p]
        current_id = root_id

        for part in parts:
            current_id = self.get_or_create_folder(part, current_id)
            if current_id is None:
                logger.error("Falha ao criar nível '%s' do caminho '%s'", part, path)
                return None

        return current_id


    def delete(self, file_or_folder_id: str) -> bool:
        """
        Move um arquivo ou pasta para a lixeira do Drive.
        Retorna True se bem-sucedido.
        """
        try:
            self._drive.files().delete(fileId=file_or_folder_id).execute()
            logger.info("Item (id=%s) enviado para lixeira.", file_or_folder_id)
            return True
        except HttpError as e:
            logger.error("Erro ao deletar (id=%s): %s", file_or_folder_id, e)
            return False