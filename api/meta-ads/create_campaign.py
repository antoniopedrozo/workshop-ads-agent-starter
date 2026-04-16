"""
Cria uma campanha no Meta Marketing API.

Campanha define o OBJETIVO. Targeting, budget e schedule ficam no Ad Set.

Objetivos suportados (Meta v17+):
- OUTCOME_SALES (conversão de venda/conversão online)
- OUTCOME_LEADS (lead generation, inclusive Lead Gen Form)
- OUTCOME_TRAFFIC (cliques pra LP)
- OUTCOME_AWARENESS (alcance, marca)
- OUTCOME_ENGAGEMENT
- OUTCOME_APP_PROMOTION

Uso:
    python api/meta-ads/create_campaign.py \\
        --name "AcmeRH - Retargeting LP Clima" \\
        --objective OUTCOME_SALES \\
        --status PAUSED
"""

import click
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign

from _client import get_ad_account_id, init_api


@click.command()
@click.option("--name", required=True)
@click.option(
    "--objective",
    type=click.Choice(
        [
            "OUTCOME_SALES",
            "OUTCOME_LEADS",
            "OUTCOME_TRAFFIC",
            "OUTCOME_AWARENESS",
            "OUTCOME_ENGAGEMENT",
            "OUTCOME_APP_PROMOTION",
        ]
    ),
    default="OUTCOME_SALES",
)
@click.option(
    "--special-ad-categories",
    default="NONE",
    help="Categorias especiais separadas por vírgula (HOUSING, EMPLOYMENT, CREDIT, ISSUES_ELECTIONS_POLITICS, NONE). Default: NONE.",
)
@click.option("--status", type=click.Choice(["PAUSED", "ACTIVE"]), default="PAUSED")
@click.option("--yes", is_flag=True)
def main(name, objective, special_ad_categories, status, yes):
    """Cria campanha Meta."""
    init_api()
    account = AdAccount(get_ad_account_id())

    print(f"\nVai criar campanha:")
    print(f"  Nome: {name}")
    print(f"  Account: {account['id']}")
    print(f"  Objetivo: {objective}")
    print(f"  Categorias especiais: {special_ad_categories}")
    print(f"  Status: {status}")

    if not yes:
        click.confirm("\nConfirmar?", abort=True)

    categories = [c.strip() for c in special_ad_categories.split(",") if c.strip()]

    params = {
        Campaign.Field.name: name,
        Campaign.Field.objective: objective,
        Campaign.Field.status: status,
        Campaign.Field.special_ad_categories: categories,
    }

    campaign = account.create_campaign(params=params)
    print(f"\nCampanha criada:")
    print(f"  ID: {campaign['id']}")
    print(f"\nPróximo passo: criar Ad Set.")
    print(
        f"  python api/meta-ads/create_adset.py --campaign-id {campaign['id']} --name '...' --daily-budget 50 ..."
    )


if __name__ == "__main__":
    main()
