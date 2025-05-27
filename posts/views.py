from django.shortcuts import get_object_or_404
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework import filters
from .models import Post, Comment, Category, Tag
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from .serializers import (
    PostCreateUpdateSerializer,
    PostListSerializer,
    PostDetailSerializer,
    CommentCreateUpdateSerializer,
    CommentSerializer,
    CategorySerializer,
    TagSerializer
)
from .pagination import PostLimitOffsetPagination
from .permissions import IsOwnerOrReadOnly
from .mixins import MultipleFieldLookupMixin


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
    pagination_class = PostLimitOffsetPagination
    lookup_field = 'slug'

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category__slug', 'tags__slug']
    search_fields = ['title']

    @action(detail=False, methods=['GET'])
    def categories(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def tags(self, request):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        elif self.action == 'retrieve':
            return PostDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return PostCreateUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# class CreatePostAPIView(APIView):
#     queryset = Post.objects.all()
#     authentication_classes = [JWTAuthentication]
#     serializer_class = PostCreateUpdateSerializer
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request, *args, **kwargs):
#         serializer = PostCreateUpdateSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save(author=request.user)
#             return Response(serializer.data, status=200)
#         else:
#             return Response({"errors": serializer.errors}, status=400)
#
#
# class ListPostsAPIView(ListAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostListSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     pagination_class = PostLimitOffsetPagination
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['title']
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         category = self.request.query_params.get('category', None)
#         if category:
#             queryset = queryset.filter(category__slug=category)
#
#         tags = self.request.query_params.get('tags', None)
#         if tags:
#             tag_list = tags.split(',')
#             queryset = queryset.filter(tags__slug__in=tag_list).distinct()
#
#         return queryset
#
#
# class DetailPostAPIView(RetrieveUpdateDestroyAPIView):
#     queryset = Post.objects.all()
#     lookup_field = 'slug'
#     serializer_class = PostDetailSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class CreateCommentAPIView(APIView):
    serializer_class = CommentCreateUpdateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        serializer = CommentCreateUpdateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=200)
        else:
            return Response({"errors": serializer.errors}, status=400)


class ListCommentsAPIView(ListAPIView):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        comments = Comment.objects.filter(post=post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=200)


class DetailCommentAPIView(MultipleFieldLookupMixin, RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    queryset = Comment.objects.all()
    lookup_field = ["post", "id"]
    serializer_class = CommentCreateUpdateSerializer


class ListCategoriesAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ListTagsAPIView(ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
