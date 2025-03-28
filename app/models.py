from django.db import models

class Department(models.Model):
    dept_id = models.AutoField(primary_key=True, unique=True)
    dept_name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0) 

    def __str__(self):
        return self.dept_name

    def has_linked_employees(self):
        """Check if there are any employees linked to this department"""
        return self.employee_set.exists()


    def reactivate(self):
        """Reactivate a deactivated department"""
        if not self.status:
            self.status = True
            self.save()
            return True
        return False

    class Meta:
        db_table = 'department'
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        employee_positions = ", ".join([emp.position for emp in self.employee_set.all() if emp.position]) if hasattr(self, 'employee_set') else ''
        return f"{self.role_name} ({employee_positions})" if employee_positions else self.role_name

    class Meta:
        db_table = 'roles'
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'

class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)  
    status = models.BooleanField(default=True)  # Indicates if the employee is active

    first_name = models.CharField(max_length=100)  
    username = models.CharField(max_length=100, null=True)  
    password = models.CharField(max_length=100, null=True)  
    last_name = models.CharField(max_length=100)  
    email = models.CharField(max_length=100, null=True)  
    mobile = models.CharField(max_length=100)  
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)  
    role_id = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, related_name='role_employees')  
    reporting_manager_id = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='reporting_employees')  
    position = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)  
    date_of_joining = models.DateField(null=True, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = 'employee'
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
