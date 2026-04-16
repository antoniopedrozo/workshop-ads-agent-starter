"""
Lê analytics do LinkedIn Ads via API de relatórios.

Pivots suportados:
- CAMPAIGN
- CREATIVE
- COMPANY (anonimizado)
- IMPRESSION_DEVICE_TYPE
- MEMBER_COUNTRY_V2
- MEMBER_INDUSTRY
- MEMBER_SENIORITY

Uso:
    python api/linkedin-ads/read_analytics.py --pivot CAMPAIGN --days 30
    python api/linkedin-ads/read_analytics.py --pivot CREATIVE --days 14 --output csv > data.csv
"""

import csv
import sys
from datetime import datetime, timedelta

import click

from _client import get_account_urn, get


FIELDS = [
    "impressions",
    "clicks",
    "costInLocalCurrency",
    "externalWebsiteConversions",
    "leadGenerationMailContactInfoShares",
    "oneClickLeads",
    "videoViews",
]


@click.command()
@click.option(
    "--pivot",
    type=click.Choice(
        [
            "CAMPAIGN",
            "CREATIVE",
            "COMPANY",
            "IMPRESSION_DEVICE_TYPE",
            "MEMBER_COUNTRY_V2",
            "MEMBER_INDUSTRY",
            "MEMBER_SENIORITY",
        ]
    ),
    default="CAMPAIGN",
)
@click.option("--days", type=int, default=30)
@click.option("--output", type=click.Choice(["table", "csv"]), default="table")
def main(pivot, days, output):
    """Puxa analytics agregado por pivot."""
    end = datetime.now()
    start = end - timedelta(days=days)

    params = {
        "q": "analytics",
        "pivot": pivot,
        "dateRange.start.day": start.day,
        "dateRange.start.month": start.month,
        "dateRange.start.year": start.year,
        "dateRange.end.day": end.day,
        "dateRange.end.month": end.month,
        "dateRange.end.year": end.year,
        "timeGranularity": "ALL",
        "accounts[0]": get_account_urn(),
        "fields": ",".join(FIELDS + ["pivotValue"]),
    }

    data = get("/adAnalytics", params)
    elements = data.get("elements", [])

    rows = []
    for el in elements:
        rows.append(
            {
                "pivot_value": el.get("pivotValue", ""),
                "impressions": int(el.get("impressions", 0) or 0),
                "clicks": int(el.get("clicks", 0) or 0),
                "spend_brl": round(float(el.get("costInLocalCurrency", 0) or 0), 2),
                "web_conversions": int(el.get("externalWebsiteConversions", 0) or 0),
                "leads": int(el.get("oneClickLeads", 0) or 0),
                "video_views": int(el.get("videoViews", 0) or 0),
            }
        )

    if not rows:
        print("Sem dados pro período/pivot.")
        return

    headers = list(rows[0].keys())

    if output == "csv":
        writer = csv.DictWriter(sys.stdout, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
    else:
        print(f"\nPivot: {pivot} | Período: últimos {days} dias | {len(rows)} linhas\n")
        widths = [
            max(len(h), max((len(str(r[h])) for r in rows), default=0)) for h in headers
        ]
        print("  ".join(h.ljust(widths[i]) for i, h in enumerate(headers)))
        print("  ".join("-" * w for w in widths))
        for r in rows:
            print("  ".join(str(r[h]).ljust(widths[i]) for i, h in enumerate(headers)))


if __name__ == "__main__":
    main()
