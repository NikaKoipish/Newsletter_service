from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='email', help_text='введите адрес электронной почты')
    is_active = models.BooleanField(default=True, verbose_name='активен')
    name = models.CharField(max_length=100, verbose_name='название', **NULLABLE)

    token = models.CharField(max_length=100, verbose_name='token', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        permissions = [
            (
                "block_the_user",
                "Can block the user"
            ),
            (
                "view_all_users",
                "Can view all users"
            )
        ]

