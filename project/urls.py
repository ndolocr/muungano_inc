from django.urls import path

from project import views

app_name = 'project'

urlpatterns = [    
    path('', views.view_all, name='view-all'),
    path('create', views.project_create, name='create'),
    path('view/<int:id>', views.view_project, name='view-project'),

    path('stages', views.stages_view_all, name='stages-view-all'),
    path('stages/create', views.stages_create, name='stages-create'),

    path('activity/create', views.activity_create, name='activity-create'),

    path('categories', views.categories_home_page, name='categories-home-page'),
    path('categories/create', views.categories_create, name='categories-create'),
]