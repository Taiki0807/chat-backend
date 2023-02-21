from django.db import models

# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, _user_has_perm


class AccountManager(BaseUserManager):
    """
    ユーザーを作成する
    """
    def create_user(self, request, **extra_fields):
        now = timezone.now()
        if not request['username']:
            raise ValueError('Users must have a username')

        user = self.model(
            username=request['username'],
            is_active=True,
            date_joined=now,
        )

        user.set_password(request['password'])
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        request_data = {
            'username': username,
            'password': password
        }
        user = self.create_user(request_data)
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    """
    アカウント
    """
    class Meta(object):
        db_table = 'account'

    username = models.CharField(verbose_name='ユーザ名', max_length=255, unique=True)
    email = models.EmailField(verbose_name='Eメール', max_length=255, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    login_date = models.DateTimeField(default=timezone.now)

    objects = AccountManager()

    USERNAME_FIELD = 'username'

    def user_has_perm(self, user, perm, obj):
        return _user_has_perm(user, perm, obj)

    def has_perm(self, perm, obj=None):
        return _user_has_perm(self, perm, obj=obj)

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def is_superuser(self):
        return self.is_admin