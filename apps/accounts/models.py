from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.tunduk.models import Company
from utils.mixins.changelog_mixins import ChangeloggableMixin


class CustomUser(AbstractUser):
    is_admin = models.BooleanField(
        "Дать права на запрос к тундук",
        default=False
    )
    company = models.ForeignKey(
        Company,
        verbose_name='КС пользователя',
        on_delete=models.CASCADE,
        null=True, blank=True
    )

    def __str__(self):
        return f'{self.get_full_name()} - {self.company}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
