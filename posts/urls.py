from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter

from .views import (
    CreatePostAPIView,
    ListPostsAPIView,
    DetailPostAPIView,
    CreateCommentAPIView,
    ListCommentsAPIView,
    DetailCommentAPIView,
    CategoryViewSet
)
router = DefaultRouter()
router.register(r'category', CategoryViewSet, basename='category')
app_name = "posts"

urlpatterns = [
    path('posts/', include(router.urls)),
    path("posts/", ListPostsAPIView.as_view(), name="list_post"),
    path("posts/create/", CreatePostAPIView.as_view(), name="create_post"),
    path("posts/<str:slug>/", DetailPostAPIView.as_view(), name="post_detail"),
    path("posts/<str:slug>/comment/", ListCommentsAPIView.as_view(), name="list_comments"),
    path("posts/<str:slug>/comment/create/", CreateCommentAPIView.as_view(), name="create_comment"),
    path("posts/<str:slug>/comment/<int:id>/", DetailCommentAPIView.as_view(), name="comment_detail"),
]
