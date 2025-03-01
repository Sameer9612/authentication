from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth import views as auth_views


app_name = 'departments'

urlpatterns = [
    path('', views.department_dashboard, name='dashboard'),
    path('admin/password_reset/', auth_views.PasswordResetView.as_view(), name='admin_password_reset'),
    path('admin/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='admin_password_reset_done'),
    path('admin/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='admin_password_reset_confirm'),
    path('admin/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='admin_password_reset_complete'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),


    path('create/', views.create_department, name='create'),
    path('update/<int:dept_id>/', views.update_department, name='update'),
    path('delete/<int:dept_id>/', views.delete_department, name='delete'),
    path('view_employees/<int:dept_id>/', views.view_department_employees, name='view_employees'),
    path('reactivate/<int:dept_id>/', views.reactivate_department, name='reactivate'),
    path('search/', views.search_department, name='search'),
    path('reassign/<int:dept_id>/', views.reassign_employees, name='reassign'),
]
