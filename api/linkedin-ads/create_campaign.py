"""
Cria uma Campaign dentro de um Campaign Group.

Tipos:
- SPONSORED_UPDATES (Sponsored Content, formato mais comum)
- TEXT_AD
- DYNAMIC
- SPONSORED_INMAILS (Message Ads / Conversation Ads)

Objetivos:
- BRAND_AWARENESS, ENGAGEMENT, JOB_APPLICANTS, LEAD_GENERATION,
  VIDEO_VIEWS, WEBSITE_CONVERSIONS, WEBSITE_VISITS

Targeting é simplificado neste script (Country + Job Titles + Company Sizes via JSON inline).
Pra targeting avançado, edite o `targetingCriteria` no payload.

Uso simplificado:
    python api/linkedin-ads/create_campaign.py \\
        --group-id 123456789 \\
        --name "Heads de RH BR - Sponsored Content" \\
        --type SPONSORED_UPDATES \\
        --objective LEAD_GENERATION \\
        --daily-budget 200 \\
        --total-budget 6000 \\
        --start-date 2026-04-20 \\
        --countries BR \\
        --job-title-urns "urn:li:title:25,urn:li:title:9846" \\
        --company-size-codes E,F,G
"""

from datetime import datetime

import click

from _client import brl_to_cents, get_account_urn, post


def to_date_obj(date_str: str) -> dict:
    d = datetime.strptime(date_str, "%Y-%m-%d")
    return {"year": d.year, "month": d.month, "day": d.day}


@click.command()
@click.option("--group-id", required=True, help="ID do Campaign Group")
@click.option("--name", required=True)
@click.option(
    "--type",
    "campaign_type",
    type=click.Choice(["SPONSORED_UPDATES", "TEXT_AD", "DYNAMIC", "SPONSORED_INMAILS"]),
    default="SPONSORED_UPDATES",
)
@click.option(
    "--objective",
    type=click.Choice(
        [
            "BRAND_AWARENESS",
            "ENGAGEMENT",
            "JOB_APPLICANTS",
            "LEAD_GENERATION",
            "VIDEO_VIEWS",
            "WEBSITE_CONVERSIONS",
            "WEBSITE_VISITS",
        ]
    ),
    default="WEBSITE_CONVERSIONS",
)
@click.option("--daily-budget", required=True, type=float, help="BRL/dia")
@click.option("--total-budget", required=True, type=float, help="BRL total")
@click.option("--start-date", required=True, help="YYYY-MM-DD")
@click.option("--end-date", help="YYYY-MM-DD opcional")
@click.option(
    "--countries",
    default="BR",
    help="Códigos de país separados por vírgula (BR,US,...)",
)
@click.option(
    "--job-title-urns",
    default="",
    help="URNs de títulos separados por vírgula (ex: urn:li:title:25,urn:li:title:9846)",
)
@click.option(
    "--company-size-codes",
    default="",
    help="Códigos de tamanho separados por vírgula (A=1-10, B=11-50, C=51-200, D=201-500, E=501-1000, F=1001-5000, G=5001-10000, H=10000+)",
)
@click.option("--cost-type", type=click.Choice(["CPM", "CPC", "CPV"]), default="CPM")
@click.option("--unit-cost-brl", type=float, default=20.0, help="Lance manual em BRL (CPC/CPM)")
@click.option("--status", type=click.Choice(["DRAFT", "ACTIVE", "PAUSED"]), default="DRAFT")
@click.option("--yes", is_flag=True)
def main(
    group_id, name, campaign_type, objective, daily_budget, total_budget, start_date, end_date,
    countries, job_title_urns, company_size_codes, cost_type, unit_cost_brl, status, yes
):
    """Cria Campaign."""
    print(f"\nVai criar Campaign:")
    print(f"  Nome: {name}")
    print(f"  Group: urn:li:sponsoredCampaignGroup:{group_id}")
    print(f"  Tipo: {campaign_type}")
    print(f"  Objetivo: {objective}")
    print(f"  Budget: R$ {daily_budget:.2f}/dia | R$ {total_budget:.2f} total")
    print(f"  Start: {start_date} | End: {end_date or '(sem fim)'}")
    print(f"  Países: {countries}")
    if job_title_urns:
        print(f"  Job titles: {job_title_urns}")
    if company_size_codes:
        print(f"  Company sizes: {company_size_codes}")
    print(f"  Cost type: {cost_type} @ R$ {unit_cost_brl:.2f}")

    if not yes:
        click.confirm("\nConfirmar?", abort=True)

    # Targeting
    country_urns = [
        f"urn:li:country:{c.strip().lower()}" for c in countries.split(",") if c.strip()
    ]
    targeting_facets = [
        {"facet": "urn:li:adTargetingFacet:locations", "values": country_urns},
    ]
    if job_title_urns:
        titles = [t.strip() for t in job_title_urns.split(",") if t.strip()]
        targeting_facets.append(
            {"facet": "urn:li:adTargetingFacet:titles", "values": titles}
        )
    if company_size_codes:
        sizes = [s.strip().upper() for s in company_size_codes.split(",") if s.strip()]
        targeting_facets.append(
            {"facet": "urn:li:adTargetingFacet:staffCountRanges", "values": sizes}
        )

    payload = {
        "account": get_account_urn(),
        "campaignGroup": f"urn:li:sponsoredCampaignGroup:{group_id}",
        "name": name,
        "type": campaign_type,
        "objectiveType": objective,
        "status": status,
        "costType": cost_type,
        "unitCost": {"amount": str(unit_cost_brl), "currencyCode": "BRL"},
        "dailyBudget": {"amount": str(daily_budget), "currencyCode": "BRL"},
        "totalBudget": {"amount": str(total_budget), "currencyCode": "BRL"},
        "runSchedule": {"start": int(datetime.strptime(start_date, "%Y-%m-%d").timestamp() * 1000)},
        "targetingCriteria": {
            "include": {"and": [{"or": {f["facet"]: f["values"]}} for f in targeting_facets]},
        },
    }
    if end_date:
        payload["runSchedule"]["end"] = int(datetime.strptime(end_date, "%Y-%m-%d").timestamp() * 1000)

    response = post("/adCampaigns", payload)
    location = response.headers.get("Location", "")
    campaign_id = location.split("/")[-1] if location else "(verifique no UI)"
    print(f"\nCampaign criada:")
    print(f"  ID: {campaign_id}")
    print(f"  URN: urn:li:sponsoredCampaign:{campaign_id}")


if __name__ == "__main__":
    main()
