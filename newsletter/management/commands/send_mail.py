from datetime import datetime
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mail
from django.core.management import BaseCommand

from config import settings
from newsletter.models import Mail, Message


class Command(BaseCommand):

    """Основная функция запуска рассылок"""
    @staticmethod
    def send_mailing():
        zone = pytz.timezone(settings.TIME_ZONE)
        current_datetime = datetime.now(zone)
        # создание объекта с применением фильтра
        mailings = Mail.objects.filter(mail_datetime__lte=current_datetime).filter(mail_status__in=[список_статусов])

        for mailing in mailings:
            try:
                send_mail(
                    subject=Message.objects.get(id=mailing.id).message_title,
                    message=Message.objects.get(id=mailing.id).message_content,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email for client in mailing.client.all()]
                )
                if (
                        mailing.period == Mail.mail_periodicity.PER_A_DAY
                        and current_datetime.day >= 1
                ):
                    mailing.sent_time = F("sent_time") + timedelta(days=1)
                    mailing.status = MailingSettings.StatusMailingSettings.STARTED
                elif (
                        mailing.period == MailingSettings.PeriodMailingSettings.ONE_WEEK
                        and current_datetime.day >= 7
                ):
                    mailing.sent_time = F("sent_time") + timedelta(days=7)
                    mailing.status = MailingSettings.StatusMailingSettings.STARTED
                elif (
                        mailing.period == MailingSettings.PeriodMailingSettings.ONE_MONTH
                        and current_datetime.day >= 30
                ):
                    mailing.sent_time = F("sent_time") + timedelta(days=30)
                    mailing.status = MailingSettings.StatusMailingSettings.STARTED
                mailing.save()
                status = True
                server_response = "успешно"
            except smtplib.SMTPResponseException as e:
                status = False
                server_response = str(e)
            finally:
                Logs.objects.create(
                    mailing=mailing,
                    status=status,
                    server_response=server_response,
                )

    """Функция старта периодических задач"""
    def start(self):
        scheduler = BackgroundScheduler()
        scheduler.add_job(self.send_mailing, 'interval', seconds=10)
        scheduler.start()
