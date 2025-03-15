# User Guide for Employee Management System

## Overview
This Employee Management System allows administrators to manage departments, roles, and employees efficiently. The system provides functionalities for creating, updating, and deleting records, as well as user authentication features.

## Features

### Role Management
- **View Roles**: Access the role dashboard to view all roles, categorized into active and inactive.
- **Create Role**: Use the form to create a new role. The role name can include the selected position.
- **Update Role**: Edit existing roles by selecting them from the dashboard.
- **Delete Role**: Soft delete a role, which will mark it as inactive.
- **Reactivate Role**: Restore a previously inactive role.

### Department Management
- **View Departments**: Access the department dashboard to view all departments, categorized into active and inactive.
- **Create Department**: Use the form to create a new department.
- **Update Department**: Edit existing departments by selecting them from the dashboard.
- **Delete Department**: Soft delete a department, which will mark it as inactive.
- **Reactivate Department**: Restore a previously inactive department.
- **Reassign Employees**: Reassign employees from one department to another.

### Employee Management
- **View Employees**: Access the employee dashboard to view all employees.
- **Create Employee**: Use the form to add a new employee.
- **Update Employee**: Edit existing employee details by selecting them from the dashboard.
- **Delete Employee**: Soft delete an employee, which will mark them as inactive.
- **View Department Employees**: See all employees associated with a specific department.

### User Authentication
- **Login**: Users can log in to access the system.
- **Logout**: Users can log out to end their session.
- **Password Reset**: Users can reset their password using the provided functionality.

### Search Functionality
- **Search Departments**: Use the search bar to find departments by name.

## Data Models

### Department
- **Fields**:
  - `dept_id`: Unique identifier for the department.
  - `dept_name`: Name of the department.
  - `description`: Description of the department.
  - `created_at`: Timestamp of when the department was created.
  - `updated_at`: Timestamp of the last update.
  - `status`: Indicates if the department is active.
  - `order`: Order of the department in listings.
- **Methods**:
  - `has_linked_employees()`: Checks if there are any active employees linked to this department.
  - `reactivate()`: Reactivates a deactivated department.

### Role
- **Fields**:
  - `role_id`: Unique identifier for the role.
  - `role_name`: Name of the role.
  - `description`: Description of the role.
  - `created_at`: Timestamp of when the role was created.
  - `updated_at`: Timestamp of the last update.
  - `status`: Indicates if the role is active.
- **String Representation**: Includes the role name and associated employee positions.

### Employee
- **Fields**:
  - `emp_id`: Unique identifier for the employee.
  - `first_name`: Employee's first name.
  - `last_name`: Employee's last name.
  - `department`: Foreign key linking to the department.
  - `position`: Employee's position.
  - `email`: Employee's email address.
  - `phone`: Employee's phone number.
  - `status`: Indicates if the employee is active.
  - `created_at`: Timestamp of when the employee was created.
  - `updated_at`: Timestamp of the last update.
- **Property**:
  - `full_name`: Returns the employee's full name.

## Q&A Section

### Q1: How do I reset my password?
A: You can reset your password by clicking on the "Forgot Password?" link on the login page. Follow the instructions sent to your email to reset your password.

### Q2: What should I do if I cannot log in?
A: Ensure that you are using the correct username and password. If you have forgotten your password, use the password reset feature. If the issue persists, contact support.

### Q3: How can I view all employees in a department?
A: Navigate to the department dashboard and select the department you wish to view. You will see a list of all employees associated with that department.

### Q4: Can I delete a department that has employees linked to it?
A: No, you cannot delete a department that has active employees linked to it. You must reassign those employees to another department before deletion.

### Q5: How do I create a new role?
A: Go to the role management section and click on "Create Role." Fill out the form with the necessary details and submit it.

## Conclusion
This system is designed to streamline the management of employees, departments, and roles within an organization. For any issues or further assistance, please contact support.
