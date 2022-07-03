# Generated by Django 4.0.5 on 2022-07-02 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_remove_teachermodel_subjects_taught_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teachermodel',
            name='subjects_taught',
        ),
        migrations.AddField(
            model_name='teachermodel',
            name='subjects_taught',
            field=models.ManyToManyField(to='app1.subjectsmodel'),
        ),
    ]