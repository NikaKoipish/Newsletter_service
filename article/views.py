from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy, reverse

from article.forms import ArticleManagerForm
from article.models import Article
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView


class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleManagerForm
    success_url = reverse_lazy('article:articles')


class ArticleUpdateView(PermissionRequiredMixin,UpdateView):
    model = Article
    form_class = ArticleManagerForm
    permission_required = 'article.change_article'
    success_url = reverse_lazy('article:articles')

    def get_success_url(self):
        return reverse('article:article_detail', args=[self.kwargs.get('pk')])


class ArticleDeleteView(PermissionRequiredMixin, DeleteView):
    model = Article
    permission_required = 'article.delete_article'
    success_url = reverse_lazy('article:articles')


class ArticleListView(ListView):
    model = Article
    template_name = 'article/articles_list.html'


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article/article_detail.html'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.view_count += 1
        self.object.save()
        return self.object
