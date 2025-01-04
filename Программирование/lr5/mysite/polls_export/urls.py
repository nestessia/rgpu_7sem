from django.urls import path
from . import views

app_name = 'polls_export'
urlpatterns = [
    path('', views.ExportDataAPI.as_view(), name='export-data'),
]
