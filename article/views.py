from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy, reverse

from article.forms import ArticleManagerForm
from article.models import Article
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView


class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleManagerForm
    success_url = reverse_lazy('article:articles')


class ArticleUpdateView(UpdateView):
    model = Article
    form_class = ArticleManagerForm
    success_url = reverse_lazy('article:articles')

    def get_success_url(self):
        return reverse('article:article_detail', args=[self.kwargs.get('pk')])

    def get_form_class(self):
        user = self.request.user
        if user.has_perm("article.change_article"):
            return ArticleManagerForm
        raise PermissionDenied


class ArticleDeleteView(DeleteView):
    model = Article
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
