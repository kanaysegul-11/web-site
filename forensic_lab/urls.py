from django.urls import path
from . import views

app_name = 'forensic_lab'

urlpatterns = [
    path('', views.tool_list, name='tool_list'),
    path('<slug:slug>/', views.tool_detail, name='tool_detail'), 
   
]