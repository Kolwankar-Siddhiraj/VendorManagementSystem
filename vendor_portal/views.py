from django.contrib.auth.models import auth
from django.db import transaction
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Avg, F, ExpressionWrapper, fields

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from vendor_portal.helpers import *
from vendor_portal.models import *
from vendor_portal.serializers import *

from datetime import datetime, timedelta





# support functions


def calculate_avg_response_time(purchase_orders):

    purchase_orders = purchase_orders.annotate(
        time_difference=ExpressionWrapper(
            F('acknowledgment_date') - F('issue_date'),
            output_field=fields.DurationField()
        )
    )

    purchase_orders = purchase_orders.exclude(time_difference=None)

    average_time_difference = purchase_orders.aggregate(
        avg_time_difference=Avg('time_difference')
    )['avg_time_difference']

    print(f"Average Time Difference: {average_time_difference}")

    return average_time_difference.total_seconds() / 3600


def calculate_on_time_delivery_rate(vendor_id):

    purchase_orders = PurchaseOrder.objects.filter(vendor__id=vendor_id, status="completed").order_by('id')
    on_time_delivery_rate = len(purchase_orders.filter(is_delivered_on_time=True)) / len(purchase_orders)

    print("on_time_delivery_rate :: ", on_time_delivery_rate)
    Vendor.objects.filter(id=vendor_id).update(on_time_delivery_rate=on_time_delivery_rate)


def calculate_quality_rating_avg(vendor_id):

    purchase_orders = PurchaseOrder.objects.filter(vendor__id=vendor_id, status="completed").exclude(quality_rating=None).order_by('id')
    quality_rating_avg = purchase_orders.aggregate(Avg('quality_rating'))['quality_rating__avg']

    print("quality_rating_avg :: ", quality_rating_avg)
    Vendor.objects.filter(id=vendor_id).update(quality_rating_avg=quality_rating_avg)


def calculate_fulfillment_rate(vendor_id):

    purchase_orders = PurchaseOrder.objects.filter(vendor__id=vendor_id).order_by('id')
    fulfillment_rate = len(purchase_orders.filter(status="completed")) / len(purchase_orders)

    print("fulfillment_rate :: ", fulfillment_rate)
    Vendor.objects.filter(id=vendor_id).update(fulfillment_rate=fulfillment_rate)





# api views


class AdminLogin(APIView):

    permission_classes = []
    authentication_classes = []

    @transaction.atomic
    def post(self, request):

        rd = request.data
        print("rd :: ", rd)

        admin_user = auth.authenticate(username=rd['username'], password=rd['password'])
        print("admin_user ::",admin_user)

        if admin_user is not None:
            token = RefreshToken.for_user(admin_user)

            return Response({"success": True, "message": "Admin User login successfully !",
                            "authToken": {
                                'type': 'Bearer',
                                'access': str(token.access_token),
                                'refresh': str(token),
                            }})
        else:
            return Response({"success": False, "message": "Oppps! Creadentials did not matched!"})


class VendorView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @transaction.atomic
    def get(self, request):

        vendors = Vendor.objects.filter().order_by('id')
        data = VendorSerializer(vendors, many=True).data

        return Response({"success": True, "message": "All vendors fetched!", "data": data})


    @transaction.atomic
    def post(self, request):

        rd = request.data
        print("rd :: ", rd)

        new_vendor = VendorSerializer(data=rd)

        if new_vendor.is_valid():
            new_vendor.save()
            return Response({"success": True, "message": "Vendor created!", "data": new_vendor.data})

        else:
            print("Vendor creation error :: ", new_vendor.errors)
            return Response({"success": False, "message": new_vendor.errors})


class VendorActionView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @transaction.atomic
    def get(self, request, vendor_id):

        vendor = Vendor.objects.filter(id=vendor_id).first()
        if vendor == None:
            return Response({"success": False, "message": "Vendor not found!"})

        data = VendorSerializer(vendor).data

        return Response({"success": True, "message": f"Vendor {vendor.name} fetched!", "data": data})


    @transaction.atomic
    def put(self, request, vendor_id):

        rd = request.data
        print("rd :: ", rd)

        vendor = Vendor.objects.filter(id=vendor_id).first()
        if vendor == None:
            return Response({"success": False, "message": "Vendor not found!"})

        updated_vendor = VendorSerializer(instance=vendor, data=rd, partial=True)

        if updated_vendor.is_valid():
            updated_vendor.save()
            return Response({"success": True, "message": "Vendor updated!", "data": updated_vendor.data})

        else:
            print("Vendor updation error :: ", updated_vendor.errors)
            return Response({"success": False, "message": updated_vendor.errors})


    @transaction.atomic
    def delete(self, request, vendor_id):

        vendor = Vendor.objects.filter(id=vendor_id).first()
        if vendor == None:
            return Response({"success": False, "message": "Vendor not found!"})

        vendor.delete()
        return Response({"success": True, "message": "Vendor deleted!"})


