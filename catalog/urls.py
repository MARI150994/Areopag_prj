from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.user_profile, name='user_profile'),
    path('create_project/', views.CreateProject.as_view(), name='create_project'),
    path('projects/', views.ProjectsListUser.as_view(), name='projects'),
    path('all-projects/', views.ProjectsListAll.as_view(), name='projects_all'),
    path('project/<str:slug>/', views.ProjectDetail.as_view(), name='project_detail'),
    path('project/<str:slug>/category', views.select_category, name='select_category'),
    path('project/<str:slug>/numbers', views.count_category, name='count_category'),
    path('project/<str:slug>/models', views.SelectModel.as_view(), name='select_models'),
    path('project/<str:slug>/scheme', views.CreateScheme.as_view(), name='create_scheme'),
]
