from django.contrib import admin
from .models import Department, Employee, Role

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('role_name', 'description', 'status')
    list_filter = ('status',)
    search_fields = ('role_name',)
    ordering = ('role_name',)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('dept_id', 'dept_name', 'status')
    list_filter = ('status',)
    search_fields = ('dept_name',)
    ordering = ('dept_name',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'full_name', 'department', 'created_at', 'updated_at')
    list_filter = ('department',)
    search_fields = ('first_name', 'last_name')
    ordering = ('last_name', 'first_name')
    readonly_fields = ('created_at', 'updated_at')
    
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Full Name'
