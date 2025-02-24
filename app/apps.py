# app/apps.py
from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        print("AppConfig.ready() called")  # Debug statement
        # Import and connect signals
        from .signals import handle_department_deactivation, reset_department_sequence
        from django.db.models.signals import pre_save, post_delete
        from .models import Department
        
        # Connect the signals
        pre_save.connect(handle_department_deactivation, sender=Department)
        post_delete.connect(reset_department_sequence, sender=Department)

        print("Signal connected successfully")  # Debug statement
