# Generated by Django 5.1.6 on 2025-02-21 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_alter_booking_hour'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='type_of_service',
            field=models.CharField(choices=[('classes', 'classes'), ('free_climbing', 'free_climbing'), ('', '')], max_length=30),
        ),
    ]
