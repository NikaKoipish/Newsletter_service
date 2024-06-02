from django.urls import path
from django.views.decorators.cache import cache_page, never_cache

from article.views import ArticleCreateView, ArticleListView, ArticleDetailView, ArticleUpdateView, ArticleDeleteView
from article.apps import ArticleConfig
app_name = ArticleConfig.name
urlpatterns = [
    path('articles/create/', never_cache(ArticleCreateView.as_view()), name="create_article"),
    path('articles/update/<int:pk>/', never_cache(ArticleUpdateView.as_view()), name="update_article"),
    path('articles/', ArticleListView.as_view(), name="articles"),
    path('articles/<int:pk>/', cache_page(60)(ArticleDetailView.as_view()), name="article_detail"),
    path('articles/delete/<int:pk>/', ArticleDeleteView.as_view(), name="delete_article"),

]