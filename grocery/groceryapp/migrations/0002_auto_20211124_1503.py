# Generated by Django 3.2.8 on 2021-11-24 09:33

from django.db import migrations, models
import groceryapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('groceryapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='image',
            field=models.ImageField(upload_to=groceryapp.models.upload_to, verbose_name='IMAGE'),
        ),
        migrations.AlterField(
            model_name='products',
            name='products',
            field=models.CharField(max_length=255),
        ),
    ]
