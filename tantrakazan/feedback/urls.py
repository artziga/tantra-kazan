from django.urls import path
from feedback.views import AddCommentView, DeleteCommentView, PutLikeView, BookmarkView

app_name = 'feedback'

urlpatterns = [
    path('<str:from_user>/', AddCommentView.as_view(), name='add_comment'),
    path('delete/<int:pk>/', DeleteCommentView.as_view(), name='delete_comment'),
    path('<str:from_user>/<int:parent_comment_id>/', AddCommentView.as_view(), name='add_comment_with_parent'),

    path('bookmark/<int:obj_pk>/<int:content_type_id>/', BookmarkView.as_view(), name='bookmark'),
]

