from django.core.management.base import BaseCommand
from export_dashboard.models import Product, Exporter, ExportRecord
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Adds sample export data for testing'

    def handle(self, *args, **kwargs):
        # Create a sample product
        product, _ = Product.objects.get_or_create(name="Chickpea")

        # Create sample exporters
        exporters = [
            Exporter.objects.get_or_create(
                name=f"Exporter {i}",
                email=f"exporter{i}@example.com",
                phone=f"123456789{i}",
                contact_person=f"Contact Person {i}"
            )[0] for i in range(1, 6)
        ]

        # Sample countries and ports
        countries_ports = [
            ("USA", "New York", "NYC"),
            ("UK", "London", "LON"),
            ("UAE", "Dubai", "DXB"),
            ("Singapore", "Singapore", "SIN"),
            ("Australia", "Sydney", "SYD"),
            ("Japan", "Tokyo", "TYO"),
            ("Germany", "Hamburg", "HAM"),
            ("France", "Marseille", "MRS"),
            ("Netherlands", "Rotterdam", "RTM"),
            ("China", "Shanghai", "SHA")
        ]

        # Generate data for the last 30 days
        start_date = datetime.now() - timedelta(days=30)
        
        for i in range(30):
            current_date = start_date + timedelta(days=i)
            
            # Create 2-5 records per day
            for _ in range(random.randint(2, 5)):
                country, port, port_code = random.choice(countries_ports)
                exporter = random.choice(exporters)
                quantity = random.uniform(100, 1000)
                rate = random.uniform(500, 1000)
                
                ExportRecord.objects.create(
                    product=product,
                    location=port,
                    port_code=port_code,
                    shipping_bill_no=f"SB{current_date.strftime('%Y%m%d')}{random.randint(1000, 9999)}",
                    shipping_bill_date=current_date.date(),
                    iec=f"IEC{random.randint(100000, 999999)}",
                    exporter=exporter,
                    exporter_address=f"Address {random.randint(1, 100)}",
                    exporter_city_state=f"City {random.randint(1, 50)}",
                    exporter_pin=f"{random.randint(100000, 999999)}",
                    destination_port=port,
                    destination_country=country,
                    invoice_no=f"INV{random.randint(10000, 99999)}",
                    ritc=f"RITC{random.randint(1000, 9999)}",
                    item="Chickpea",
                    quantity=quantity,
                    uqc="MTS",
                    item_rate=rate,
                    currency="USD",
                    fob=quantity * rate,
                    cha_name=f"CHA {random.randint(1, 10)}",
                    leo_date=current_date.date(),
                    invoice_sr_no=random.randint(1, 100),
                    item_no=random.randint(1, 50)
                )

        self.stdout.write(self.style.SUCCESS('Successfully added sample data')) 