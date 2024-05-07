
from django.urls import path
from .views import (
    VendorListCreateView,
    VendorRetrieveUpdateDeleteView,
    PurchaseOrderListCreateView,
    PurchaseOrderRetrieveUpdateDeleteView,
    HistoricalPerformanceListCreateView,
    HistoricalPerformanceRetrieveUpdateDeleteView,
    PurchaseOrderAcknowledgeView,

)

urlpatterns = [
    path('vendors/', VendorListCreateView.as_view(), name='vendor-list-create'),
    path('vendors/<int:pk>/', VendorRetrieveUpdateDeleteView.as_view(), name='vendor-retrieve-update-delete'),
    path('purchase_orders/', PurchaseOrderListCreateView.as_view(), name='purchase-order-list-create'),
    path('purchase_orders/<int:pk>/', PurchaseOrderRetrieveUpdateDeleteView.as_view(), name='purchase-order-retrieve-update-delete'),
    path('historical_performance/', HistoricalPerformanceListCreateView.as_view(), name='historical-performance-list-create'),
    path('historical_performance/<int:pk>/', HistoricalPerformanceRetrieveUpdateDeleteView.as_view(), name='historical-performance-retrieve-update-delete'),
    path('purchase_orders/<int:pk>/acknowledge/', PurchaseOrderAcknowledgeView.as_view(), name='purchase-order-acknowledge'),

]
