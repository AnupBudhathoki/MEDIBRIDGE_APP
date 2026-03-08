from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('log_in/', views.log_in, name='log_in'),
    path('pat_profile/', views.pat_profile, name='pat_profile'),
    path('ha_profile/', views.ha_profile, name='ha_profile'),
    path('log_out/', views.log_out, name='log_out'),
    path('add_slot/', views.add_slot, name='add_slot'),
    path('remove_slot/', views.remove_slot, name='remove_slot'),
    path('health_status/', views.health_status, name='health_status'),
    path('view_appointment/', views.view_appointment, name='view_appoinment'),
]
