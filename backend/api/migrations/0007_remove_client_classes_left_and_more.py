# Generated by Django 5.1.5 on 2025-02-02 15:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_paymentticket_amount_of_uses_left'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='classes_left',
        ),
        migrations.RemoveField(
            model_name='client',
            name='free_climbing_left',
        ),
    ]
