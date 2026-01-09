# Unificador de PDFs (Google Drive)

App simples para unificar PDFs via links públicos do Google Drive.

## Funcionalidades

-   Baixa PDFs de links públicos.
-   Une múltiplos arquivos em um só.
-   Interface moderna e em Português.
-   Sem necessidade de login ou configurações complexas.

## Instalação

1.  Certifique-se de ter Python instalado.
2.  Instale as dependências:
    ```bash
    python -m pip install -r requirements.txt
    ```

## Uso

Para rodar o aplicativo, use o comando abaixo no seu terminal (PowerShell):

```bash
python -m streamlit run app.py
```

### Como usar:

1.  **Cole os Links**: Insira os links dos arquivos PDF (públicos) na área de texto.
2.  **Unificar**: Clique no botão "Unificar Arquivos".
3.  **Baixar**: Faça o download do arquivo gerado.
4.  **Salvar**: Use o botão de atalho para abrir sua pasta do Drive e salvar o arquivo manualmente.

## Observações

-   Os arquivos **precisam** estar configurados como "Qualquer pessoa com o link" no Google Drive.
