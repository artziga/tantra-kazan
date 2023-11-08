from django.urls import path
from main.views import IndexListView, SearchView, ContactUsView

app_name = 'main'

urlpatterns = [
    path('', IndexListView.as_view(), name='home'),
    path('search/', SearchView.as_view(), name='search_results'),
    path('contact_us/', ContactUsView.as_view(), name='contact-us')
]
