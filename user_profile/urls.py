from . import views
from django.urls import path

app_name = 'profile'

urlpatterns = [
    
    path('delete_account/', views.delete_account, name='deleteaccount'),
    path('edit/', views.edit_profile, name='edit'),
    path('', views.profile_view, name='profile'),
]