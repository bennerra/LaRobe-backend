from django.contrib.auth.models import AbstractUser
from django.db import models


class SlimRole(models.TextChoices):
    STANDARD = 'standard', 'Стандартный'
    BLOCKED = 'blocked', 'Заблокированный'


class User(AbstractUser):
    class Role(models.TextChoices):
        STANDARD = 'standard', 'Стандартный'
        BLOCKED = 'blocked', 'Заблокированный'
        JUNIOR_ADMIN = 'junior_admin', 'Мл. администратор'
        SENIOR_ADMIN = 'senior_admin', 'Ст. администратор'

    patronymic = models.CharField(blank=True, max_length=32)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    nickname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.IntegerField()
    sex = models.CharField(max_length=10, choices=(('male', 'male'), ('female', 'female')))
    date_of_birth = models.DateField()
    avatar = models.ImageField(upload_to='avatars/%Y/%m')
    banner_image = models.ImageField(upload_to='banners/%Y/%m')
    about_me = models.TextField(blank=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STANDARD)
    role_expired = models.DateTimeField(blank=True, null=True)

    @property
    def is_junior_admin(self):
        return self.role == self.Role.JUNIOR_ADMIN

    @property
    def is_senior_admin(self):
        return self.role == self.Role.SENIOR_ADMIN

    @property
    def is_standard(self):
        return self.role == self.Role.STANDARD
