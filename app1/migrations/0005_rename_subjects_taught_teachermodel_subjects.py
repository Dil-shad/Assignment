# Generated by Django 4.0.5 on 2022-07-02 10:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_remove_teachermodel_subjects_taught_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teachermodel',
            old_name='subjects_taught',
            new_name='subjects',
        ),
    ]