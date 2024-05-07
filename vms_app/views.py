
from django.shortcuts import render
from django.db import models
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer
from django.db.models import Avg  
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class VendorListCreateView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class PurchaseOrderListCreateView(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class PurchaseOrderRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class HistoricalPerformanceListCreateView(generics.ListCreateAPIView):
    queryset = HistoricalPerformance.objects.all()
    serializer_class = HistoricalPerformanceSerializer

class HistoricalPerformanceRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HistoricalPerformance.objects.all()
    serializer_class = HistoricalPerformanceSerializer

class PurchaseOrderAcknowledgeView(generics.UpdateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def perform_update(self, serializer):
        serializer.save(acknowledgment_date=timezone.now())
        instance = serializer.instance
        instance.vendor.average_response_time = calculate_average_response_time(instance.vendor)
        instance.vendor.save()

@receiver(post_save, sender=PurchaseOrder)
def update_vendor_metrics(sender, instance, created, **kwargs):
    if created or instance.status == 'completed':
        instance.vendor.on_time_delivery_rate = calculate_on_time_delivery_rate(instance.vendor)
        instance.vendor.quality_rating_avg = calculate_quality_rating_avg(instance.vendor)
        instance.vendor.average_response_time = calculate_average_response_time(instance.vendor)
        instance.vendor.fulfillment_rate = calculate_fulfillment_rate(instance.vendor)
        instance.vendor.save()

def calculate_on_time_delivery_rate(vendor):
    completed_orders = vendor.purchaseorder_set.filter(status='completed')
    on_time_deliveries = completed_orders.filter(delivery_date__lte=timezone.now())
    return (on_time_deliveries.count() / completed_orders.count()) * 100 if completed_orders.count() > 0 else 0.0

def calculate_quality_rating_avg(vendor):
    completed_orders = vendor.purchaseorder_set.filter(status='completed', quality_rating__isnull=False)
    return completed_orders.aggregate(avg_quality_rating=models.Avg('quality_rating'))['avg_quality_rating'] or 0.0

def calculate_average_response_time(vendor):
    acknowledged_orders = vendor.purchaseorder_set.filter(acknowledgment_date__isnull=False)
    response_times = [(po.acknowledgment_date - po.issue_date).seconds for po in acknowledged_orders]
    return sum(response_times) / len(response_times) if len(response_times) > 0 else 0.0

def calculate_fulfillment_rate(vendor):
    completed_orders = vendor.purchaseorder_set.filter(status='completed')
    successful_fulfillments = completed_orders.filter(issue_date__isnull=False, acknowledgment_date__isnull=False)
    return (successful_fulfillments.count() / completed_orders.count()) * 100 if completed_orders.count() > 0 else 0.0
