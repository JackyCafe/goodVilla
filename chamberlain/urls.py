"""
URL configuration for goodVilla project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include

from chamberlain import views
from django.contrib.auth import views as auth_views

app_name = 'chamberlain'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), {'next_page': '/'}, name='logout'),
    path('user_login/', views.user_login, name='user_login'),
    path('register/', views.register, name='register'),
    path('attendance/', views.attendance_view, name='attendance'),
    path('major/', views.major, name='major'),
    path('detail/<int:id>/', views.detail, name='detail'),
    path('task_record/<int:id>', views.task_record, name='task_record'),
    path('task_end/<int:id>', views.task_end, name='task_end'),
    path('report/',views.report,name='report'),
    path('update_record/<int:id>', views.update_record, name='update_record'),

]
