# Generated by Django 3.2.12 on 2022-07-01 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SubjectsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TeacherModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=220)),
                ('last_name', models.CharField(max_length=220)),
                ('email', models.EmailField(max_length=220, unique=True)),
                ('phone_number', models.CharField(max_length=20)),
                ('room_number', models.CharField(max_length=5)),
                ('image_name', models.ImageField(blank=True, upload_to='profile_pictures')),
                ('subjects_taught', models.ManyToManyField(to='app1.SubjectsModel')),
            ],
        ),
    ]