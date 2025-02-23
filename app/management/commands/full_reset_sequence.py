from django.core.management.base import BaseCommand
from django.db import connection, transaction
from app.models import Department, Employee
import json


class Command(BaseCommand):
    help = 'Completely resets department IDs starting from 1'

    def handle(self, *args, **options):
        # Export all department data and employee relationships
        departments = list(Department.objects.values())
        employee_departments = {
            emp.pk: emp.department_id
            for emp in Employee.objects.select_related('department')
        }
        
        # Disable foreign key constraints
        with connection.cursor() as cursor:
            cursor.execute('PRAGMA foreign_keys=OFF')

        # First transaction for schema changes
        with transaction.atomic():
            with connection.schema_editor() as editor:
                # Create new table without foreign key constraint initially
                editor.execute("""
                    CREATE TABLE temp_employee (
                        emp_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        first_name TEXT NOT NULL,
                        last_name TEXT NOT NULL,
                        department_id INTEGER,
                        position TEXT,
                        email TEXT,
                        phone TEXT,
                        status BOOLEAN DEFAULT TRUE,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    );
                """)

                # Copy data to temporary table, handling NULL department_ids
                editor.execute("""
                    INSERT INTO temp_employee
                    SELECT emp_id, first_name, last_name,
                           CASE WHEN department_id = 0 THEN NULL ELSE department_id END,
                           position, email, phone, status, created_at, updated_at
                    FROM employee;
                """)
                
                # Drop original table
                editor.execute("DROP TABLE employee;")
                
                # Rename temporary table
                editor.execute("ALTER TABLE temp_employee RENAME TO employee;")

        # Second transaction for data changes
        with transaction.atomic():
            # Set employee departments to NULL
            Employee.objects.filter(department_id__isnull=False).update(department_id=None)

            # Delete all departments
            Department.objects.all().delete()

            # Reset sequences for both department and employee tables
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('department', 'employee')")
                cursor.execute("INSERT INTO sqlite_sequence (name, seq) VALUES ('department', 0)")
                cursor.execute("INSERT INTO sqlite_sequence (name, seq) VALUES ('employee', 0)")

            
            # Recreate departments with new IDs
            new_dept_ids = {}
            for dept in departments:
                old_id = dept['dept_id']
                # Remove old ID to let Django assign new one
                dept.pop('dept_id')
                new_dept = Department.objects.create(**dept)
                new_dept_ids[old_id] = new_dept.pk
            
            # Reassign employees to their original departments
            for emp_id, dept_id in employee_departments.items():
                if dept_id and dept_id in new_dept_ids:
                    Employee.objects.filter(pk=emp_id).update(
                        department_id=new_dept_ids[dept_id]
                    )

            # Final schema update with proper constraints
            with connection.schema_editor() as editor:
                # Create final table with proper constraints
                editor.execute("""
                    CREATE TABLE temp_employee (
                        emp_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        first_name TEXT NOT NULL,
                        last_name TEXT NOT NULL,
                        department_id INTEGER,
                        position TEXT,
                        email TEXT,
                        phone TEXT,
                        status BOOLEAN DEFAULT TRUE,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (department_id) REFERENCES department(dept_id)
                    );
                """)

                # Copy data to final table
                editor.execute("""
                    INSERT INTO temp_employee
                    SELECT * FROM employee;
                """)
                
                # Drop intermediate table
                editor.execute("DROP TABLE employee;")
                
                # Rename final table
                editor.execute("ALTER TABLE temp_employee RENAME TO employee;")

        # Re-enable foreign key constraints
        with connection.cursor() as cursor:
            cursor.execute('PRAGMA foreign_keys=ON')

        # Verify sequences
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM sqlite_sequence")
            sequences = cursor.fetchall()
            self.stdout.write(self.style.SUCCESS(f'Successfully reset sequences: {sequences}'))
