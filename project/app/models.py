from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Role(models.Model):
    ADMIN = 'ADMIN'
    PROFESOR = 'PROFESOR'
    STUDENT = 'STUDENT'
    ROLE_CHOICES = [
        (ADMIN, 'admin'),
        (PROFESOR, 'profesor'),
        (STUDENT, 'student'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

class MyUser(AbstractUser):
    STATUS = (('none', 'None'), ('redovni', 'redovni student'), ('izvanredni', 'izvanredni student'))

    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS)

class Course(models.Model):
    ELECTIVE = (('DA', 'da'), ('NE', 'ne'))

    name = models.CharField(max_length=80)
    code = models.CharField(max_length=10)
    program = models.CharField(max_length=250)
    ects = models.IntegerField()
    semester_ft = models.IntegerField()
    semester_pt = models.IntegerField()
    elective = models.CharField(max_length=2, choices=ELECTIVE)
    lecturer = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True)

class EnrollmentList(models.Model):
    STATUS = (('upisan', 'upisan'), ('polozen', 'polozen'), ('izgubljen_potpis', 'izgubljen potpis'))

    student = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=STATUS, default="upisan")