import logging
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.db import transaction, connection
from django.db import models
from .models import Department, Employee

logger = logging.getLogger(__name__)

@receiver(pre_save, sender=Department)
def handle_department_deactivation(sender, instance, **kwargs):
    """Handles department deactivation without altering primary keys."""
    if instance.pk and not instance.status:
        logger.info("Department deactivation detected")

        try:
            with transaction.atomic():
                # Reassign employees to NULL
                Employee.objects.filter(department=instance).update(department=None)

                # Update order field instead of modifying dept_id
                departments = Department.objects.filter(status=True).order_by('order')
                for index, department in enumerate(departments, start=1):
                    department.order = index
                    department.save()

        except Exception as e:
            logger.error(f"Error handling department deactivation: {str(e)}")
            raise

@receiver(post_delete, sender=Department)
def reset_department_sequence(sender, instance, **kwargs):
    """Resets auto-increment sequence after department deletion."""
    try:
        with connection.cursor() as cursor:
            db_engine = connection.settings_dict['ENGINE']
            max_id = Department.objects.aggregate(models.Max('dept_id'))['dept_id__max']
            if max_id is None:
                # No departments exist, reset sequence to 1
                reset_value = 1
                cursor.execute("DELETE FROM sqlite_sequence WHERE name = ?", ('app_department',))
                cursor.execute("INSERT INTO sqlite_sequence (name, seq) VALUES (?, ?)", ('app_department', reset_value))
                logger.debug(f"No departments found, resetting sequence to: {reset_value}")
            else:
                # Departments exist, update sequence to max_id + 1
                reset_value = max_id + 1
                cursor.execute("UPDATE sqlite_sequence SET seq = ? WHERE name = ?", (reset_value, 'app_department'))
                logger.debug(f"Max department ID found: {max_id}, resetting sequence to: {reset_value}")




            if 'postgresql' in db_engine:
                cursor.execute("ALTER SEQUENCE app_department_dept_id_seq RESTART WITH %s;", [max_id + 1])
            elif 'mysql' in db_engine:
                cursor.execute("ALTER TABLE app_department AUTO_INCREMENT = %s;", [max_id + 1])


    except Exception as e:
        logger.error(f"Error resetting sequence: {str(e)}")
        raise
