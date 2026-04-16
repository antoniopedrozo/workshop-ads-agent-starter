"""
Cria um Campaign Group no LinkedIn.

Uso:
    python api/linkedin-ads/create_campaign_group.py --name "Q1 2026 - Demand Gen"
"""

import click

from _client import get_account_urn, post


@click.command()
@click.option("--name", required=True)
@click.option(
    "--status",
    type=click.Choice(["DRAFT", "ACTIVE", "PAUSED"]),
    default="DRAFT",
)
@click.option("--total-budget-brl", type=float, help="Budget total opcional em BRL")
@click.option("--yes", is_flag=True)
def main(name, status, total_budget_brl, yes):
    """Cria Campaign Group."""
    print(f"\nVai criar Campaign Group:")
    print(f"  Nome: {name}")
    print(f"  Account: {get_account_urn()}")
    print(f"  Status: {status}")
    if total_budget_brl:
        print(f"  Budget total: R$ {total_budget_brl:.2f}")

    if not yes:
        click.confirm("\nConfirmar?", abort=True)

    payload = {
        "name": name,
        "account": get_account_urn(),
        "status": status,
    }
    if total_budget_brl:
        payload["totalBudget"] = {
            "amount": str(int(total_budget_brl)),
            "currencyCode": "BRL",
        }

    response = post("/adCampaignGroups", payload)
    location = response.headers.get("Location", "")
    group_id = location.split("/")[-1] if location else "(verifique no UI)"
    print(f"\nCampaign Group criado:")
    print(f"  ID: {group_id}")
    print(f"  URN: urn:li:sponsoredCampaignGroup:{group_id}")


if __name__ == "__main__":
    main()
