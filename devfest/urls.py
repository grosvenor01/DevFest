"""
URL configuration for devfest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from devApp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/',register.as_view(),name="register"),
    path("api/login/", logine.as_view(),name="login"),
    path("api/machines/", machine_AddDelete.as_view(),name="machine_managment"),
    path("api/machines/<int:id>", machine_managment.as_view(),name="machine_managment"),
    path('api/tasks/', Task_managment.as_view(), name='task_managment'),
    path('api/current_tasks/', all_current_tasks, name='task_managment'),
    path('api/all_tasks_user/', all_tasks, name='task_managment'),
    path('api/tasks/<int:id>', Task_managment_user.as_view(), name='task_managment'),
    path('api/affect_task/<int:id>', task_affection.as_view(), name='task_affectaation'),
    path('api/Dashboard/', Production_overview, name='dashboard'),
    path('api/maintenance/', machine_Maintenance, name='dashboard'),
    path('callback/', callback_view, name='callback'),
]
