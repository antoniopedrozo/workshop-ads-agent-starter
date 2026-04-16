"""
Helper compartilhado: instancia o GoogleAdsClient a partir do .env.

Usado por todos os outros scripts em api/google-ads/.
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# Carrega .env da raiz do projeto
ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")


def get_client() -> GoogleAdsClient:
    """Retorna GoogleAdsClient configurado pelas variáveis do .env."""

    required = [
        "GOOGLE_ADS_DEVELOPER_TOKEN",
        "GOOGLE_ADS_CLIENT_ID",
        "GOOGLE_ADS_CLIENT_SECRET",
        "GOOGLE_ADS_REFRESH_TOKEN",
        "GOOGLE_ADS_LOGIN_CUSTOMER_ID",
    ]
    missing = [k for k in required if not os.getenv(k)]
    if missing:
        sys.exit(
            f"Variáveis ausentes no .env: {', '.join(missing)}.\n"
            f"Veja SETUP.md ou COWORK_SETUP.md."
        )

    config = {
        "developer_token": os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN"),
        "client_id": os.getenv("GOOGLE_ADS_CLIENT_ID"),
        "client_secret": os.getenv("GOOGLE_ADS_CLIENT_SECRET"),
        "refresh_token": os.getenv("GOOGLE_ADS_REFRESH_TOKEN"),
        "login_customer_id": os.getenv("GOOGLE_ADS_LOGIN_CUSTOMER_ID"),
        "use_proto_plus": True,
    }

    return GoogleAdsClient.load_from_dict(config)


def get_customer_id() -> str:
    """Customer ID alvo (a conta que vai gastar). Sem hífen."""
    cid = os.getenv("GOOGLE_ADS_CUSTOMER_ID") or os.getenv("GOOGLE_ADS_LOGIN_CUSTOMER_ID")
    if not cid:
        sys.exit("GOOGLE_ADS_CUSTOMER_ID ausente no .env.")
    return cid.replace("-", "").strip()


def brl_to_micros(brl: float) -> int:
    """Converte BRL em micros (unidade da API Google Ads): 1 BRL = 1.000.000 micros."""
    return int(round(brl * 1_000_000))


def handle_google_ads_error(ex: GoogleAdsException) -> None:
    """Imprime erro do Google Ads de forma legível e sai com código 1."""
    print(f"\nErro Google Ads (request_id={ex.request_id}):")
    for error in ex.failure.errors:
        print(f"  - {error.error_code}: {error.message}")
        if error.location:
            for fpe in error.location.field_path_elements:
                print(f"      campo: {fpe.field_name}")
    sys.exit(1)
