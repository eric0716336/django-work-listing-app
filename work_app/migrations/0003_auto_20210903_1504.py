# Generated by Django 3.1.3 on 2021-09-03 07:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('work_app', '0002_auto_20210903_1446'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jobs',
            old_name='title',
            new_name='position',
        ),
    ]
