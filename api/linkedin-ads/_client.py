"""
Helper compartilhado: monta config de requisições à LinkedIn REST API.
"""

import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")

API_BASE = "https://api.linkedin.com/rest"
LINKEDIN_VERSION = "202404"


def get_token() -> str:
    token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    if not token:
        sys.exit("LINKEDIN_ACCESS_TOKEN ausente no .env.")
    return token


def get_account_id() -> str:
    aid = (os.getenv("LINKEDIN_AD_ACCOUNT_ID") or "").strip()
    if not aid:
        sys.exit("LINKEDIN_AD_ACCOUNT_ID ausente no .env.")
    return aid


def get_account_urn() -> str:
    return f"urn:li:sponsoredAccount:{get_account_id()}"


def headers() -> dict:
    return {
        "Authorization": f"Bearer {get_token()}",
        "LinkedIn-Version": LINKEDIN_VERSION,
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json",
    }


def post(path: str, payload: dict) -> requests.Response:
    """POST helper. Retorna response e checa erro."""
    url = f"{API_BASE}{path}"
    r = requests.post(url, headers=headers(), json=payload)
    if r.status_code >= 400:
        sys.exit(f"\nErro {r.status_code}: {r.text}")
    return r


def get(path: str, params: dict = None) -> dict:
    """GET helper. Retorna JSON."""
    url = f"{API_BASE}{path}"
    r = requests.get(url, headers=headers(), params=params or {})
    if r.status_code >= 400:
        sys.exit(f"\nErro {r.status_code}: {r.text}")
    return r.json()


def brl_to_cents(brl: float) -> int:
    return int(round(brl * 100))
