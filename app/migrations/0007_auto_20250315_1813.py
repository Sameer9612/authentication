from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='mobile',
            field=models.CharField(max_length=100, default=''),
        ),
    ]
