from django.contrib.auth.models import AbstractUser
# from django.contrib.auth import get_user_model
from django.db import models

# User = get_user_model()


class User(AbstractUser):

    email = models.EmailField(
        verbose_name='Email',
        max_length=254,
        unique=True,
    )
    username = models.CharField(
        verbose_name='Username',
        max_length=150,
        unique=True,
    )
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)


class Follow(models.Model):
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
                name='unique follow',
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='user_not_equal_author',
            ),
        ]
