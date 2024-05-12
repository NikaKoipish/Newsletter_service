from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView

from newsletter.models import Mail, Client, Message


class HomePageView(TemplateView):
    template_name = 'newsletter/home.html'


class MailListView(ListView):
    """ Просмотр списка рассылок """
    model = Mail
    template_name = 'newsletter/mail_list.html'


class MailDetailView(DetailView):
    """ Просмотр деталей рассылки """
    model = Mail
    template_name = 'newsletter/mail_detail.html'


class MailCreateView(CreateView):
    """ Создание рассылки """
    model = Mail
    fields = ('title', 'mail_periodicity')
    success_url = reverse_lazy('newsletter:mail_list')


class MailUpdateView(UpdateView):
    """ Редактирование данных рассылки """
    model = Mail
    fields = ('title', 'mail_periodicity')
    success_url = reverse_lazy('newsletter:mail_list')


class MailDeleteView(DeleteView):
    """ Удаление рассылки """
    model = Mail
    success_url = reverse_lazy('newsletter:mail_list')


class ClientListView(ListView):
    """ Просмотр списка клиентов """
    model = Client
    template_name = 'newsletter/client_list.html'


class ClientDetailView(DetailView):
    """Просмотр одного клиента"""
    model = Client
    template_name = 'newsletter/client_detail.html'


class ClientCreateView(CreateView):
    """Создание клиента"""
    model = Client
    fields = '__all__'


class ClientUpdateView(UpdateView):
    """Редактирование данных клиента"""
    model = Client
    fields = '__all__'


class ClientDeleteView(DeleteView):
    """Удаление клиента"""
    model = Client
    success_url = reverse_lazy('newsletter:client_list')


class MessageListView(ListView):
    """ Просмотр списка сообщений """
    model = Message
    template_name = 'newsletter/message_list.html'


class MessageDetailView(DetailView):
    """Просмотр деталей сообщения"""
    model = Message
    template_name = 'newsletter/message_detail.html'


class MessageCreateView(CreateView):
    """Создание сообщения"""
    model = Message
    fields = '__all__'


class MessageUpdateView(UpdateView):
    """Редактирование сообщения"""
    model = Message
    fields = '__all__'


class MessageDeleteView(DeleteView):
    """Удаление сообщения"""
    model = Message
    success_url = reverse_lazy('newsletter:message_list')