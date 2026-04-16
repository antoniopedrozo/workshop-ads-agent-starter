"""
Helper compartilhado: inicializa o SDK do Meta Marketing API a partir do .env.
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from facebook_business.api import FacebookAdsApi

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")


def init_api() -> FacebookAdsApi:
    """Inicializa FacebookAdsApi singleton e retorna instância."""
    required = ["META_APP_ID", "META_APP_SECRET", "META_ACCESS_TOKEN", "META_AD_ACCOUNT_ID"]
    missing = [k for k in required if not os.getenv(k)]
    if missing:
        sys.exit(
            f"Variáveis ausentes no .env: {', '.join(missing)}.\n"
            f"Veja SETUP.md ou COWORK_SETUP.md."
        )

    api = FacebookAdsApi.init(
        app_id=os.getenv("META_APP_ID"),
        app_secret=os.getenv("META_APP_SECRET"),
        access_token=os.getenv("META_ACCESS_TOKEN"),
    )
    return api


def get_ad_account_id() -> str:
    """Retorna ad account ID com prefixo act_."""
    aid = os.getenv("META_AD_ACCOUNT_ID", "").strip()
    if not aid:
        sys.exit("META_AD_ACCOUNT_ID ausente.")
    if not aid.startswith("act_"):
        aid = f"act_{aid}"
    return aid


def brl_to_cents(brl: float) -> int:
    """Converte BRL em centavos (unidade da API Meta): 1 BRL = 100 cents."""
    return int(round(brl * 100))
