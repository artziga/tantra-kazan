from django.urls import path
from main.views import IndexListView, SearchView

app_name = 'main'

urlpatterns = [
    path('', IndexListView.as_view(), name='home'),
    path('search/', SearchView.as_view(), name='search_results')
]
