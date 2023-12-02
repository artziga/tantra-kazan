from django.urls import path
from articles.views import ArticleCreateView, ArticleDeleteView, ArticleUpdateView, ArticleDetailView

app_name = 'articles'

urlpatterns = [
    path('create/', ArticleCreateView.as_view(), name='create_article'),
    path('show/<slug:slug>', ArticleDetailView.as_view(), name='article'),
    path('update/<slug:slug>', ArticleUpdateView.as_view(), name='update_article'),
    path('delete/<slug:slug>', ArticleDeleteView.as_view(), name='delete_article')
]
