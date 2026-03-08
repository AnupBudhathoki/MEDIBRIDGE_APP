from django.urls import path
from . import views

urlpatterns = [
    path('pay/esewa/', views.start_esewa_payment, name='start_esewa_payment'),
    path('esewa/success/', views.success_esewa, name='success_esewa'),
    path('esewa/failure/', views.failure_esewa, name='failure_esewa'),
]
