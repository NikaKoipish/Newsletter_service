from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from newsletter.models import Mail


class MailListView(ListView):
    model = Mail
    template_name = 'newsletter/mail_list.html'


class MailDetailView(DetailView):
    model = Mail
    template_name = 'newsletter/mail_detail.html'


class MailCreateView(CreateView):
    model = Mail
    fields = ('title', 'mail_periodicity')
    success_url = reverse_lazy('newsletter:mail_list')


class MailUpdateView(UpdateView):
    model = Mail
    fields = ('title', 'mail_periodicity')
    success_url = reverse_lazy('newsletter:mail_list')


class MailDeleteView(DeleteView):
    model = Mail
    success_url = reverse_lazy('newsletter:mail_list')
