import datetime

from braces.views import LoginRequiredMixin

from django.views.generic import CreateView, UpdateView, DetailView, DeleteView

from articles.forms import ArticleForm
from articles.models import Article
from config.utils import DataMixin


class ArticleDetailView(LoginRequiredMixin, DataMixin, DetailView):
    model = Article
    title = 'статья'

    def get_context_data(self, **kwargs):
        return super().get_context_data() | self.get_user_context()


class ArticleCreateView(LoginRequiredMixin, DataMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'articles/create_article.html'
    success_url = '/'

    def form_valid(self, form):
        article = form.save(commit=False)
        article.author = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, DataMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'articles/create_article.html'
    success_url = '/'

    def form_valid(self, form):
        article = form.save(commit=False)
        article.last_update = datetime.datetime.now()
        return super().form_valid(form)


class ArticleDeleteView(LoginRequiredMixin, DataMixin, DeleteView):
    model = Article
