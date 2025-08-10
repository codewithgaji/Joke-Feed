from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser


# Create your models here.




class CustomUser(BaseUserManager):
  def create_user(self, email, password, **extra_fields):
    email = self.normalize_email(email)
    user = self.model(email=email, **extra_fields)

    user.set_password(password)
    user.save()

  def create_super_user(self, email, passsword, **extra_fields):
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_superuser', True)

    if extra_fields.get('is_staff') is not True:
      raise ValueError("User must have is_staff being True")
    
    if extra_fields.get('is_superuser') is not True:
      raise ValueError("User must have is_superuser being True")
    
    return self.create_user(email=email, password=passsword)
  

class User(AbstractUser):
  email = models.EmailField(unique=True, max_length=45)
  date_of_birth = models.DateField(null=True, blank=True)
  username = models.CharField(max_length=20)

  REQUIRED_FIELDS = ['username']
  USERNAME_FIELD = 'email'

  objects = CustomUser()

  def __str__(self):
    return self.username


  