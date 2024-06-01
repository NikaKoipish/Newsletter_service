import smtplib
from datetime import datetime, timedelta
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mail
from django.core.management import BaseCommand
from django.db.models import F

from config import settings
from newsletter.models import Mail, LogAttempt


class Command(BaseCommand):
    help = "Runs APScheduler."
    """Основная функция запуска рассылок"""
    @staticmethod
    def send_mail():
        zone = pytz.timezone(settings.TIME_ZONE)
        current_datetime = datetime.now(zone)
        # создание объекта с применением фильтра
        mailings = Mail.objects.filter(mail_datetime__lte=current_datetime, mail_status__in=["Создана", "Запущена"])

        for mailing in mailings:
            if (mailing.is_active
                    and mailing.mail_datetime_last
                    and mailing.mail_status in ("Запущена", "Создана",)
                    and current_datetime > mailing.mail_datetime_last):
                mailing.mail_status = "Завершена"
                mailing.save()
            if (
                    mailing.is_active
                    and mailing.mail_datetime_last
                    and mailing.mail_status == "Создана"
                    and (mailing.mail_datetime < current_datetime < mailing.mail_datetime_last)
            ):
                try:
                    send_mail(
                        subject=Mail.objects.get(id=mailing.id).title,
                        message=Mail.objects.get(id=mailing.id).message,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[client.email for client in mailing.client.all()]
                    )
                    mailing.mail_status = "Запущена"
                    mailing.save()
                    if mailing.mail_periodicity == "Раз в день" and (current_datetime -  mailing.mail_datetime_last).days >= 1:
                        mailing.mail_datetime = F("mail_datetime") + timedelta(days=1)
                        mailing.save()
                    elif mailing.mail_periodicity == "Раз в неделю" and (current_datetime -  mailing.mail_datetime_last).days >= 7:
                        mailing.mail_datetime = F("mail_datetime") + timedelta(days=7)
                        mailing.save()
                    elif mailing.mail_periodicity == "Раз в месяц" and (current_datetime -  mailing.mail_datetime_last).days >= 30:
                        mailing.mail_datetime = F("mail_datetime") + timedelta(days=30)
                        mailing.save()
                    attempt = LogAttempt.objects.create(
                        attempt_datetime=current_datetime,
                        attempt_status="Успешно",
                        mail_settings=mailing,
                    )
                    attempt.save()
                except smtplib.SMTPResponseException as e:
                    attempt = LogAttempt.objects.create(
                        attempt_datetime=current_datetime,
                        attempt_status="Не успешно",
                        server_response=str(e),
                        mail_settings=mailing,
                    )
                    attempt.save()

    def handle(self, *args, **options):
        """Функция старта периодических задач"""
        scheduler = BackgroundScheduler()
        scheduler.add_job(self.send_mail, 'interval', seconds=5)
        scheduler.start()
