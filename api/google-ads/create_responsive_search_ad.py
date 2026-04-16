"""
Cria um Responsive Search Ad (RSA) num ad group existente.

RSA aceita 3 a 15 headlines (até 30 caracteres cada) e 2 a 4 descriptions
(até 90 caracteres cada). O Google testa combinações automaticamente.

Uso:
    python api/google-ads/create_responsive_search_ad.py \\
        --ad-group-id 1234567890 \\
        --final-url "https://acmerh.com.br/clima-organizacional" \\
        --headlines "Pesquisa de Clima|Pulse Semanal no Slack|+200 empresas|92% de resposta|..." \\
        --descriptions "Pulse semanal direto no Slack ou Teams.|Dashboard pronto pra board.|..."

Headlines e descriptions são separados por pipe `|`.
"""

import sys

import click
from google.ads.googleads.errors import GoogleAdsException

from _client import (
    get_client,
    get_customer_id,
    handle_google_ads_error,
)

MAX_HEADLINE_LEN = 30
MAX_DESCRIPTION_LEN = 90


def validate_assets(items, max_len, kind):
    """Valida limite de caracteres."""
    over = [(i, t) for i, t in enumerate(items) if len(t) > max_len]
    if over:
        print(f"\nErro: {len(over)} {kind}(s) excedem {max_len} caracteres:")
        for i, t in over:
            print(f"  [{i}] ({len(t)} chars): {t}")
        sys.exit(1)


@click.command()
@click.option("--ad-group-id", required=True)
@click.option("--final-url", required=True, help="URL de destino do ad")
@click.option(
    "--headlines",
    required=True,
    help="Headlines separados por |. Mínimo 3, máximo 15. Cada um até 30 chars.",
)
@click.option(
    "--descriptions",
    required=True,
    help="Descriptions separados por |. Mínimo 2, máximo 4. Cada um até 90 chars.",
)
@click.option("--path1", default="", help="Display path 1 (parte da URL exibida)")
@click.option("--path2", default="", help="Display path 2")
@click.option("--status", type=click.Choice(["PAUSED", "ENABLED"]), default="ENABLED")
@click.option("--yes", is_flag=True, help="Pula confirmação")
def main(ad_group_id, final_url, headlines, descriptions, path1, path2, status, yes):
    """Cria responsive search ad."""
    headline_list = [h.strip() for h in headlines.split("|") if h.strip()]
    description_list = [d.strip() for d in descriptions.split("|") if d.strip()]

    if not 3 <= len(headline_list) <= 15:
        sys.exit(f"Erro: precisa de 3 a 15 headlines, recebeu {len(headline_list)}.")
    if not 2 <= len(description_list) <= 4:
        sys.exit(f"Erro: precisa de 2 a 4 descriptions, recebeu {len(description_list)}.")

    validate_assets(headline_list, MAX_HEADLINE_LEN, "headline")
    validate_assets(description_list, MAX_DESCRIPTION_LEN, "description")

    print(f"\nVai criar Responsive Search Ad:")
    print(f"  Ad Group ID: {ad_group_id}")
    print(f"  Final URL: {final_url}")
    print(f"  Headlines ({len(headline_list)}):")
    for h in headline_list:
        print(f"    - {h}  ({len(h)} chars)")
    print(f"  Descriptions ({len(description_list)}):")
    for d in description_list:
        print(f"    - {d}  ({len(d)} chars)")
    print(f"  Status: {status}")

    if not yes:
        click.confirm("\nConfirmar criação?", abort=True)

    client = get_client()
    customer_id = get_customer_id()

    try:
        ad_group_service = client.get_service("AdGroupService")
        ad_group_ad_service = client.get_service("AdGroupAdService")

        operation = client.get_type("AdGroupAdOperation")
        ad_group_ad = operation.create
        ad_group_ad.ad_group = ad_group_service.ad_group_path(customer_id, ad_group_id)
        ad_group_ad.status = client.enums.AdGroupAdStatusEnum[status]

        ad = ad_group_ad.ad
        ad.final_urls.append(final_url)

        rsa = ad.responsive_search_ad
        for h in headline_list:
            asset = client.get_type("AdTextAsset")
            asset.text = h
            rsa.headlines.append(asset)
        for d in description_list:
            asset = client.get_type("AdTextAsset")
            asset.text = d
            rsa.descriptions.append(asset)

        if path1:
            rsa.path1 = path1
        if path2:
            rsa.path2 = path2

        response = ad_group_ad_service.mutate_ad_group_ads(
            customer_id=customer_id, operations=[operation]
        )
        ad_resource = response.results[0].resource_name
        ad_id = ad_resource.split("~")[-1]

        print(f"\nAd criado com sucesso.")
        print(f"  Resource: {ad_resource}")
        print(f"  Ad ID: {ad_id}")

    except GoogleAdsException as ex:
        handle_google_ads_error(ex)


if __name__ == "__main__":
    main()
