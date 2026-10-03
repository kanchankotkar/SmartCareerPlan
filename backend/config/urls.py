from django.contrib import admin
from django.urls import path, include


urlpatterns = [

    path(
        'admin/',
        admin.site.urls
    ),

    path(
        'api/accounts/',
        include('accounts.urls')
    ),
     path(
        'api/skills/',
        include('skills.urls')
    ),
    path(
        'api/careers/',
        include('careers.urls')
    ),

    path('api/learning/', 
         include('learning.urls')
    ),
    path(
    'api/analytics/',
    include('analytics.urls')
    ),

    path(
        'api/admin-management/',
        include('admin_management.urls')
    ),
    


]