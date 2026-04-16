"""
Lê insights (relatórios de performance) do Meta Marketing API.

Levels:
- account: agregado da conta
- campaign: por campanha
- adset: por ad set
- ad: por ad

Uso:
    python api/meta-ads/read_insights.py --level adset --days 30
    python api/meta-ads/read_insights.py --level ad --days 14 --output csv > insights.csv
"""

import csv
import sys
from datetime import datetime, timedelta

import click
from facebook_business.adobjects.adaccount import AdAccount

from _client import get_ad_account_id, init_api


FIELDS = [
    "campaign_name",
    "adset_name",
    "ad_name",
    "impressions",
    "reach",
    "frequency",
    "clicks",
    "ctr",
    "cpm",
    "cpp",
    "spend",
    "actions",
]


def cents_to_brl(value) -> float:
    """Meta retorna spend já em decimal BRL (não em cents). Mantido pra clareza."""
    try:
        return round(float(value), 2)
    except (TypeError, ValueError):
        return 0.0


def extract_actions(actions, action_type: str) -> int:
    """Soma actions de um tipo específico."""
    if not actions:
        return 0
    total = 0
    for a in actions:
        if a.get("action_type") == action_type:
            try:
                total += int(float(a.get("value", 0)))
            except ValueError:
                pass
    return total


@click.command()
@click.option(
    "--level", type=click.Choice(["account", "campaign", "adset", "ad"]), required=True
)
@click.option("--days", type=int, default=30)
@click.option("--output", type=click.Choice(["table", "csv"]), default="table")
@click.option(
    "--action-type",
    default="lead",
    help="Tipo de ação a extrair como coluna (lead, purchase, complete_registration, etc.)",
)
def main(level, days, output, action_type):
    """Lê insights e imprime."""
    init_api()
    account = AdAccount(get_ad_account_id())

    since = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    until = datetime.now().strftime("%Y-%m-%d")

    params = {
        "level": level,
        "time_range": {"since": since, "until": until},
        "limit": 500,
    }

    insights = account.get_insights(fields=FIELDS, params=params)

    rows = []
    for ins in insights:
        rows.append(
            {
                "campaign_name": ins.get("campaign_name", ""),
                "adset_name": ins.get("adset_name", ""),
                "ad_name": ins.get("ad_name", ""),
                "impressions": int(ins.get("impressions", 0) or 0),
                "reach": int(ins.get("reach", 0) or 0),
                "frequency": round(float(ins.get("frequency", 0) or 0), 2),
                "clicks": int(ins.get("clicks", 0) or 0),
                "ctr": round(float(ins.get("ctr", 0) or 0), 4),
                "cpm_brl": cents_to_brl(ins.get("cpm")),
                "spend_brl": cents_to_brl(ins.get("spend")),
                f"{action_type}s": extract_actions(ins.get("actions"), action_type),
            }
        )

    if not rows:
        print("Sem dados pro período/level.")
        return

    headers = list(rows[0].keys())

    if output == "csv":
        writer = csv.DictWriter(sys.stdout, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
    else:
        print(f"\nLevel: {level} | Período: {since} a {until} | {len(rows)} linhas\n")
        widths = [
            max(len(h), max((len(str(r[h])) for r in rows), default=0)) for h in headers
        ]
        print("  ".join(h.ljust(widths[i]) for i, h in enumerate(headers)))
        print("  ".join("-" * w for w in widths))
        for r in rows:
            print("  ".join(str(r[h]).ljust(widths[i]) for i, h in enumerate(headers)))


if __name__ == "__main__":
    main()
