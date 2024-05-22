# Generated by Django 5.0.4 on 2024-05-22 19:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0007_alter_mail_mail_periodicity_alter_mail_mail_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attempt_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время последней попытки')),
                ('attempt_status', models.CharField(choices=[('success', 'Успешно'), ('fail', 'Не успешно')], max_length=50, verbose_name='Cтатус попытки')),
                ('server_response', models.CharField(blank=True, null=True, verbose_name='Ответ почтового сервера')),
                ('mail_settings', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newsletter.mail', verbose_name='Настройка рассылки')),
            ],
            options={
                'verbose_name': 'Попытка рассылки',
                'verbose_name_plural': 'Попытки рассылки',
            },
        ),
    ]
