"""
Cria uma campanha de Search no Google Ads.

A campanha entra com status PAUSED por padrão (segurança). Você revisa no
Google Ads UI e ativa quando estiver confortável.

Uso:
    python api/google-ads/create_search_campaign.py \\
        --name "AcmeRH - Clima Organizacional - BR - PT" \\
        --budget 100 \\
        --bid-strategy MAXIMIZE_CONVERSIONS \\
        --target-cpa 60

Bid strategies suportadas:
- MAXIMIZE_CONVERSIONS (com --target-cpa opcional)
- MAXIMIZE_CONVERSION_VALUE (com --target-roas opcional)
- TARGET_IMPRESSION_SHARE (pra brand)
- MANUAL_CPC (controle total)
"""

from datetime import datetime, timedelta

import click
from google.ads.googleads.errors import GoogleAdsException

from _client import (
    brl_to_micros,
    get_client,
    get_customer_id,
    handle_google_ads_error,
)


def create_budget(client, customer_id: str, name: str, daily_brl: float) -> str:
    """Cria budget compartilhável (a campanha referencia)."""
    operation = client.get_type("CampaignBudgetOperation")
    budget = operation.create
    budget.name = f"{name} - Budget"
    budget.amount_micros = brl_to_micros(daily_brl)
    budget.delivery_method = client.enums.BudgetDeliveryMethodEnum.STANDARD
    budget.explicitly_shared = False

    service = client.get_service("CampaignBudgetService")
    response = service.mutate_campaign_budgets(customer_id=customer_id, operations=[operation])
    resource = response.results[0].resource_name
    print(f"  Budget criado: {resource}")
    return resource


@click.command()
@click.option("--name", required=True, help="Nome da campanha (siga padrão de naming)")
@click.option("--budget", required=True, type=float, help="Budget diário em BRL (ex: 100 = R$ 100/dia)")
@click.option(
    "--bid-strategy",
    type=click.Choice(
        ["MAXIMIZE_CONVERSIONS", "MAXIMIZE_CONVERSION_VALUE", "TARGET_IMPRESSION_SHARE", "MANUAL_CPC"],
        case_sensitive=False,
    ),
    default="MAXIMIZE_CONVERSIONS",
)
@click.option("--target-cpa", type=float, help="Meta de CPA em BRL (só com MAXIMIZE_CONVERSIONS)")
@click.option("--target-roas", type=float, help="Meta de ROAS em decimal (ex: 4.0 = 400%)")
@click.option("--status", type=click.Choice(["PAUSED", "ENABLED"]), default="PAUSED")
@click.option("--language", default="pt", help="Código do idioma (pt, en, es...)")
@click.option("--country-code", default="BR", help="Código do país alvo (BR, US, ...)")
@click.option("--yes", is_flag=True, help="Pula confirmação interativa")
def main(name, budget, bid_strategy, target_cpa, target_roas, status, language, country_code, yes):
    """Cria campanha de search com budget e bid strategy escolhidos."""
    client = get_client()
    customer_id = get_customer_id()

    print("\nVai criar a seguinte campanha:")
    print(f"  Nome: {name}")
    print(f"  Customer ID: {customer_id}")
    print(f"  Budget diário: R$ {budget:.2f}")
    print(f"  Bid strategy: {bid_strategy}")
    if target_cpa:
        print(f"  Target CPA: R$ {target_cpa:.2f}")
    if target_roas:
        print(f"  Target ROAS: {target_roas}")
    print(f"  Status inicial: {status}")
    print(f"  País/Idioma: {country_code} / {language}")

    if not yes:
        click.confirm("\nConfirmar criação?", abort=True)

    try:
        budget_resource = create_budget(client, customer_id, name, budget)

        operation = client.get_type("CampaignOperation")
        campaign = operation.create
        campaign.name = name
        campaign.advertising_channel_type = client.enums.AdvertisingChannelTypeEnum.SEARCH
        campaign.status = client.enums.CampaignStatusEnum[status]
        campaign.campaign_budget = budget_resource

        # Bid strategy
        if bid_strategy == "MAXIMIZE_CONVERSIONS":
            if target_cpa:
                campaign.maximize_conversions.target_cpa_micros = brl_to_micros(target_cpa)
            else:
                campaign.maximize_conversions.target_cpa_micros = 0
        elif bid_strategy == "MAXIMIZE_CONVERSION_VALUE":
            if target_roas:
                campaign.maximize_conversion_value.target_roas = target_roas
        elif bid_strategy == "TARGET_IMPRESSION_SHARE":
            campaign.target_impression_share.location = (
                client.enums.TargetImpressionShareLocationEnum.TOP_OF_PAGE
            )
            campaign.target_impression_share.location_fraction_micros = 900_000  # 90%
        elif bid_strategy == "MANUAL_CPC":
            campaign.manual_cpc.enhanced_cpc_enabled = False

        # Datas
        campaign.start_date = datetime.now().strftime("%Y%m%d")
        campaign.end_date = (datetime.now() + timedelta(days=365 * 2)).strftime("%Y%m%d")

        # Network: só Search por padrão (sem partners, sem display)
        campaign.network_settings.target_google_search = True
        campaign.network_settings.target_search_network = False
        campaign.network_settings.target_content_network = False
        campaign.network_settings.target_partner_search_network = False

        service = client.get_service("CampaignService")
        response = service.mutate_campaigns(customer_id=customer_id, operations=[operation])
        campaign_resource = response.results[0].resource_name
        campaign_id = campaign_resource.split("/")[-1]

        print(f"\nCampanha criada com sucesso.")
        print(f"  Resource: {campaign_resource}")
        print(f"  Campaign ID: {campaign_id}")
        print(f"\nPróximo passo: criar ad group.")
        print(
            f"  python api/google-ads/create_ad_group.py "
            f"--campaign-id {campaign_id} --name 'Ad Group 1'"
        )

    except GoogleAdsException as ex:
        handle_google_ads_error(ex)


if __name__ == "__main__":
    main()
