from django.urls import path
from gallery import views

app_name = 'gallery'

urlpatterns = [
    path('create/', views.GalleryCreateView.as_view(), name='create_gallery'),
    path('update/<str:slug>', views.GalleryUpdateView.as_view(), name='update_gallery'),
    path('delete/<str:slug>', views.GalleryDeleteView.as_view(), name='delete_gallery'),
    path('<str:slug>/add_photos/', views.AddPhotosView.as_view(), name='add_photos'),
    path('<str:slug>/', views.GalleryDetailView.as_view(), name='gallery'),
    path('photo/<str:slug>/', views.PhotoDetailView.as_view(), name='photo'),
    path('photo/update/<str:slug>/', views.PhotoUpdateView.as_view(), name='update_photo_description'),
    path('photo/delete/<str:slug>', views.PhotoDeleteView.as_view(), name='delete_photo'),

]