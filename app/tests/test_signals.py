from django.test import TestCase
from app.models import Department


class DepartmentSignalTests(TestCase):
    def test_department_id_reordering(self):
        # Create initial departments
        dept1 = Department.objects.create(dept_name="Dept A", description="Test A")
        dept2 = Department.objects.create(dept_name="Dept B", description="Test B")
        dept3 = Department.objects.create(dept_name="Dept C", description="Test C")
        
        # Delete middle department
        dept2.delete()
        
        # Verify IDs are reordered
        remaining_depts = Department.objects.order_by('dept_id')
        self.assertEqual(remaining_depts[0].dept_id, 1)
        self.assertEqual(remaining_depts[1].dept_id, 2)
        
        # Verify names are preserved
        self.assertEqual(remaining_depts[0].dept_name, "Dept A")
        self.assertEqual(remaining_depts[1].dept_name, "Dept C")
