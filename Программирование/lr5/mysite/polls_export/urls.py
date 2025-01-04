from django.urls import path
from . import views

app_name = 'polls_export'
urlpatterns = [
    path('', views.ExportDataAPI.as_view(), name='export-data'),
    path('.json', views.ExportDataAPI.as_view(), name='export-data-json'),
    path('.csv', views.ExportDataAPI.as_view(), name='export-data-csv'),
]
