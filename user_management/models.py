from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


# --------------------------
# Custom User Manager
# --------------------------
class UserModuleManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, phone, password=None, **extra_fields):
        """
        Creates and saves a User with the given phone number and password.
        """
        if not phone:
            raise ValueError("The phone number must be set")
        phone = str(phone).strip()
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(phone, password, **extra_fields)


# --------------------------
# User Model (phone login)
# --------------------------
class User(AbstractUser):
    # Names
    last_name = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    middle_name = models.CharField(max_length=255, blank=True, null=True)

    # Contacts
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True, null=True, unique=True)

    # main login field    
    date_of_birth = models.DateField(blank=True, null=True)
    id_number = models.CharField(max_length=50, blank=True, null=True)
    id_photo = models.ImageField(upload_to="id_photos/", blank=True, null=True)
    passport_photo = models.ImageField(upload_to="passport_photos/", blank=True, null=True)
    id_type = models.CharField(
        max_length=20,
        choices=[
            ("national_id", "National ID"),
            ("passport", "Passport"),
            ("foreign_id", "Foreign ID"),
        ],
        blank=True,
        null=True,
    )
    gender = models.CharField(
        max_length=10,
        choices=[("male", "Male"), ("female", "Female")],
        blank=True,
        null=True,
    )
    country_code = models.CharField(max_length=10, blank=True, null=True)

    # created_by = models.CharField(max_length=50, blank=True, null=True)

    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)    

    USERNAME_FIELD = "phone"  # login with phone
    REQUIRED_FIELDS = []  # no username or email required

    objects = UserModuleManager()

    def __str__(self):
        return f"{self.phone} ({self.get_full_name() or 'No Name'})"
    
    def get_full_name(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}"


# # --------------------------
# # Department Model
# # --------------------------
# class Department(models.Model):
#     name = models.CharField(max_length=100, unique=True)
#     description = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return self.name


# # --------------------------
# # Role Model
# # --------------------------
# class Role(models.Model):
#     name = models.CharField(max_length=100, unique=True)
#     description = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return self.name


# # --------------------------
# # Employee Model
# # --------------------------
# class Employee(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employee")
#     department = models.ForeignKey(
#         Department, on_delete=models.SET_NULL, null=True, blank=True, related_name="employees"
#     )
#     role = models.ForeignKey(
#         Role, on_delete=models.SET_NULL, null=True, blank=True, related_name="employees"
#     )

#     employment_date = models.DateField(auto_now_add=True)
#     contract = models.FileField(upload_to="contracts/", blank=True, null=True)

#     def __str__(self):
#         return f"{self.user.phone} - {self.role.name if self.role else 'No Role'}"


# # --------------------------
# # Salary Model
# # --------------------------
# class Salary(models.Model):
#     employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="salaries")
#     amount = models.DecimalField(max_digits=12, decimal_places=2)
#     currency = models.CharField(max_length=10, default="KES")
#     effective_from = models.DateField()
#     effective_to = models.DateField(blank=True, null=True)

#     def __str__(self):
#         return f"{self.employee.user.phone} - {self.amount} {self.currency}"


# # --------------------------
# # Benefit Model
# # --------------------------
# class Benefit(models.Model):
#     employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="benefits")
#     name = models.CharField(max_length=100)
#     description = models.TextField(blank=True, null=True)
#     amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

#     def __str__(self):
#         return f"{self.name} ({self.employee.user.phone})"
