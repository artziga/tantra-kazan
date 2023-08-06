from django.urls import path
from main.views import IndexListView

app_name = 'main'

urlpatterns = [
    path('', IndexListView.as_view(), name='home')
]
