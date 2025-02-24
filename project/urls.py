"""
URL configuration for project project.

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
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from app import views







urlpatterns = [
    path('', RedirectView.as_view(url='departments/')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),


    # Department URLs
    path('departments/', include('app.urls')),
    path('reactivate/<int:dept_id>/', views.reactivate_department, name='reactivate_department'),




    # Employee URLs
    path('employees/', views.employee_dashboard, name='employee_dashboard'),
    path('employees/create/', views.create_employee, name='create_employee'),
    path('employees/update/<int:emp_id>/', views.update_employee, name='update_employee'),
    path('employees/delete/<int:emp_id>/', views.delete_employee, name='delete_employee'),

]
