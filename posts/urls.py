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
    ListCategoriesAPIView,
    ListTagsAPIView,
    PostViewSet,
)

router = DefaultRouter()
router.register(r"", PostViewSet, basename="posts")
app_name = "posts"

urlpatterns = [
    path("", include(router.urls)),
    path("<str:slug>/comment/", ListCommentsAPIView.as_view(), name="list_comments"),
    path("<str:slug>/comment/create/", CreateCommentAPIView.as_view(), name="create_comment"),
    path("<str:slug>/comment/<int:id>/", DetailCommentAPIView.as_view(), name="comment_detail"),
]
