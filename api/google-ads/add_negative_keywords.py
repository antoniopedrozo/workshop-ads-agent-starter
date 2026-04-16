"""
Adiciona negativas no nível de campanha ou ad group.

Negativa impede que seu ad apareça quando o termo aparece na busca.
Recomendado: mantenha lista compartilhada (shared set) pra reusar entre
campanhas, e use este script pra adicionar ao set específico ou direto na campanha.

Uso (campaign-level):
    python api/google-ads/add_negative_keywords.py \\
        --campaign-id 1234567890 \\
        --match-type PHRASE \\
        --negatives "grátis,free,curso,tcc,monografia"

Uso (ad group-level):
    python api/google-ads/add_negative_keywords.py \\
        --ad-group-id 9876543210 \\
        --match-type BROAD \\
        --negatives-file negatives.txt
"""

from pathlib import Path

import click
from google.ads.googleads.errors import GoogleAdsException

from _client import (
    get_client,
    get_customer_id,
    handle_google_ads_error,
)


def parse_negatives(inline: str, file_path: Path) -> list:
    negatives = []
    if file_path:
        for line in file_path.read_text(encoding="utf-8").splitlines():
            n = line.strip()
            if n and not n.startswith("#"):
                negatives.append(n)
    if inline:
        negatives.extend([k.strip() for k in inline.split(",") if k.strip()])
    return negatives


@click.command()
@click.option("--campaign-id", help="Adiciona negativas no nível de campanha")
@click.option("--ad-group-id", help="Adiciona negativas no nível de ad group")
@click.option(
    "--match-type",
    type=click.Choice(["EXACT", "PHRASE", "BROAD"], case_sensitive=False),
    default="PHRASE",
)
@click.option("--negatives", help="Negativas separadas por vírgula")
@click.option(
    "--negatives-file",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="Arquivo com 1 negativa por linha",
)
@click.option("--yes", is_flag=True, help="Pula confirmação")
def main(campaign_id, ad_group_id, match_type, negatives, negatives_file, yes):
    """Adiciona negativas a campanha ou ad group."""
    if not (campaign_id or ad_group_id):
        raise click.UsageError("Informe --campaign-id OU --ad-group-id.")
    if campaign_id and ad_group_id:
        raise click.UsageError("Use só um: --campaign-id OU --ad-group-id, não ambos.")

    neg_list = parse_negatives(negatives or "", negatives_file)
    if not neg_list:
        raise click.UsageError("Nenhuma negativa. Use --negatives ou --negatives-file.")

    target = f"campaign {campaign_id}" if campaign_id else f"ad_group {ad_group_id}"
    print(f"\nVai adicionar {len(neg_list)} negativas ({match_type}) em {target}:")
    for n in neg_list[:30]:
        print(f"  - {n}")
    if len(neg_list) > 30:
        print(f"  ... e mais {len(neg_list) - 30}")

    if not yes:
        click.confirm("\nConfirmar?", abort=True)

    client = get_client()
    customer_id = get_customer_id()

    operations = []

    if campaign_id:
        campaign_service = client.get_service("CampaignService")
        campaign_path = campaign_service.campaign_path(customer_id, campaign_id)
        for n in neg_list:
            op = client.get_type("CampaignCriterionOperation")
            criterion = op.create
            criterion.campaign = campaign_path
            criterion.negative = True
            criterion.keyword.text = n
            criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum[match_type.upper()]
            operations.append(op)
        try:
            service = client.get_service("CampaignCriterionService")
            response = service.mutate_campaign_criteria(
                customer_id=customer_id, operations=operations
            )
            print(f"\n{len(response.results)} negativas adicionadas em campaign {campaign_id}.")
        except GoogleAdsException as ex:
            handle_google_ads_error(ex)
    else:
        ad_group_service = client.get_service("AdGroupService")
        ad_group_path = ad_group_service.ad_group_path(customer_id, ad_group_id)
        for n in neg_list:
            op = client.get_type("AdGroupCriterionOperation")
            criterion = op.create
            criterion.ad_group = ad_group_path
            criterion.negative = True
            criterion.keyword.text = n
            criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum[match_type.upper()]
            operations.append(op)
        try:
            service = client.get_service("AdGroupCriterionService")
            response = service.mutate_ad_group_criteria(
                customer_id=customer_id, operations=operations
            )
            print(f"\n{len(response.results)} negativas adicionadas em ad_group {ad_group_id}.")
        except GoogleAdsException as ex:
            handle_google_ads_error(ex)


if __name__ == "__main__":
    main()
