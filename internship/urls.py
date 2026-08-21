from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    #path("admin/dashboard/",include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('index', views.index, name='index'),
    path('', include('accounts.urls')),
    path('add/', views.add_page, name='add_page'),

    path('CRUD_post', views.CRUD_post, name='CRUD_post'),
    path('CRUD_applicant', views.CRUD_applicant, name='CRUD_applicant'),
    path('CRUD_org', views.CRUD_org, name='CRUD_org'),
    path('CRUD_application', views.CRUD_application, name='CRUD_application'),

]
