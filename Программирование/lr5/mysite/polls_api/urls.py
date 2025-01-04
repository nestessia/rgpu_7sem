from django.urls import path
from . import views

app_name = 'polls_api'
urlpatterns = [
    path('', views.QuestionListAPI.as_view(), name='question-list-api'),
    path('<int:pk>/', views.QuestionDetailAPI.as_view(), name='question-detail-api'),
]
