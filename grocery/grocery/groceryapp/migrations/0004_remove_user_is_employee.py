# Generated by Django 3.2.8 on 2021-11-11 12:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groceryapp', '0003_user_phno'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_employee',
        ),
    ]
