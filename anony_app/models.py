from django.db import models

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

# Create your models here.


class AuthUserManager(BaseUserManager):
    """
    Customized Authentication Manager
    """
    def get(self, **kwargs):
        if 'email' in kwargs:
            kwargs["email__iexact"] = kwargs["email"]
            del kwargs["email"]
        return super(AuthUserManager, self).get(**kwargs)

    def filter(self, **kwargs):
        if 'email' in kwargs:
            kwargs["email__iexact"] = kwargs["email"]
            del kwargs["email"]
        return super(AuthUserManager, self).filter(**kwargs)

    def create_user(self, username, password=None):
        """
        Overridden create_user method
        """
        user = self.model(username=username)
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        """
        Overridden create_superuser method
        """
        user = self.create_user(username=username, password=password)
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    class Meta(object):
        """
            Meta class
        """
        db_table = 'auth_user_manager'
        verbose_name_plural = "Auth User Manager"


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    username = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    date_joined = models.DateField(null=True, blank=True)

    objects = AuthUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        full_name = ''
        if self.first_name:
            full_name = self.first_name
        if self.last_name:
            full_name += ' ' + str(self.last_name)
        return full_name

    def get_short_name(self):
        return str(self.first_name)

    class Meta:
        db_table = 'auth_user'
        verbose_name_plural = "Users"

    full_name = property(get_full_name)

    def __str__(self):
        return self.username


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    msg = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)