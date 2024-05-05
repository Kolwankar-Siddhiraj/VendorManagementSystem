from rest_framework.serializers import ModelSerializer
from vendor_portal.models import *


# Vendor model serializer
class VendorSerializer(ModelSerializer):

    class Meta:
        model = Vendor
        fields = '__all__'


# Vendor performance serializer
class VendorPerformanceMetricsSerializer(ModelSerializer):

    class Meta:
        model = Vendor
        fields = ('on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate')


# PurchaseOrder model serializer
class PurchaseOrderSerializer(ModelSerializer):

    class Meta:
        model = PurchaseOrder
        fields = '__all__'


# HistoricalPerformance model serializer
class HistoricalPerformanceSerializer(ModelSerializer):

    class Meta:
        model = HistoricalPerformance
        fields = '__all__'

