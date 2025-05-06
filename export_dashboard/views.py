from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from .forms import ExcelUploadForm
from .models import Product, Exporter, Consignee, ExportRecord, SeaPort
import pandas as pd
from io import BytesIO
import datetime
from django.http import JsonResponse

def dashboard_view(request):
    return render(request, 'export_dashboard/dash.html')

def timeline_view(request):
    return render(request, 'export_dashboard/timeline.html')

def index_html(request):
    context = {"data": "some value"}
    return render(request, 'export_dashboard/index.html', context),

def export_data_json(request):
    data = ExportRecord.objects.select_related('exporter', 'product').values(
        'shipping_bill_date',
        'exporter__name',
        'destination_country',
        'item',
        'product__name',
        'quantity',
        'item_rate',
        'fob',  # FOB in INR already
    )

    data_list = []
    for item in data:
        data_list.append({
            'shipping_bill_date': item['shipping_bill_date'],
            'exporter': item['exporter__name'] or 'Not Provided',
            'destination_country': item['destination_country'] or 'Not Provided',
            'item': item['item'] or 'Not Provided',
            'product': item['product__name'] or 'Not Provided',
            'quantity': item['quantity'] or 0,
            'rate_per_unit': item['item_rate'] or 0,
            'fob': round(item['fob'] or 0, 2),
        })

    return JsonResponse(data_list, safe=False)

@staff_member_required
def upload_excel(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            product_name = form.cleaned_data['product']
            excel_file = request.FILES['excel_file']

            product, created = Product.objects.get_or_create(name=product_name)

            df = pd.read_excel(BytesIO(excel_file.read()))
            df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

            # Data Cleaning
            df = df[~df['uqc'].isin(['PCS', 'NOS'])]
            df['quantity'] = df.apply(lambda row: row['quantity'] / 1000 if row['uqc'] == 'KGS' else row['quantity'], axis=1)
            df['item_rate'] = df.apply(lambda row: row['item_rate'] * 1000 if row['uqc'] == 'KGS' else row['item_rate'], axis=1)
            df['uqc'] = df['uqc'].apply(lambda x: 'MTS' if x == 'KGS' else x)
            df['consignee'] = df['consignee'].apply(lambda x: 'NOT PROVIDED' if 'TO ORDER' in str(x).upper() else x)

            # Date Conversion Helper
            def safe_parse_date(value):
                if pd.isnull(value):
                    return None
                if isinstance(value, str):
                    return pd.to_datetime(value).date()
                if isinstance(value, pd.Timestamp):
                    return value.date()
                if isinstance(value, datetime.date):
                    return value
                return None

            for _, row in df.iterrows():
                exporter, _ = Exporter.objects.get_or_create(
                    name=row['exporter'],
                    defaults={
                        'email': row.get('exporter_mail', 'Not Provided'),
                        'phone': row.get('exporter_phone', 'Not Provided'),
                        'contact_person': row.get('exporter_contact_person_1', 'Not Provided'),
                    }
                )

                consignee_obj = None
                if row['consignee'] != 'NOT PROVIDED':
                    consignee_obj, _ = Consignee.objects.get_or_create(
                        name=row['consignee'],
                        defaults={
                            'address_line_1': row.get('consignee_add_1', ''),
                            'address_line_2': row.get('consignee_add_2', ''),
                            'country': row.get('consignee_country', ''),
                        }
                    )

                invoice_sr_no_value = row['invoice_sr_no']
                item_no_value = row['item_no']

                # Replace NaN with 0 or a default integer
                if pd.isnull(invoice_sr_no_value):
                    invoice_sr_no_value = 0
                if pd.isnull(item_no_value):
                    item_no_value = 0

                ExportRecord.objects.create(
                    product=product,
                    location=row['location'],
                    port_code=row['cush'],
                    shipping_bill_no=row['sbno'],
                    shipping_bill_date=safe_parse_date(row['sbdt']),
                    iec=row['iec'],
                    exporter=exporter,
                    exporter_address=row['exporter_address'],
                    exporter_city_state=row['exporter_city_state'],
                    exporter_pin=row['exporter_pin'],
                    destination_port=row['port_cd'],
                    destination_country=row['country'],
                    invoice_no=row['invoice_no'],
                    ritc=row['ritc'],
                    item=row['item'],
                    quantity=row['quantity'],
                    uqc=row['uqc'],
                    item_rate=row['item_rate'],
                    currency=row['currency'],
                    fob=row['fob'],
                    cha_name=row['cha_name'],
                    consignee=consignee_obj,
                    leo_date=safe_parse_date(row['leo_date']),
                    invoice_sr_no=invoice_sr_no_value,
                    item_no=item_no_value,
                    drawback=row.get('drawback', 0),
                )

            return redirect('admin:index')
    else:
        form = ExcelUploadForm()

    return render(request, 'export_dashboard/upload_excel.html', {'form': form})

def ports_json(request):
    ports = list(SeaPort.objects.values())
    return JsonResponse(ports, safe=False)
