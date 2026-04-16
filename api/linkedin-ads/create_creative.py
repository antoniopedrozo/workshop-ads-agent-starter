"""
Cria um Creative no LinkedIn associado a uma Campaign.

Suporta Sponsored Content (post promovido) com referência a uma share existente
(URN no formato urn:li:share:... ou urn:li:ugcPost:...).

Pra outros formatos (Document Ad, Video Ad, Single Image Ad upload direto),
adapte o `variables.data`.

Uso:
    python api/linkedin-ads/create_creative.py \\
        --campaign-id 123456789 \\
        --share-urn "urn:li:share:7000000000000000000" \\
        --name "Creative v1 - depoimento Head RH"

Pra criar a share (post orgânico que vira sponsored), use a UI do Campaign
Manager OU a Posts API. A automação direta exige fluxo mais complexo.
"""

import click

from _client import post


@click.command()
@click.option("--campaign-id", required=True)
@click.option("--share-urn", required=True, help="URN da share/post a promover")
@click.option("--name", required=True, help="Nome interno do creative")
@click.option(
    "--status",
    type=click.Choice(["DRAFT", "ACTIVE", "PAUSED"]),
    default="DRAFT",
)
@click.option("--yes", is_flag=True)
def main(campaign_id, share_urn, name, status, yes):
    """Cria Creative referenciando uma share existente."""
    print(f"\nVai criar Creative:")
    print(f"  Nome: {name}")
    print(f"  Campaign: urn:li:sponsoredCampaign:{campaign_id}")
    print(f"  Share/Post: {share_urn}")
    print(f"  Status: {status}")

    if not yes:
        click.confirm("\nConfirmar?", abort=True)

    payload = {
        "campaign": f"urn:li:sponsoredCampaign:{campaign_id}",
        "status": status,
        "type": "SPONSORED_STATUS_UPDATE",
        "reference": share_urn,
        "name": name,
    }

    response = post("/creatives", payload)
    location = response.headers.get("Location", "")
    creative_id = location.split("/")[-1] if location else "(verifique no UI)"
    print(f"\nCreative criado:")
    print(f"  ID: {creative_id}")


if __name__ == "__main__":
    main()
