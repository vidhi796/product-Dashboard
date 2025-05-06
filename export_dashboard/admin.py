from django.contrib import admin
from .models import Product, Exporter, Consignee, ExportRecord

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Exporter)
class ExporterAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'contact_person')

@admin.register(Consignee)
class ConsigneeAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')

@admin.register(ExportRecord)
class ExportRecordAdmin(admin.ModelAdmin):
    list_display = ('product', 'exporter', 'destination_country', 'shipping_bill_date', 'item_rate', 'quantity', 'uqc' )
    list_filter = ('product', 'destination_country')
