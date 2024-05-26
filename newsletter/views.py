from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView

from newsletter.models import Mail, Client, Message


class HomePageView(TemplateView):
    template_name = 'newsletter/home.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        count = Mail.objects.count()
        is_active = Mail.objects.filter(mail_active=True).count()
        unique = Client.objects.distinct().count()
        context_data = {
            'count': count,
            'is_active': is_active,
            'unique': unique,
        }
        return context_data


class MailListView(ListView):
    """ Просмотр списка рассылок """
    model = Mail


class MailDetailView(DetailView):
    """ Просмотр деталей рассылки """
    model = Mail


class MailCreateView(CreateView):
    """ Создание рассылки """
    model = Mail
    fields = ('title', 'message', 'mail_periodicity', 'client', 'mail_datetime', 'mail_datetime_last')
    success_url = reverse_lazy('newsletter:mail_list')


class MailUpdateView(UpdateView):
    """ Редактирование данных рассылки """
    model = Mail
    fields = ('title', 'message', 'mail_periodicity', 'client', 'mail_datetime', 'mail_datetime_last')
    success_url = reverse_lazy('newsletter:mail_list')


class MailDeleteView(DeleteView):
    """ Удаление рассылки """
    model = Mail
    success_url = reverse_lazy('newsletter:mail_list')


class ClientListView(ListView):
    """ Просмотр списка клиентов """
    model = Client


class ClientDetailView(DetailView):
    """Просмотр одного клиента"""
    model = Client


class ClientCreateView(CreateView):
    """Создание клиента"""
    model = Client
    fields = '__all__'
    success_url = reverse_lazy('newsletter:client_list')


class ClientUpdateView(UpdateView):
    """Редактирование данных клиента"""
    model = Client
    fields = '__all__'
    success_url = reverse_lazy('newsletter:client_list')


class ClientDeleteView(DeleteView):
    """Удаление клиента"""
    model = Client
    success_url = reverse_lazy('newsletter:client_list')


class MessageListView(ListView):
    """ Просмотр списка сообщений """
    model = Message


class MessageDetailView(DetailView):
    """Просмотр деталей сообщения"""
    model = Message


class MessageCreateView(CreateView):
    """Создание сообщения"""
    model = Message
    fields = '__all__'
    success_url = reverse_lazy('newsletter:message_list')


class MessageUpdateView(UpdateView):
    """Редактирование сообщения"""
    model = Message
    fields = '__all__'
    success_url = reverse_lazy('newsletter:message_list')


class MessageDeleteView(DeleteView):
    """Удаление сообщения"""
    model = Message
    success_url = reverse_lazy('newsletter:message_list')