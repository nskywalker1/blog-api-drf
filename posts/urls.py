from django.urls import path
from .views import (
    CreatePostAPIView,
    ListPostsAPIView,
    DetailPostAPIView,
    CreateCommentAPIView,
    ListCommentsAPIView,
    DetailCommentAPIView,
)

app_name = "posts"

urlpatterns = [
    path("", ListPostsAPIView.as_view(), name="list_post"),
    path("create/", CreatePostAPIView.as_view(), name="create_post"),
    path("<str:slug>/", DetailPostAPIView.as_view(), name="post_detail"),
    path("<str:slug>/comment/", ListCommentsAPIView.as_view(), name="list_comments"),
    path("<str:slug>/comment/create/", CreateCommentAPIView.as_view(), name="create_comment"),
    path("<str:slug>/comment/<int:id>/", DetailCommentAPIView.as_view(), name="comment_detail"),
]
