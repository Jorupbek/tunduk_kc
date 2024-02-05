from django.contrib.auth.models import AbstractUser
from django.db import models

from utils.mixins.changelog_mixins import ChangeloggableMixin


class CustomUser(AbstractUser):
    is_admin = models.BooleanField(
        "Дать права на запрос к тундук",
        default=False
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
