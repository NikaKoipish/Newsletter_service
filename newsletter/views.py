from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView

from newsletter.forms import MailForm, ClientForm, MessageForm, MailManagerForm
from newsletter.models import Mail, Client, Message


class HomePageView(TemplateView):
    template_name = 'newsletter/home.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        count = Mail.objects.count()
        is_active = Mail.objects.filter(mail_active=True).count()
        unique = Client.objects.distinct('email').count()
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


class MailCreateView(CreateView, LoginRequiredMixin):
    """ Создание рассылки """
    model = Mail
    form_class = MailForm
    success_url = reverse_lazy('newsletter:mail_list')

    def form_valid(self, form):
        mail = form.save()
        user = self.request.user
        mail.owner = user
        mail.save()
        return super().form_valid(form)


class MailUpdateView(LoginRequiredMixin, UpdateView):
    """ Редактирование данных рассылки """
    model = Mail
    form_class = MailForm
    success_url = reverse_lazy('newsletter:mail_list')

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return MailForm
        if (
                user.has_perm("mail.set_activation_mail")
                and user.has_perm("user.change_user")
                and user.has_perm("user.view_user")
                and user.has_perm("mail.view_mail")
        ):
            return MailManagerForm
        raise PermissionDenied


class MailDeleteView(DeleteView, LoginRequiredMixin):
    """ Удаление рассылки """
    model = Mail
    success_url = reverse_lazy('newsletter:mail_list')


class ClientListView(ListView):
    """ Просмотр списка клиентов """
    model = Client


class ClientDetailView(DetailView):
    """Просмотр одного клиента"""
    model = Client


class ClientCreateView(CreateView, LoginRequiredMixin):
    """Создание клиента"""
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('newsletter:client_list')

    def form_valid(self, form):
        client = form.save()
        user = self.request.user
        client.owner = user
        client.save()
        return super().form_valid(form)


class ClientUpdateView(UpdateView, LoginRequiredMixin):
    """Редактирование данных клиента"""
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('newsletter:client_list')


class ClientDeleteView(DeleteView, LoginRequiredMixin):
    """Удаление клиента"""
    model = Client
    success_url = reverse_lazy('newsletter:client_list')


class MessageListView(ListView):
    """ Просмотр списка сообщений """
    model = Message


class MessageDetailView(DetailView):
    """Просмотр деталей сообщения"""
    model = Message


class MessageCreateView(CreateView, LoginRequiredMixin):
    """Создание сообщения"""
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('newsletter:message_list')

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(UpdateView, LoginRequiredMixin):
    """Редактирование сообщения"""
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('newsletter:message_list')


class MessageDeleteView(DeleteView, LoginRequiredMixin):
    """Удаление сообщения"""
    model = Message
    success_url = reverse_lazy('newsletter:message_list')