from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView
from .views import CustomPasswordResetConfirmView, CustomPasswordResetCompleteView, CustomPasswordResetView

app_name = 'departments'

urlpatterns = [
    path('', views.department_dashboard, name='dashboard'),
    path('accounts/password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('create/', views.create_department, name='create'),
    path('update/<int:dept_id>/', views.update_department, name='update'),
    path('delete/<int:dept_id>/', views.delete_department, name='delete'),
    path('view_employees/<int:dept_id>/', views.view_department_employees, name='view_employees'),
    path('reactivate/<int:dept_id>/', views.reactivate_department, name='reactivate'),
    path('search/', views.search_department, name='search'),
    path('reassign/<int:dept_id>/', views.reassign_employees, name='reassign'),
]
