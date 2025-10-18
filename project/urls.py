from django.urls import path

from project import views

app_name = 'project'

urlpatterns = [    
    path('', views.project_home_page, name='home-page'),
    path('create', views.project_create, name='create'),

    path('categories', views.categories_home_page, name='categories-home-page'),
    path('categories/create', views.categories_create, name='categories-create'),
]