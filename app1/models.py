from django.db import models

# Create your models here.

class SubjectsModel(models.Model):
    subject_name = models.CharField(max_length=100, null=False, unique=True)
    def __str__(self):
        return self.subject_name

class TeacherModel(models.Model):
    first_name = models.CharField(max_length=220)
    last_name = models.CharField(max_length=220)
    email = models.EmailField(max_length=220, null=False, unique=True)
    phone_number = models.CharField(max_length=20)
    room_number = models.CharField(max_length=5)
    image = models.ImageField(upload_to='profile_pictures', blank=True,null=True)
    subjects = models.ManyToManyField(SubjectsModel)
    def __str__(self):
        return self.first_name
