from django.urls import path
from vendor_portal.views import *


urlpatterns = [
    path('admin/login/', AdminLogin.as_view(), name='admin-login'),

    # vendor apis
    path('vendors/', VendorView.as_view(), name='vendor-view'),
    path('vendor/<int:vendor_id>/', VendorActionView.as_view(), name='vendor-action-view'),
    path('vendor/<int:vendor_id>/performance/', VendorPerformanceView.as_view(), name='vendor-performance-view'),
    
    # purchase_order apis
    path('purchase_orders/', PurchaseOrderView.as_view(), name='purchase-order-view'),
    path('purchase_order/<int:po_id>/', PurchaseOrderActionView.as_view(), name='purchase-order-action-view'),
    path('purchase_order/<int:po_id>/acknowledge/', PurchaseOrderAcknowledgeView.as_view(), name='purchase-order-acknowledge-view'),
]

