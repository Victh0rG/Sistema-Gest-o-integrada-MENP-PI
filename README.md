# MENP-PI — Sistema de Gestão Integrada

Aplicação desktop em Python para gestão integrada de atendimentos, documentos, reuniões e arquivos da organização MENP-PI, com dados persistidos no Google Sheets e arquivos armazenados no Google Drive.

---

## 📋 Funcionalidades

- **Formulário de Atendimentos** — Cadastro de atendimentos com validação e gravação direta na planilha Google Sheets.
- **IA para Leitura de Documentos** — Upload de PDFs com extração de texto e preenchimento automático via GPT-4o, com tela de revisão antes de gravar.
- **Gerenciador de Arquivos** — Upload e vinculação de arquivos ao Google Drive organizados por tipo/data.
- **Calendário de Reuniões** — Visualização mensal/semanal de reuniões com verificação automática de arquivos vinculados e notificações de divergências.
- **Busca e Consulta** — Busca global com filtros por data, tipo, responsável e status, com exportação para `.xlsx` ou `.csv`.

---

## 🛠️ Stack de Tecnologias

| Categoria | Tecnologia |
|---|---|
| Linguagem | Python 3.11+ |
| Interface gráfica | CustomTkinter |
| Calendário visual | tkcalendar |
| Google Sheets | gspread + google-auth |
| Google Drive | google-api-python-client |
| Leitura de PDF | pdfplumber |
| IA / LLM | OpenAI GPT-4o |
| Transcrição de áudio (futuro) | OpenAI Whisper API |
| Tabelas na GUI | pandastable / ttk.Treeview |
| Manipulação de dados | pandas |
| Notificações | plyer |
| Empacotamento | PyInstaller |

---

## 🚀 Instalação

### Pré-requisitos

- Python 3.11+
- Conta Google com acesso ao Google Cloud Console
- Chave de API da OpenAI

### 1. Clone o repositório

```bash
git clone https://github.com/sua-org/menp-pi.git
cd menp-pi
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure as credenciais Google

1. Acesse o [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um projeto e habilite as APIs **Google Sheets API** e **Google Drive API**
3. Gere uma credencial do tipo **Service Account** e baixe o arquivo `credentials.json`
4. Compartilhe sua planilha Google Sheets com o e-mail da Service Account

### 4. Configure as variáveis de ambiente

Copie o arquivo de exemplo e preencha com suas credenciais:

```bash
cp .env.example .env
```

Edite o `.env`:

```env
GOOGLE_CREDENTIALS_PATH=./credentials.json
GOOGLE_SHEET_ID=<id_da_planilha>
OPENAI_API_KEY=<sua_chave_openai>
```

> ⚠️ **Nunca commite o arquivo `.env` ou `credentials.json` no repositório.**

### 5. Execute a aplicação

```bash
python main.py
```

---

## 📁 Estrutura do Projeto

```
menp_pi/
├── main.py                   # Entry point
├── requirements.txt
├── .env                      # Variáveis de ambiente (não versionar)
├── .env.example
├── config/
│   ├── settings.py           # Constantes e IDs da planilha
│   └── column_map.py         # Mapeamento campo → coluna da planilha
├── domain/
│   ├── atendimento.py        # Dataclass Atendimento
│   ├── reuniao.py            # Dataclass Reuniao
│   └── documento.py          # Dataclass Documento
├── infrastructure/
│   ├── google_auth.py        # Autenticação OAuth2 Google
│   ├── sheets_repository.py  # CRUD no Google Sheets
│   ├── drive_repository.py   # Upload/download Google Drive
│   └── ai_client.py          # Chamadas à API OpenAI
├── services/
│   ├── atendimento_service.py
│   ├── reuniao_service.py
│   ├── documento_service.py
│   ├── pdf_service.py
│   ├── ai_service.py
│   └── search_service.py
├── ui/
│   ├── app.py                # Janela principal
│   ├── components/
│   │   ├── sidebar.py
│   │   ├── notification_bar.py
│   │   └── data_table.py
│   └── views/
│       ├── atendimento_view.py
│       ├── ia_upload_view.py
│       ├── calendario_view.py
│       ├── arquivos_view.py
│       └── busca_view.py
├── assets/
│   └── logo.png
└── tests/
    ├── test_atendimento_service.py
    ├── test_sheets_repository.py
    └── test_pdf_service.py
```

---

## 🏗️ Arquitetura

O projeto segue os princípios de **Clean Architecture** com separação clara de camadas:

- **Presentation (UI)** — Telas e widgets em CustomTkinter, sem lógica de negócio.
- **Application (Services)** — Orquestra os casos de uso (gravar atendimento, processar PDF, verificar arquivos).
- **Infrastructure (API)** — Comunicação com Google Sheets, Google Drive e OpenAI.
- **Domain (Models)** — Classes de dados puras (`dataclasses`): `Atendimento`, `Reuniao`, `Documento`.
- **Config** — Credenciais, constantes e mapeamento de colunas.

---

## 🧪 Testes

```bash
python -m pytest tests/
```

---

## 📄 Licença

Uso interno — MENP-PI. Todos os direitos reservados.
