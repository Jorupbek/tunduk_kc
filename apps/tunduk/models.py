from django.db import models


class Company(models.Model):
    name = models.CharField(
        'Название компании',
        max_length=300
    )
    client_id = models.CharField(
        'ID клиента',
        help_text='ID клиента в тундук, пример: ak_jol_2000',
        max_length=150,
    )
    infocom_secret_key = models.CharField(
        'Секретный ключ клиента',
        help_text='Секретный ключ выдаваемый от Инфоком',
        max_length=150,
    )
    ip_addr = models.CharField(
        'IP Адрес',
        help_text='IP Адрес сервера тундук',
        max_length=30,
    )
    member_code = models.CharField(
        'Код участника тундук',
        help_text='Код участника тундук, пример: 60000165',
        max_length=30,
    )
    subsystem_code = models.CharField(
        'Название участника в тундук',
        help_text='Название участника передаваемый от тундук, пример: akzhol_subsystem',
        max_length=100
    )
    infocom = models.BooleanField(
        default=True,
        verbose_name='Инфоком',
    )
    unaa = models.BooleanField(
        default=False,
        verbose_name='Унаа',
    )
    minjyst = models.BooleanField(
        default=False,
        verbose_name='Мин. Юст',
    )
    kadastr = models.BooleanField(
        default=False,
        verbose_name='Кадастр',
    )
    minselxoz = models.BooleanField(
        default=False,
        verbose_name='Мин. Сель. Хоз',
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'

