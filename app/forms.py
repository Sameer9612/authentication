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
    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.fields['reporting_manager_id'].queryset = Employee.objects.all()  

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
        fields = [
            'first_name',
            'last_name',
            'username',
            'password',
            'email',
            'mobile',
            'department',
            'role_id',
            'reporting_manager_id',
            'date_of_joining'
        ]

        widgets = {
            'department': forms.Select(attrs={'class': 'form-control'}),
            'role_id': forms.Select(attrs={'class': 'form-control'}),
            'reporting_manager_id': forms.Select(attrs={'class': 'form-control', 'required': False}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'date_of_joining': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Select date'}),
        }


        widgets = {
            'department': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department'].queryset = Department.objects.filter(status=True)
        self.fields['role_id'].queryset = Role.objects.all()
