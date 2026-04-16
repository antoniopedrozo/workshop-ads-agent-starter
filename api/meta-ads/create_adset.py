"""
Cria um Ad Set vinculado a uma campanha existente.

Ad Set define targeting, budget e schedule.

Uso simples (com Custom Audience existente):
    python api/meta-ads/create_adset.py \\
        --campaign-id 120150000000000 \\
        --name "Adset - LAL 1% clientes" \\
        --daily-budget 50 \\
        --optimization-goal OFFSITE_CONVERSIONS \\
        --custom-audience-id 23850000000000 \\
        --start-time "2026-04-20T10:00:00-0300"

Uso com targeting por interesse (cold prospecting):
    python api/meta-ads/create_adset.py \\
        --campaign-id 120150000000000 \\
        --name "Adset - Heads de RH BR" \\
        --daily-budget 100 \\
        --optimization-goal LEAD_GENERATION \\
        --countries BR \\
        --age-min 28 --age-max 55 \\
        --start-time "2026-04-20T10:00:00-0300"
"""

import click
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adset import AdSet

from _client import brl_to_cents, get_ad_account_id, init_api


@click.command()
@click.option("--campaign-id", required=True)
@click.option("--name", required=True)
@click.option("--daily-budget", required=True, type=float, help="Em BRL por dia")
@click.option(
    "--optimization-goal",
    type=click.Choice(
        ["OFFSITE_CONVERSIONS", "LEAD_GENERATION", "LINK_CLICKS", "REACH", "IMPRESSIONS", "VIDEO_VIEWS"]
    ),
    default="OFFSITE_CONVERSIONS",
)
@click.option("--billing-event", type=click.Choice(["IMPRESSIONS", "LINK_CLICKS"]), default="IMPRESSIONS")
@click.option("--bid-amount-brl", type=float, help="Lance manual em BRL (opcional)")
@click.option("--custom-audience-id", help="ID de Custom Audience pra usar como targeting")
@click.option("--countries", default="BR", help="ISO codes separados por vírgula (BR,US,...)")
@click.option("--age-min", type=int, default=18)
@click.option("--age-max", type=int, default=65)
@click.option("--start-time", required=True, help="ISO 8601 com timezone, ex 2026-04-20T10:00:00-0300")
@click.option("--end-time", help="ISO 8601, opcional")
@click.option("--status", type=click.Choice(["PAUSED", "ACTIVE"]), default="PAUSED")
@click.option("--yes", is_flag=True)
def main(
    campaign_id, name, daily_budget, optimization_goal, billing_event, bid_amount_brl,
    custom_audience_id, countries, age_min, age_max, start_time, end_time, status, yes
):
    """Cria Ad Set."""
    init_api()
    account = AdAccount(get_ad_account_id())

    targeting = {
        "geo_locations": {"countries": [c.strip() for c in countries.split(",") if c.strip()]},
        "age_min": age_min,
        "age_max": age_max,
    }
    if custom_audience_id:
        targeting["custom_audiences"] = [{"id": custom_audience_id}]

    print(f"\nVai criar Ad Set:")
    print(f"  Nome: {name}")
    print(f"  Campaign: {campaign_id}")
    print(f"  Budget diário: R$ {daily_budget:.2f}")
    print(f"  Optimization goal: {optimization_goal}")
    print(f"  Billing event: {billing_event}")
    print(f"  Targeting: {targeting}")
    print(f"  Start: {start_time}")
    if end_time:
        print(f"  End: {end_time}")
    print(f"  Status: {status}")

    if not yes:
        click.confirm("\nConfirmar?", abort=True)

    params = {
        AdSet.Field.name: name,
        AdSet.Field.campaign_id: campaign_id,
        AdSet.Field.daily_budget: brl_to_cents(daily_budget),
        AdSet.Field.optimization_goal: optimization_goal,
        AdSet.Field.billing_event: billing_event,
        AdSet.Field.targeting: targeting,
        AdSet.Field.start_time: start_time,
        AdSet.Field.status: status,
    }
    if end_time:
        params[AdSet.Field.end_time] = end_time
    if bid_amount_brl is not None:
        params[AdSet.Field.bid_amount] = brl_to_cents(bid_amount_brl)

    adset = account.create_ad_set(params=params)
    print(f"\nAd Set criado:")
    print(f"  ID: {adset['id']}")


if __name__ == "__main__":
    main()
