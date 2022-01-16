from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('category/', views.choice_category, name='choice_category'),
    path('category/numbers', views.enter_number, name='enter_number'),
    path('category/numbers/models', views.select_models, name='select_models'),
    path('category/result/final', views.final, name='final')
]
