from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ha_home/', views.ha_home, name='ha_home'),
    path('doctors_list/', views.doctors_list, name='doctors_list'),
    path('appointment/<int:doctor_id>/', views.appointment_page, name='appoinment_page'),
]
