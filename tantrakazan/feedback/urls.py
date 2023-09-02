from django.urls import path
from feedback.views import AddCommentView, DeleteCommentView

app_name = 'feedback'

urlpatterns = [
    path('<str:from_user>/', AddCommentView.as_view(), name='add_comment'),
    path('<str:from_user>/<int:parent_comment_id>/', AddCommentView.as_view(), name='add_comment_with_parent'),
    path('delete/<int:pk>', DeleteCommentView.as_view(), name='delete_comment')

]

