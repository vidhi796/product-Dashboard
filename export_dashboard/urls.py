from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('upload/', views.upload_excel, name='upload_excel'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('timeline/', views.timeline_view, name='timeline'),
    path('export-data/', views.export_data_json, name='export_data_json'),
    path('dashboard/index.html/', views.index_html, name='index_html'), 
    path('ports_json/', views.ports_json, name='ports_json'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
