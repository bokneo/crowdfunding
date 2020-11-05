"""crowdfunding URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.adminPortal, name = "adminPortal"),
    path('deleteuser',views.deluser, name = "deluser"),   
    path('user',views.userPortal, name = "userPortal"),
    path('project',views.projectPortal, name = "projectPortal"),
    path('deleteproject',views.delproject, name = "delproject"),
    path('<str:name>/project', views.editdetail, name = "editdetail"),
    path('userdetail', views.userdetail, name = "userdetail"),
    path('investment', views.investment, name = "investment"),
    path('deleteinvest',views.delinvest, name = "delinvest"),
    path('editinvest',views.editinvest, name = "editinvest"),
    path('editproject',views.editproject, name = "editproject"),
    path('edituser',views.edituser, name = "edituser"),
    path('profile',views.profile, name = "profile"),
]
