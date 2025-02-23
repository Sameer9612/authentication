from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Department, Employee
from .forms import DepartmentForm, EmployeeForm

def is_admin(user):
    return user.is_superuser

# Department views
@login_required
@user_passes_test(is_admin)
def department_dashboard(request):
    departments = Department.objects.filter(status=True)
    return render(request, 'departments/dashboard.html', {'departments': departments})

@login_required
@user_passes_test(is_admin)
def create_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department created successfully!')
            return redirect('departments:dashboard')
    else:
        form = DepartmentForm()
    return render(request, 'departments/form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def update_department(request, dept_id):
    department = get_object_or_404(Department, dept_id=dept_id)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department updated successfully!')
            return redirect('departments:dashboard')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'departments/form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def reassign_employees(request, dept_id):
    department = get_object_or_404(Department, dept_id=dept_id)
    employees = Employee.objects.filter(department=department, status=True)
    
    if request.method == 'POST':
        new_department_id = request.POST.get('new_department')
        new_department = get_object_or_404(Department, dept_id=new_department_id)
        
        employees.update(department=new_department)
        messages.success(request, f'Employees successfully reassigned to {new_department.dept_name}')
        return redirect('departments:delete', dept_id=dept_id)
    
    departments = Department.objects.filter(status=True).exclude(dept_id=department.dept_id)

    return render(request, 'departments/reassign_employees.html', {
        'department': department,
        'employees': employees,
        'departments': departments
    })


@login_required
@user_passes_test(is_admin)
def delete_department(request, dept_id):
    department = get_object_or_404(Department, dept_id=dept_id)
    if request.method == 'POST':
        if department.has_linked_employees():
            messages.error(request, 
                'Cannot deactivate department. There are active employees linked to this department. '
                'Please reassign them to another department first using the Employee Management section.'
            )
        else:
            department.status = False
            department.save()
            messages.success(request, 'Department deactivated successfully!')
        return redirect('departments:dashboard')
    return render(request, 'departments/confirm_delete.html', {
        'department': department,
        'has_linked_employees': department.has_linked_employees(),
        'linked_employee_count': department.employee_set.count
    })

@login_required
@user_passes_test(is_admin)
def search_department(request):
    query = request.GET.get('q')
    if query:
        departments = Department.objects.filter(
            dept_name__icontains=query, 
            status=True
        )
    else:
        departments = Department.objects.filter(status=True)
    return render(request, 'departments/search_results.html', {'departments': departments})

# Employee views
@login_required
@user_passes_test(is_admin)
def employee_dashboard(request):
    employees = Employee.objects.filter(status=True)
    return render(request, 'employees/dashboard.html', {'employees': employees})

@login_required
@user_passes_test(is_admin)
def create_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee created successfully!')
            return redirect('employee_dashboard')
    else:
        form = EmployeeForm()
    return render(request, 'employees/form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def update_employee(request, emp_id):
    employee = get_object_or_404(Employee, emp_id=emp_id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee updated successfully!')
            return redirect('employee_dashboard')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employees/form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def delete_employee(request, emp_id):
    employee = get_object_or_404(Employee, emp_id=emp_id)
    if request.method == 'POST':
        employee.status = False
        employee.save()
        messages.success(request, 'Employee deactivated successfully!')
        return redirect('employee_dashboard')
    return render(request, 'employees/confirm_delete.html', {'employee': employee})
