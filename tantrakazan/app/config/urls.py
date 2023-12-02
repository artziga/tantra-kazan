"""
URL configuration for tantrakazan project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from config import settings
from django.conf.urls.static import static

from config.utils import TagAutocomplete

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('main.urls')),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
    path('accounts/', include('accounts.urls')),
    path('users/', include('users.urls')),
    path('specialists/', include('specialists.urls')),
    path('listings/', include('listings.urls')),
    path('gallery/', include('gallery.urls')),
    path('feedback/', include('feedback.urls')),
    path('articles/', include('articles.urls')),
    path('tag-autocomplete/', TagAutocomplete.as_view(), name='tag_autocomplete'),
    path("__debug__/", include("debug_toolbar.urls")),
    # path('silk/', include('silk.urls', namespace='silk'))

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


