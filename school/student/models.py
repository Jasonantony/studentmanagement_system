from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    class_name = models.CharField(max_length=20)
    student_id = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    total_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fees_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    attendance_percentage = models.FloatField(default=0.0)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.name


class Staff(models.Model):
    name = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    email = models.EmailField(unique=True, default="staff@gmail.com")
    password = models.CharField(max_length=255, default="1234")

    def __str__(self):
        return self.name
