# Generated by Django 3.2.25 on 2024-09-07 19:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smartflow', '0009_columns_datatypes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='columns',
            old_name='datatypes',
            new_name='datatype',
        ),
    ]