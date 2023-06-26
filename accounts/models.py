from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, user_type=None):
        if not email:
            raise ValueError("Email is required.")
        if not user_type:
            raise ValueError("User type is required.")

        email = self.normalize_email(email)
        user = self.model(email=email, user_type=user_type)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, user_type=None):
        user = self.create_user(email, password, user_type)
        user.is_admin = True
        user.save()
        return user


class CustomUser(AbstractBaseUser):
    USER_TYPE_CHOICES = (
        ('employer', 'Employer'),
        ('employee', 'Employee'),
    )

    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_type']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    


class EmployerProfile(models.Model):
    user=models.OneToOneField(CustomUser, on_delete=models.CASCADE,limit_choices_to={'user_type': 'employer'})
    photo=models.ImageField(upload_to ='uploads/% Y/% m/% d/',blank=True)
    about=models.CharField(max_length=100,blank=True)

    def __str__(self):
        return f'{self.user.email}'
    
class EmployeeProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='employee_profile',default='',limit_choices_to={'user_type': 'employee'})
    employer=models.ForeignKey(EmployerProfile,on_delete=models.CASCADE,related_name='employee')
    photo=models.ImageField(upload_to ='uploads/% Y/% m/% d/',blank=True)
    about=models.CharField(max_length=100,blank=True)


