from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

class Exporter(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200, default='Not Provided')
    phone = models.CharField(max_length=50, default='Not Provided')
    contact_person = models.CharField(max_length=200, default='Not Provided')

    def __str__(self):
        return self.name

class Consignee(models.Model):
    name = models.CharField(max_length=200)
    address_line_1 = models.CharField(max_length=300, blank=True, null=True)
    address_line_2 = models.CharField(max_length=300, blank=True, null=True)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ExportRecord(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    port_code = models.CharField(max_length=50)
    shipping_bill_no = models.CharField(max_length=100)
    shipping_bill_date = models.DateField()
    iec = models.CharField(max_length=100)
    exporter = models.ForeignKey(Exporter, on_delete=models.SET_NULL, null=True)
    exporter_address = models.CharField(max_length=300)
    exporter_city_state = models.CharField(max_length=200)
    exporter_pin = models.CharField(max_length=20)
    destination_port = models.CharField(max_length=100)
    destination_country = models.CharField(max_length=100)
    invoice_no = models.CharField(max_length=100)
    ritc = models.CharField(max_length=20)
    item = models.CharField(max_length=300)
    quantity = models.FloatField()
    uqc = models.CharField(max_length=10)
    item_rate = models.FloatField()
    currency = models.CharField(max_length=10)
    fob = models.FloatField()
    cha_name = models.CharField(max_length=200)
    consignee = models.ForeignKey(Consignee, on_delete=models.SET_NULL, null=True, blank=True)
    leo_date = models.DateField(null=True, blank=True) 
    invoice_sr_no = models.IntegerField(null=True, blank=True)
    item_no = models.IntegerField(null=True, blank=True)
    drawback = models.FloatField(blank=True, null=True)
    
# Create your models here.
class EVChargingLocation(models.Model):
    station_name = models.CharField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    


    def __str__(self):
        return self.station_name

# --- SeaPort model for world sea ports ---
class SeaPort(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    country_code = models.CharField(max_length=10)
    port_code = models.CharField(max_length=10)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.name} ({self.country})"