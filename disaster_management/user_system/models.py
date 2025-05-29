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