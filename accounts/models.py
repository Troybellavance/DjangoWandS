from django.db import models
from django.contrib.auth.models import (
     AbstractBaseUser, BaseUserManager
)



class UserManager(BaseUserManager):

    def create_user(self, email, first_name=None, last_name=None, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Users require an email.")
        if not password:
            raise ValueError("Users require a password.")
        user_obj = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staff(self, email, first_name=None, last_name=None, password=None):
        user = self.create_user(
               email,
               first_name = first_name,
               last_name = last_name,
               password=password,
               is_staff=True
        )
        return user

    def create_superuser(self, email,first_name=None, last_name=None, password=None):
        user = self.create_user(
                email,
                first_name = first_name,
                last_name = last_name,
                password=password,
                is_staff=True,
                is_admin=True
        )
        return user


class CustomUser(AbstractBaseUser):
    #username    = models.CharField(max_length=35)
    first_name   = models.CharField(max_length=75, blank=True, null=True)
    last_name    = models.CharField(max_length=75, blank=True, null=True)
    email        = models.EmailField(max_length=75, default='tuskysclub@tuskysclub.com', unique=True)
    staff        = models.BooleanField(default=False)
    admin        = models.BooleanField(default=False)
    active       = models.BooleanField(default=True)
    timestamp    = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'

    REQUIED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.first_name and self.last_name:
            return self.first_name and self.last_name
        return self.email

    def get_short_name(self):
        if self.first_name:
            return self.first_name
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

# class Profile(models.Model):
#     username = models.OneToOneField(CustomUser) #Going to move this to own app/enhance registration for email confirmation.


class GuestEmail(models.Model):
    email       = models.EmailField()
    active      = models.BooleanField(default=True)
    update      = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
