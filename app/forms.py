from django import forms
from .models import Department, Employee, Role

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['dept_name', 'description']

class RoleForm(forms.ModelForm):
    POSITION_CHOICES = [
        ('', 'Select a position'),
        ('Accountant', 'Accountant'),
        ('Analyst', 'Analyst'),
        ('Developer', 'Developer'),
        ('Designer', 'Designer'),
        ('Engineer', 'Engineer'),
        ('Manager', 'Manager'),
        ('Specialist', 'Specialist'),
        ('Technician', 'Technician'),
    ]
    
    position = forms.ChoiceField(choices=POSITION_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    ROLE_CHOICES = [
        ('', 'Select a position'),
        ('Accountant', 'Accountant'),
        ('Analyst', 'Analyst'),
        ('Developer', 'Developer'),
        ('Designer', 'Designer'),
        ('Engineer', 'Engineer'),
        ('Manager', 'Manager'),
        ('Specialist', 'Specialist'),
        ('Technician', 'Technician'),
    ]
    
    role_name = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Role
        fields = ['role_name', 'position', 'description'] 

        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'role_name': forms.Select(attrs={'class': 'form-control'}),
            'position': forms.Select(attrs={'class': 'form-control'}),
        }

class EmployeeForm(forms.ModelForm):
    POSITION_CHOICES = [
        ('', 'Select a position'),
        ('Accountant', 'Accountant'),
        ('Analyst', 'Analyst'),
        ('Developer', 'Developer'),
        ('Designer', 'Designer'),
        ('Engineer', 'Engineer'),
        ('Manager', 'Manager'),
        ('Specialist', 'Specialist'),
        ('Technician', 'Technician'),
    ]
    
    position = forms.ChoiceField(choices=POSITION_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'department', 'position', 'email', 'phone']

        widgets = {
            'department': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department'].queryset = Department.objects.filter(status=True)
