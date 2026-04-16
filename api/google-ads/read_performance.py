"""
Lê relatórios de performance do Google Ads.

Reports disponíveis:
- campaigns: performance por campanha (gasto, cliques, conversões, CTR, CAC)
- ad-groups: performance por ad group
- search-terms: termos de busca reais (pra pruning) com gasto e conversões
- keywords: performance das keywords ativas

Uso:
    python api/google-ads/read_performance.py --report campaigns --days 30
    python api/google-ads/read_performance.py --report search-terms --days 30 --min-cost 50
    python api/google-ads/read_performance.py --report ad-groups --days 7 --output csv > report.csv
"""

import csv
import sys

import click
from google.ads.googleads.errors import GoogleAdsException

from _client import (
    get_client,
    get_customer_id,
    handle_google_ads_error,
)


REPORTS = {
    "campaigns": {
        "select": (
            "campaign.id, campaign.name, campaign.status, "
            "metrics.cost_micros, metrics.impressions, metrics.clicks, "
            "metrics.conversions, metrics.ctr, metrics.average_cpc"
        ),
        "from": "campaign",
        "headers": ["campaign_id", "campaign_name", "status", "cost_brl", "impressions", "clicks", "conversions", "ctr", "avg_cpc_brl"],
    },
    "ad-groups": {
        "select": (
            "campaign.name, ad_group.id, ad_group.name, ad_group.status, "
            "metrics.cost_micros, metrics.impressions, metrics.clicks, "
            "metrics.conversions, metrics.ctr"
        ),
        "from": "ad_group",
        "headers": ["campaign_name", "ad_group_id", "ad_group_name", "status", "cost_brl", "impressions", "clicks", "conversions", "ctr"],
    },
    "search-terms": {
        "select": (
            "campaign.name, ad_group.name, search_term_view.search_term, "
            "metrics.cost_micros, metrics.impressions, metrics.clicks, "
            "metrics.conversions"
        ),
        "from": "search_term_view",
        "headers": ["campaign_name", "ad_group_name", "search_term", "cost_brl", "impressions", "clicks", "conversions"],
    },
    "keywords": {
        "select": (
            "campaign.name, ad_group.name, ad_group_criterion.keyword.text, "
            "ad_group_criterion.keyword.match_type, ad_group_criterion.status, "
            "metrics.cost_micros, metrics.clicks, metrics.conversions"
        ),
        "from": "keyword_view",
        "headers": ["campaign_name", "ad_group_name", "keyword", "match_type", "status", "cost_brl", "clicks", "conversions"],
    },
}


def micros_to_brl(micros: int) -> float:
    return round(micros / 1_000_000, 2)


def extract_row(report_name: str, row) -> list:
    """Extrai a linha conforme o tipo de report."""
    if report_name == "campaigns":
        return [
            row.campaign.id,
            row.campaign.name,
            row.campaign.status.name,
            micros_to_brl(row.metrics.cost_micros),
            row.metrics.impressions,
            row.metrics.clicks,
            round(row.metrics.conversions, 2),
            round(row.metrics.ctr, 4),
            micros_to_brl(row.metrics.average_cpc),
        ]
    if report_name == "ad-groups":
        return [
            row.campaign.name,
            row.ad_group.id,
            row.ad_group.name,
            row.ad_group.status.name,
            micros_to_brl(row.metrics.cost_micros),
            row.metrics.impressions,
            row.metrics.clicks,
            round(row.metrics.conversions, 2),
            round(row.metrics.ctr, 4),
        ]
    if report_name == "search-terms":
        return [
            row.campaign.name,
            row.ad_group.name,
            row.search_term_view.search_term,
            micros_to_brl(row.metrics.cost_micros),
            row.metrics.impressions,
            row.metrics.clicks,
            round(row.metrics.conversions, 2),
        ]
    if report_name == "keywords":
        return [
            row.campaign.name,
            row.ad_group.name,
            row.ad_group_criterion.keyword.text,
            row.ad_group_criterion.keyword.match_type.name,
            row.ad_group_criterion.status.name,
            micros_to_brl(row.metrics.cost_micros),
            row.metrics.clicks,
            round(row.metrics.conversions, 2),
        ]


@click.command()
@click.option("--report", type=click.Choice(list(REPORTS.keys())), required=True)
@click.option("--days", type=int, default=30, help="Período em dias (default 30)")
@click.option("--min-cost", type=float, default=0, help="Filtra rows com gasto >= valor em BRL")
@click.option("--output", type=click.Choice(["table", "csv"]), default="table")
@click.option("--limit", type=int, default=200, help="Máximo de linhas (default 200)")
def main(report, days, min_cost, output, limit):
    """Lê relatório de performance e imprime."""
    client = get_client()
    customer_id = get_customer_id()
    cfg = REPORTS[report]

    where = f"segments.date DURING LAST_{days}_DAYS"
    if min_cost > 0:
        min_micros = int(min_cost * 1_000_000)
        where += f" AND metrics.cost_micros >= {min_micros}"

    query = (
        f"SELECT {cfg['select']} "
        f"FROM {cfg['from']} "
        f"WHERE {where} "
        f"ORDER BY metrics.cost_micros DESC "
        f"LIMIT {limit}"
    )

    try:
        ga_service = client.get_service("GoogleAdsService")
        rows = list(ga_service.search(customer_id=customer_id, query=query))
    except GoogleAdsException as ex:
        handle_google_ads_error(ex)

    extracted = [extract_row(report, row) for row in rows]

    if output == "csv":
        writer = csv.writer(sys.stdout)
        writer.writerow(cfg["headers"])
        writer.writerows(extracted)
    else:
        # Tabela simples no terminal
        print(f"\nReport: {report} | Período: últimos {days} dias | {len(extracted)} linhas\n")
        widths = [
            max(len(str(h)), max((len(str(r[i])) for r in extracted), default=0))
            for i, h in enumerate(cfg["headers"])
        ]
        sep = "  ".join("-" * w for w in widths)
        header = "  ".join(h.ljust(widths[i]) for i, h in enumerate(cfg["headers"]))
        print(header)
        print(sep)
        for r in extracted:
            print("  ".join(str(r[i]).ljust(widths[i]) for i in range(len(r))))


if __name__ == "__main__":
    main()
