from . import views
from django.urls import path, include

app_name = 'appointments'

urlpatterns = [
    path('create/', views.appt_create, name='create'),
    path('', views.ApptList.as_view(), name='home'),
    path('appointments/<id>/', views.appt_detail, name='detail'),
    path('appointments/<id>/edit/', views.appt_edit, name='edit'),
    ]