"""
Fluxo OAuth pra gerar refresh token do Google Ads API.

Roda 1x no setup. Abre o navegador, você autoriza com a conta Google que tem
acesso ao MCC, e o script imprime o refresh token. Cole no .env como
GOOGLE_ADS_REFRESH_TOKEN.

Pré-requisitos:
- Cliente OAuth criado no Google Cloud Console (tipo "Desktop app")
- client_secret*.json baixado e salvo em api/google-ads/credentials/
- Developer token Google Ads aprovado (ou modo teste)

Uso:
    python api/google-ads/01_auth_setup.py [--client-secret PATH]
"""

import sys
from pathlib import Path

import click
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/adwords"]
CREDENTIALS_DIR = Path(__file__).resolve().parent / "credentials"


def find_client_secret() -> Path:
    """Procura client_secret*.json na pasta credentials/."""
    if not CREDENTIALS_DIR.exists():
        sys.exit(
            f"Pasta {CREDENTIALS_DIR} não existe.\n"
            f"Crie e coloque o client_secret*.json baixado do Google Cloud Console."
        )
    matches = list(CREDENTIALS_DIR.glob("client_secret*.json"))
    if not matches:
        sys.exit(
            f"Nenhum client_secret*.json encontrado em {CREDENTIALS_DIR}.\n"
            f"Baixe do Google Cloud Console > Credentials > OAuth 2.0 Client IDs."
        )
    if len(matches) > 1:
        print(f"Aviso: {len(matches)} arquivos client_secret encontrados. Usando: {matches[0].name}")
    return matches[0]


@click.command()
@click.option(
    "--client-secret",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="Caminho do client_secret.json. Se omitido, procura em api/google-ads/credentials/",
)
def main(client_secret: Path):
    """Roda o fluxo OAuth e imprime o refresh token."""
    secret_path = client_secret or find_client_secret()

    print(f"Usando: {secret_path}")
    print("Abrindo navegador pra autorização...\n")

    flow = InstalledAppFlow.from_client_secrets_file(str(secret_path), SCOPES)
    credentials = flow.run_local_server(port=0, prompt="consent")

    print("\nAutorização concluída.")
    print("=" * 70)
    print(f"Refresh token:\n\n{credentials.refresh_token}\n")
    print("=" * 70)
    print("\nCole no .env:\n")
    print(f"GOOGLE_ADS_REFRESH_TOKEN={credentials.refresh_token}\n")
    print("Pegue também:")
    print(f"  GOOGLE_ADS_CLIENT_ID={credentials.client_id}")
    print(f"  GOOGLE_ADS_CLIENT_SECRET={credentials.client_secret}")
    print(
        "\nGuarde o client_secret*.json em segurança. Ele NÃO é versionado pelo git "
        "(já está no .gitignore)."
    )


if __name__ == "__main__":
    main()
