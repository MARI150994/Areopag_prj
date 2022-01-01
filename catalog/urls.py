from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('scheme-decribe/', views.scheme, name='scheme'),
    path('scheme-decribe/result/', views.result, name='result')
]
