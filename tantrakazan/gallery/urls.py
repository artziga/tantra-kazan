from django.urls import path
from gallery import views

app_name = 'gallery'

urlpatterns = [
    path('create/', views.CreateGalleryView.as_view(), name='create_gallery'),
    path('<str:slug>/add_photos/', views.AddPhotosView.as_view(), name='add_photos'),
    path('<str:slug>/', views.GalleryDetailView.as_view(), name='gallery'),

]