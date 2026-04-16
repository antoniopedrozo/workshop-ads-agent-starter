"""
Pausa ou retoma uma campanha, ad group ou ad.

Uso:
    python api/google-ads/pause_resume.py --action PAUSE --campaign-id 1234567890
    python api/google-ads/pause_resume.py --action RESUME --ad-group-id 9876543210
    python api/google-ads/pause_resume.py --action PAUSE --ad-id 5555555555 --ad-group-id 9876543210
"""

import click
from google.ads.googleads.errors import GoogleAdsException
from google.protobuf.field_mask_pb2 import FieldMask

from _client import (
    get_client,
    get_customer_id,
    handle_google_ads_error,
)


@click.command()
@click.option("--action", type=click.Choice(["PAUSE", "RESUME"], case_sensitive=False), required=True)
@click.option("--campaign-id", help="ID da campanha pra pausar/retomar")
@click.option("--ad-group-id", help="ID do ad group pra pausar/retomar")
@click.option("--ad-id", help="ID do ad pra pausar/retomar (precisa também --ad-group-id)")
@click.option("--yes", is_flag=True, help="Pula confirmação")
def main(action, campaign_id, ad_group_id, ad_id, yes):
    """Pausa ou retoma entidade."""
    targets = sum([bool(campaign_id), bool(ad_group_id and not ad_id), bool(ad_id)])
    if targets != 1:
        raise click.UsageError(
            "Use exatamente um: --campaign-id, --ad-group-id, OU --ad-id (com --ad-group-id)."
        )
    if ad_id and not ad_group_id:
        raise click.UsageError("--ad-id requer --ad-group-id também.")

    client = get_client()
    customer_id = get_customer_id()
    new_status = "PAUSED" if action.upper() == "PAUSE" else "ENABLED"

    target = (
        f"campaign {campaign_id}"
        if campaign_id
        else f"ad_group {ad_group_id}"
        if not ad_id
        else f"ad {ad_id}"
    )
    print(f"\nVai mudar status de {target} pra {new_status}.")
    if not yes:
        click.confirm("Confirmar?", abort=True)

    try:
        if campaign_id:
            service = client.get_service("CampaignService")
            op = client.get_type("CampaignOperation")
            op.update.resource_name = service.campaign_path(customer_id, campaign_id)
            op.update.status = client.enums.CampaignStatusEnum[new_status]
            client.copy_from(op.update_mask, FieldMask(paths=["status"]))
            response = service.mutate_campaigns(customer_id=customer_id, operations=[op])
        elif ad_group_id and not ad_id:
            service = client.get_service("AdGroupService")
            op = client.get_type("AdGroupOperation")
            op.update.resource_name = service.ad_group_path(customer_id, ad_group_id)
            op.update.status = client.enums.AdGroupStatusEnum[new_status]
            client.copy_from(op.update_mask, FieldMask(paths=["status"]))
            response = service.mutate_ad_groups(customer_id=customer_id, operations=[op])
        else:
            service = client.get_service("AdGroupAdService")
            op = client.get_type("AdGroupAdOperation")
            op.update.resource_name = service.ad_group_ad_path(customer_id, ad_group_id, ad_id)
            op.update.status = client.enums.AdGroupAdStatusEnum[new_status]
            client.copy_from(op.update_mask, FieldMask(paths=["status"]))
            response = service.mutate_ad_group_ads(customer_id=customer_id, operations=[op])

        print(f"OK. Resource: {response.results[0].resource_name}")

    except GoogleAdsException as ex:
        handle_google_ads_error(ex)


if __name__ == "__main__":
    main()
