from django.contrib import admin
from newsletter.models import Message, Client, Mail, LogAttempt


@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    list_display = ('title', 'message', 'mail_periodicity', 'mail_status')
    list_filter = ('mail_status', 'mail_periodicity')
    search_fields = ('title',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('message_title', 'message_content')
    search_fields = ('message_title', 'message_content',)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'patronymic', 'email', 'comment')
    search_fields = ('last_name',)


@admin.register(LogAttempt)
class LogAttemptAdmin(admin.ModelAdmin):
    list_display = ('attempt_datetime', 'attempt_status', 'server_response')
    list_filter = ('attempt_status',)