from django.urls import path
from . import views

app_name = 'departments'

urlpatterns = [
    path('', views.department_dashboard, name='dashboard'),
    path('create/', views.create_department, name='create'),
    path('update/<int:dept_id>/', views.update_department, name='update'),
    path('delete/<int:dept_id>/', views.delete_department, name='delete'),
    path('search/', views.search_department, name='search'),
    path('reassign/<int:dept_id>/', views.reassign_employees, name='reassign'),
]