class VendorPerformanceView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @transaction.atomic
    def get(self, request, vendor_id):

        vendor = Vendor.objects.filter(id=vendor_id).first()
        if vendor == None:
            return Response({"success": False, "message": "Vendor not found!"})

        data = VendorPerformanceMetricsSerializer(vendor).data

        HistoricalPerformance.objects.create(vendor=vendor, **data)

        return Response({"success": True, "message": f"Vendor '{vendor.name}' performance metrics!", "data": data})


class PurchaseOrderView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @transaction.atomic
    def get(self, request):

        vendor_id = request.GET.get('vendor_id', None)

        if vendor_id == None:
            return Response({"success": False, "message": "Vendor id required!"})

        purchase_orders = PurchaseOrder.objects.filter(vendor__id=vendor_id).order_by('id')
        data = PurchaseOrderSerializer(purchase_orders, many=True).data

        return Response({"success": True, "message": "All Purchase orders fetched!", "data": data})


    @transaction.atomic
    def post(self, request):

        rd = request.data
        print("rd :: ", rd)

        rd['po_number'] = generate_po_number(vendor_id=rd['vendor'])
        rd['delivery_date'] = format_date(sdate=rd['delivery_date'])

        new_purchase_order = PurchaseOrderSerializer(data=rd)

        if new_purchase_order.is_valid():
            new_purchase_order.save()
            return Response({"success": True, "message": "Purchase order created!", "data": new_purchase_order.data})

        else:
            print("Purchase order creation error :: ", new_purchase_order.errors)
            return Response({"success": False, "message": new_purchase_order.errors})


class PurchaseOrderActionView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @transaction.atomic
    def get(self, request, po_id):

        purchase_order = PurchaseOrder.objects.filter(id=po_id).first()
        if purchase_order == None:
            return Response({"success": False, "message": "Purchase order not found!"})

        data = PurchaseOrderSerializer(purchase_order).data

        return Response({"success": True, "message": f"Purchase order {purchase_order.po_number} fetched!", "data": data})


    @transaction.atomic
    def put(self, request, po_id):

        rd = request.data
        print("rd :: ", rd)

        purchase_order = PurchaseOrder.objects.filter(id=po_id).first()
        if purchase_order == None:
            return Response({"success": False, "message": "Purchase order not found!"})

        updated_purchase_order = PurchaseOrderSerializer(instance=purchase_order, data=rd, partial=True)

        if updated_purchase_order.is_valid():
            updated_purchase_order.save()

            if purchase_order.status == "completed":
                purchase_order.is_delivered_on_time = True if purchase_order.delivery_date > timezone.now() else False
                purchase_order.delivery_date = timezone.now()
                purchase_order.save()

            # update on time delivery rate of vendor
            calculate_on_time_delivery_rate(vendor_id=purchase_order.vendor.id)

            # update quality rating average of vendor
            if 'quality_rating' in rd:
                calculate_quality_rating_avg(vendor_id=purchase_order.vendor.id)
            
            # update fulfillment rate of vendor
            if 'status' in rd:
                calculate_fulfillment_rate(vendor_id=purchase_order.vendor.id)

            return Response({"success": True, "message": "Purchase order updated!", "data": updated_purchase_order.data})

        else:
            print("Purchase order updation error :: ", updated_purchase_order.errors)
            return Response({"success": False, "message": updated_purchase_order.errors})


    @transaction.atomic
    def delete(self, request, po_id):

        purchase_order = PurchaseOrder.objects.filter(id=po_id).first()
        if purchase_order == None:
            return Response({"success": False, "message": "Purchase order not found!"})

        purchase_order.delete()
        return Response({"success": True, "message": "Purchase order deleted!"})


class PurchaseOrderAcknowledgeView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @transaction.atomic
    def post(self, request, po_id):

        rd = request.data
        print("rd :: ", rd)

        purchase_order = PurchaseOrder.objects.filter(id=po_id).first()
        if purchase_order == None:
            return Response({"success": False, "message": "Purchase order not found!"})
        
        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.save()

        vendor_purchase_orders = PurchaseOrder.objects.filter(vendor__id=purchase_order.vendor.id).order_by('id')
        print("vendor_purchase_orders :: ", vendor_purchase_orders)
        avg_resps_time = calculate_avg_response_time(purchase_orders=vendor_purchase_orders)

        # update average response time of vendor
        Vendor.objects.filter(id=purchase_order.vendor.id).update(average_response_time=avg_resps_time)

        return Response({"success": True, "message": "Purchase order acknowledged!"})






