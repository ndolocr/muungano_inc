from django.urls import path

from project import views

app_name = 'project'

urlpatterns = [    
    path('', views.home_page, name='home-page'),
    path('create', views.create, name='create'),
]