from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    captcha = models.CharField(max_length=200, blank=True, null=True, default=0)
   
    def __str__(self):
        return (f"{str(self.username), str(self.email)}")
    
    class Meta:
        verbose_name = 'User Table'
        db_table = 'user_table'

class UserLocationDetail(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_location_detail')
    location = models.CharField(max_length=200, blank=True, null=True)
    latitude = models.CharField(max_length=200, blank=True, null=True)
    longitude = models.CharField(max_length=200, blank=True, null=True)
    phonenumber = models.CharField(max_length=200, blank=True, null=True)
    country_code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.user.email}, {self.location}"
    
    class Meta:
        verbose_name = 'User Location Detail Table'
        db_table = 'user_location_detail_table'
    