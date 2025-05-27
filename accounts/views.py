from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly

from .serializers import UserSerializer
from posts.permissions import IsOwner

User = get_user_model()


class UserCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer


class UserDetailAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwner]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'