from django.contrib.auth.models import AbstractUser
from django.db import models

MAX_LENGTH_1 = 254
MAX_LENGTH_2 = 150


class User(AbstractUser):
    """Модель пользователя"""

    email = models.EmailField(
        verbose_name='Email',
        max_length=MAX_LENGTH_1,
        unique=True,
    )
    username = models.CharField(
        verbose_name='Username',
        max_length=MAX_LENGTH_2,
        unique=True,
    )
    first_name = models.CharField(max_length=MAX_LENGTH_2)
    last_name = models.CharField(max_length=MAX_LENGTH_2)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']


class Follow(models.Model):
    """Модель подписок"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follow',
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='user_not_equal_author',
            ),
        ]
