from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager

# Create your models here.
class UserModuleManager(BaseUserManager):
    use_in_migrations = True 

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        email, password, False, **data
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(str(password))
        user.is_active = False
        user.save()
        created = True
        return user, created
    
class Emoloyee(AbstractUser):
    # Names
    last_name = models.CharField(max_length=255, default=False, null=True)
    last_name = models.CharField(max_length=255, default=False, null=True)
    middle_name = models.CharField(max_length=255, default=False, null=True)

    # Contacts
    email = models.CharField(max_length=100, blank=True, null=True, unique=True)
    phone = models.CharField(max_length=20, blank=False, null=True, unique=True)

    # dates
    date_of_birth = models.DateField(blank=True, null=True)
    employment_date = models.DateTimeField(auto_now_add=True, null=True)

    # Images
    id_photo = models.ImageField(upload_to='id_photos/', blank=True, null=True)
    passport_photo = models.ImageField(upload_to='passport_photos/', blank=True, null=True)

    # Other Info
    gender = models.CharField(max_length=10, default=False, null=True)
    country_code = models.CharField(max_length=255, default=False, null=True)

    # Administration
    created_by = models.CharField(max_length=20, blank=False, null=True)

    # Record 
    
    
    
    
    
    