from django.contrib import admin
from vendor_portal.models import *


# Register your models here.

admin.site.register(Vendor)
admin.site.register(PurchaseOrder)
admin.site.register(HistoricalPerformance)


