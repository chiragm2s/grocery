# Generated by Django 3.2.8 on 2021-11-13 10:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('groceryapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='products',
            name='category',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='groceryapp.category'),
            preserve_default=False,
        ),
    ]