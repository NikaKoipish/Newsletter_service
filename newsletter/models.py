from django.db import models
from django.utils.translation import gettext_lazy as _

NULLABLE = {'null': True, 'blank': True}


class Client(models.Model):
    """ Клиент """
    first_name = models.CharField(max_length=20, verbose_name='Имя')
    last_name = models.CharField(max_length=20, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=20, verbose_name='Отчество', **NULLABLE)
    email = models.EmailField(verbose_name='Электронный адрес')
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)

    def __str__(self):
        return f'{self.first_name}{self.last_name} ({self.email})'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    """ Сообщение """
    message_title = models.CharField(max_length=100, verbose_name='Тема письма')
    message_content = models.TextField(verbose_name='Содержание')

    def __str__(self):
        return f'{self.message_title}'

    class Meta:
        verbose_name = 'Сообщение для рассылки'
        verbose_name_plural = 'Сообщения для рассылки'


class Mail(models.Model):
    """ Рассылка """
    class PeriodicityOfMail(models.TextChoices):
        PER_A_DAY = "Раз в день", _("Раз в день")
        PER_A_WEEK = "Раз в неделю", _("Раз в неделю")
        PER_A_MONTH = "Раз в месяц", _("Раз в месяц")

    class StatusOfMail(models.TextChoices):
        CREATED = "Создана", _("Создана")
        LAUNCHED = "Запущена", _("Запущена")
        FINISHED = "Завершена", _("Завершена")

    title = models.CharField(max_length=100, verbose_name='Тема рассылки')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение')
    client = models.ManyToManyField(Client, verbose_name='Клиент', related_name='client')
    mail_datetime = models.DateTimeField(verbose_name='Начало отправки рассылки')
    mail_datetime_last = models.DateTimeField(verbose_name='Последняя дата отправки рассылки', **NULLABLE)
    mail_periodicity = models.CharField(verbose_name='Периодичность', choices=PeriodicityOfMail)
    mail_status = models.CharField(verbose_name='Статус отправки', choices=StatusOfMail, default=StatusOfMail.CREATED)
    mail_active = models.BooleanField(verbose_name='Активность рассылки', default=True)

    def __str__(self):
        return f'{self.mail_status}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class LogAttempt(models.Model):
    """Попытка рассылки"""
    ATTEMPT_STATUS = [
        ("success", "Успешно"),
        ("fail", "Не успешно"),
    ]
    attempt_datetime = models.DateTimeField(verbose_name='Дата и время последней попытки', auto_now_add=True)
    attempt_status = models.CharField(max_length=50, choices=ATTEMPT_STATUS, verbose_name="Cтатус попытки")
    server_response = models.CharField(verbose_name="Ответ почтового сервера", **NULLABLE)
    mail_settings = models.ForeignKey(Mail, verbose_name="Настройка рассылки", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.mail_settings}, {self.attempt_datetime}, {self.attempt_status}"

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"
