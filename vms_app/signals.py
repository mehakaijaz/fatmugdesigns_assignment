from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PurchaseOrder, HistoricalPerformance
from .views import update_vendor_metrics

@receiver(post_save, sender=PurchaseOrder)
def purchase_order_post_save(sender, instance, created, **kwargs):
    update_vendor_metrics(sender, instance, created, **kwargs)

    if instance.status == 'completed':
        # Create a historical performance record
        HistoricalPerformance.objects.create(
            vendor=instance.vendor,
            date=instance.delivery_date,
            on_time_delivery_rate=instance.vendor.on_time_delivery_rate,
            quality_rating_avg=instance.vendor.quality_rating_avg,
            average_response_time=instance.vendor.average_response_time,
            fulfillment_rate=instance.vendor.fulfillment_rate,
        )
        