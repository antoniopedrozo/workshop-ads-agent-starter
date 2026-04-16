"""
Cria um Ad usando Ad Set existente + creative (imagem ou vídeo).

Usa Single Image/Video Ad simples com link. Pra carousel, formatos avançados,
adapta o object_story_spec.

Uso (imagem):
    python api/meta-ads/create_ad.py \\
        --adset-id 12000000000 \\
        --name "Ad v1 - dor planilha" \\
        --page-id 123456789 \\
        --image-hash abc123def456 \\
        --primary-text "Sua planilha de clima já não dá conta?" \\
        --headline "Pulse direto no Slack" \\
        --description "+200 empresas, 92% de resposta" \\
        --link "https://acmerh.com.br/clima" \\
        --cta LEARN_MORE

Uso (vídeo):
    python api/meta-ads/create_ad.py \\
        --adset-id 12000000000 \\
        --name "Ad v1 - depoimento UGC" \\
        --page-id 123456789 \\
        --video-id 234567890 \\
        --image-hash abc123 \\
        --primary-text "..." --headline "..." --link "..." --cta LEARN_MORE

(vídeo precisa de uma image_hash pra thumbnail)
"""

import click
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adcreative import AdCreative

from _client import get_ad_account_id, init_api


@click.command()
@click.option("--adset-id", required=True)
@click.option("--name", required=True)
@click.option("--page-id", required=True, help="Facebook Page ID que vai patrocinar o ad")
@click.option("--image-hash", help="Hash da imagem (de upload_creative.py)")
@click.option("--video-id", help="ID do vídeo (de upload_creative.py)")
@click.option("--primary-text", required=True, help="Texto principal (até 125 chars recomendado)")
@click.option("--headline", required=True, help="Headline (até 40 chars)")
@click.option("--description", default="", help="Descrição (até 30 chars)")
@click.option("--link", required=True, help="URL de destino")
@click.option(
    "--cta",
    type=click.Choice(
        ["LEARN_MORE", "SIGN_UP", "DOWNLOAD", "CONTACT_US", "GET_QUOTE", "BOOK_NOW", "SUBSCRIBE"]
    ),
    default="LEARN_MORE",
)
@click.option("--instagram-actor-id", help="Instagram Account ID (opcional, pra ad também rodar no IG)")
@click.option("--status", type=click.Choice(["PAUSED", "ACTIVE"]), default="PAUSED")
@click.option("--yes", is_flag=True)
def main(
    adset_id, name, page_id, image_hash, video_id, primary_text, headline, description, link, cta,
    instagram_actor_id, status, yes
):
    """Cria Ad."""
    if not (image_hash or video_id):
        raise click.UsageError("Use --image-hash OU --video-id.")

    init_api()
    account = AdAccount(get_ad_account_id())

    print(f"\nVai criar Ad:")
    print(f"  Nome: {name}")
    print(f"  Ad Set: {adset_id}")
    print(f"  Page: {page_id}")
    if instagram_actor_id:
        print(f"  Instagram: {instagram_actor_id}")
    print(f"  Asset: {'image_hash=' + image_hash if image_hash else 'video_id=' + video_id}")
    print(f"  Primary text: {primary_text}")
    print(f"  Headline: {headline}")
    if description:
        print(f"  Description: {description}")
    print(f"  Link: {link}")
    print(f"  CTA: {cta}")
    print(f"  Status: {status}")

    if not yes:
        click.confirm("\nConfirmar?", abort=True)

    # Criativo
    if image_hash and not video_id:
        link_data = {
            "image_hash": image_hash,
            "link": link,
            "message": primary_text,
            "name": headline,
            "call_to_action": {"type": cta, "value": {"link": link}},
        }
        if description:
            link_data["description"] = description
        object_story_spec = {"page_id": page_id, "link_data": link_data}
    else:
        video_data = {
            "video_id": video_id,
            "image_hash": image_hash,
            "title": headline,
            "message": primary_text,
            "call_to_action": {"type": cta, "value": {"link": link}},
        }
        object_story_spec = {"page_id": page_id, "video_data": video_data}

    if instagram_actor_id:
        object_story_spec["instagram_actor_id"] = instagram_actor_id

    creative_params = {
        AdCreative.Field.name: f"{name} - Creative",
        AdCreative.Field.object_story_spec: object_story_spec,
    }
    creative = account.create_ad_creative(params=creative_params)
    print(f"\nCreative criado: {creative['id']}")

    ad_params = {
        Ad.Field.name: name,
        Ad.Field.adset_id: adset_id,
        Ad.Field.creative: {"creative_id": creative["id"]},
        Ad.Field.status: status,
    }
    ad = account.create_ad(params=ad_params)
    print(f"\nAd criado:")
    print(f"  ID: {ad['id']}")


if __name__ == "__main__":
    main()
