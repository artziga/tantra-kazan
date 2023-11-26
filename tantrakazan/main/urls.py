from django.urls import path
from main.views import index, SearchView, ContactUsView

app_name = 'main'

urlpatterns = [
    path('', index, name='index'),
    path('search/', SearchView.as_view(), name='search_results'),
    path('contact_us/', ContactUsView.as_view(), name='contact-us')
]
