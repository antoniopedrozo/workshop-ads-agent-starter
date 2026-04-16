"""
Faz upload de imagem ou vídeo pra biblioteca de creative do Meta.

Imagem retorna `image_hash` (string). Vídeo retorna `video_id`.
Use esses identificadores como input em `create_ad.py`.

Uso:
    python api/meta-ads/upload_creative.py --image path/to/image.jpg
    python api/meta-ads/upload_creative.py --video path/to/video.mp4
"""

import sys
from pathlib import Path

import click
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adimage import AdImage
from facebook_business.adobjects.advideo import AdVideo

from _client import get_ad_account_id, init_api


@click.command()
@click.option("--image", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--video", type=click.Path(exists=True, dir_okay=False, path_type=Path))
def main(image, video):
    """Sobe imagem ou vídeo."""
    if not (image or video):
        raise click.UsageError("Use --image OU --video.")
    if image and video:
        raise click.UsageError("Use só um: --image OU --video.")

    init_api()
    account = AdAccount(get_ad_account_id())

    if image:
        print(f"Subindo imagem: {image}")
        ad_image = AdImage(parent_id=account["id"])
        ad_image[AdImage.Field.filename] = str(image)
        ad_image.remote_create()
        print(f"\nImagem subida.")
        print(f"  image_hash: {ad_image['hash']}")
        print(f"\nUse no create_ad.py: --image-hash {ad_image['hash']}")
    else:
        print(f"Subindo vídeo: {video}")
        ad_video = AdVideo(parent_id=account["id"])
        ad_video[AdVideo.Field.filepath] = str(video)
        ad_video.remote_create()
        print(f"\nVídeo subido.")
        print(f"  video_id: {ad_video['id']}")
        print(f"\nUse no create_ad.py: --video-id {ad_video['id']}")
        print(
            "\nNota: o Meta processa o vídeo em background. Espere ~1-3 min antes de criar o ad."
        )


if __name__ == "__main__":
    main()
