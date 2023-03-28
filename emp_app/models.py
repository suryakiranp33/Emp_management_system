

from django.db import models
from django.contrib.auth.models import User

class UserLogin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)


class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    employee_name = models.CharField(max_length=255)
    contact = models.IntegerField(null=True, blank=True)
    emergency_contact_number = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=300)
    reporting_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField(unique=True)
    designation = models.CharField(max_length=50)
    work_location = models.CharField(max_length=100)
    dob= models.DateField(null=True, blank=True)
    profile_pic=models.ImageField(upload_to='profile/',blank=True)    
    maritial_status=models.CharField(max_length=50)
    blood_group=models.CharField(max_length=50)
    date_of_joining=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.employee_name
    
class LeaveStatus(models.Model):
    status = models.CharField(max_length=100)

class LeaveSystem(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    apply_date = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey(
        LeaveStatus,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    apply_date = models.DateTimeField(auto_now_add=True)
    first_day = models.DateField()
    last_day = models.DateField()
    nature = models.CharField(max_length=50)
