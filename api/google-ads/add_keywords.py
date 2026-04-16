"""
Adiciona keywords a um ad group existente.

Uso:
    python api/google-ads/add_keywords.py \\
        --ad-group-id 1234567890 \\
        --match-type PHRASE \\
        --keywords "pesquisa de clima organizacional,como medir engajamento,..."

Ou via arquivo:

    python api/google-ads/add_keywords.py \\
        --ad-group-id 1234567890 \\
        --match-type PHRASE \\
        --keywords-file keywords.txt

(arquivo com uma keyword por linha)
"""

from pathlib import Path

import click
from google.ads.googleads.errors import GoogleAdsException

from _client import (
    get_client,
    get_customer_id,
    handle_google_ads_error,
)


def parse_keywords(inline: str, file_path: Path) -> list:
    """Parse keywords de string inline OU de arquivo (1 por linha)."""
    keywords = []
    if file_path:
        for line in file_path.read_text(encoding="utf-8").splitlines():
            kw = line.strip()
            if kw and not kw.startswith("#"):
                keywords.append(kw)
    if inline:
        keywords.extend([k.strip() for k in inline.split(",") if k.strip()])
    return keywords


@click.command()
@click.option("--ad-group-id", required=True)
@click.option(
    "--match-type",
    type=click.Choice(["EXACT", "PHRASE", "BROAD"], case_sensitive=False),
    default="PHRASE",
)
@click.option("--keywords", help="Keywords separadas por vírgula")
@click.option(
    "--keywords-file",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="Arquivo com 1 keyword por linha (linhas com # são ignoradas)",
)
@click.option("--yes", is_flag=True, help="Pula confirmação")
def main(ad_group_id, match_type, keywords, keywords_file, yes):
    """Adiciona keywords a um ad group."""
    keyword_list = parse_keywords(keywords or "", keywords_file)
    if not keyword_list:
        raise click.UsageError("Nenhuma keyword. Use --keywords ou --keywords-file.")

    print(f"\nVai adicionar {len(keyword_list)} keywords ({match_type}) ao ad group {ad_group_id}:")
    for kw in keyword_list[:20]:
        print(f"  - {kw}")
    if len(keyword_list) > 20:
        print(f"  ... e mais {len(keyword_list) - 20}")

    if not yes:
        click.confirm("\nConfirmar?", abort=True)

    client = get_client()
    customer_id = get_customer_id()
    ad_group_service = client.get_service("AdGroupService")
    ad_group_path = ad_group_service.ad_group_path(customer_id, ad_group_id)

    operations = []
    for kw in keyword_list:
        op = client.get_type("AdGroupCriterionOperation")
        criterion = op.create
        criterion.ad_group = ad_group_path
        criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
        criterion.keyword.text = kw
        criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum[match_type.upper()]
        operations.append(op)

    try:
        service = client.get_service("AdGroupCriterionService")
        response = service.mutate_ad_group_criteria(
            customer_id=customer_id, operations=operations
        )
        print(f"\n{len(response.results)} keywords adicionadas com sucesso.")
    except GoogleAdsException as ex:
        handle_google_ads_error(ex)


if __name__ == "__main__":
    main()
