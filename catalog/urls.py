from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('scheme-decribe/', views.scheme, name='scheme'),
    path('scheme-decribe/result/', views.result, name='result'),
    path('scheme-decribe/enter_number', views.enter_number, name='enter_number'),
    path('scheme-decribe/result/final', views.final, name='final')
]
