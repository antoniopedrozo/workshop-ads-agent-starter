"""
Cria um ad group dentro de uma campanha existente.

Uso:
    python api/google-ads/create_ad_group.py \\
        --campaign-id 1234567890 \\
        --name "Pesquisa de Clima - Phrase" \\
        --default-cpc 5.00
"""

import click
from google.ads.googleads.errors import GoogleAdsException

from _client import (
    brl_to_micros,
    get_client,
    get_customer_id,
    handle_google_ads_error,
)


@click.command()
@click.option("--campaign-id", required=True, help="ID da campanha existente")
@click.option("--name", required=True, help="Nome do ad group")
@click.option(
    "--default-cpc",
    type=float,
    default=2.0,
    help="CPC default em BRL (usado só se a campanha for Manual CPC)",
)
@click.option("--status", type=click.Choice(["PAUSED", "ENABLED"]), default="ENABLED")
@click.option("--yes", is_flag=True, help="Pula confirmação interativa")
def main(campaign_id, name, default_cpc, status, yes):
    """Cria ad group e imprime o ID."""
    client = get_client()
    customer_id = get_customer_id()

    print(f"\nVai criar ad group:")
    print(f"  Nome: {name}")
    print(f"  Campaign ID: {campaign_id}")
    print(f"  Default CPC: R$ {default_cpc:.2f} (ignorado se a campanha não é Manual CPC)")
    print(f"  Status: {status}")

    if not yes:
        click.confirm("\nConfirmar criação?", abort=True)

    try:
        campaign_service = client.get_service("CampaignService")
        ad_group_service = client.get_service("AdGroupService")

        operation = client.get_type("AdGroupOperation")
        ad_group = operation.create
        ad_group.name = name
        ad_group.campaign = campaign_service.campaign_path(customer_id, campaign_id)
        ad_group.type_ = client.enums.AdGroupTypeEnum.SEARCH_STANDARD
        ad_group.status = client.enums.AdGroupStatusEnum[status]
        ad_group.cpc_bid_micros = brl_to_micros(default_cpc)

        response = ad_group_service.mutate_ad_groups(
            customer_id=customer_id, operations=[operation]
        )
        ad_group_resource = response.results[0].resource_name
        ad_group_id = ad_group_resource.split("/")[-1]

        print(f"\nAd group criado com sucesso.")
        print(f"  Resource: {ad_group_resource}")
        print(f"  Ad Group ID: {ad_group_id}")
        print(f"\nPróximos passos:")
        print(
            f"  1. Adicionar keywords: python api/google-ads/add_keywords.py "
            f"--ad-group-id {ad_group_id} --match-type PHRASE --keywords '...'"
        )
        print(
            f"  2. Criar ad: python api/google-ads/create_responsive_search_ad.py "
            f"--ad-group-id {ad_group_id} --headlines '...' --descriptions '...' --final-url '...'"
        )

    except GoogleAdsException as ex:
        handle_google_ads_error(ex)


if __name__ == "__main__":
    main()
