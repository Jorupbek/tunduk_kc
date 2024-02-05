import uuid

from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

try:
    from django.db.models import JSONField
except ImportError:
    from django.contrib.postgres.fields import JSONField

ACTION_CREATE = 'create'
ACTION_UPDATE = 'update'
ACTION_DELETE = 'delete'


class ChangeLog(models.Model):
    TYPE_ACTION_ON_MODEL = (
        (ACTION_CREATE, _('Создание')),
        (ACTION_UPDATE, _('Изменение')),
        (ACTION_DELETE, _('Удаление')),
    )

    changed = models.DateTimeField(auto_now=True, verbose_name=u'Дата/время изменения')
    model = models.CharField(max_length=255, verbose_name=u'Таблица', null=True)
    record_id = models.IntegerField(verbose_name=u'ID записи', null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=u'Автор изменения',
        on_delete=models.DO_NOTHING, null=True)
    action_on_model = models.CharField(
        choices=TYPE_ACTION_ON_MODEL, max_length=50, verbose_name=u'Действие', null=True)
    data = JSONField(verbose_name=u'Изменяемые данные модели', default=dict)

    class Meta:
        ordering = ('-changed',)
        verbose_name = _('Журнал изменений')
        verbose_name_plural = _('Журнал изменений')

    def __str__(self):
        return f'{self.id}'

    @classmethod
    def add(cls, instance, user, action_on_model, data, id=None):
        """Создание записи в журнале регистрации изменений"""
        log = ChangeLog.objects.get(id=id) if id else ChangeLog()
        log.model = instance._meta.verbose_name
        log.record_id = instance.pk
        if user:
            log.user = user
        log.action_on_model = action_on_model
        log.data = data
        log.save()
        return log.pk


class TundukRequestLog(models.Model):
    class RequestType(models.TextChoices):
        INFOCOM = 'Инфоком', 'Инфоком'
        UNAA = 'Унаа', 'Унаа'
        MINJYST = 'Мин. Юст', 'Мин. Юст'
        KADASTR = 'Кадастр', 'Кадастр'
        MINSELXOZ = 'Мин. Сель. Хоз', 'Мин. Сель. Хоз'

    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    request_type = models.CharField('Тип запроса', choices=RequestType.choices,
                                    max_length=20, help_text='В какой сервис отправлен запрос')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=u'Автор запроса',
        on_delete=models.DO_NOTHING, null=True)
    data = JSONField(verbose_name=u'Запрошенные данные', default=dict)
    file = models.FileField('Фото / Документ запрашиваемого',
                              upload_to='tunduk/%m.%y',
                              null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=u'Дата/время изменения')

    class Meta:
        verbose_name = 'Журнал запросов'
        verbose_name_plural = 'Журнал запросов'

    def get_absolute_url(self):
        return reverse('tunduk:infocom-detail',  # todo переделать
                       args=[self.created_at.year, self.created_at.month,
                             self.pk, self.uuid])
