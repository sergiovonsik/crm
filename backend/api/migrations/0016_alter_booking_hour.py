# Generated by Django 5.1.6 on 2025-02-21 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_alter_booking_hour'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='hour',
            field=models.CharField(choices=[('6 to 8', '6 to 8'), ('8 to 10', '8 to 10'), ('', '')], default='', max_length=30),
        ),
    ]
