from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserListAPIView, UserCreateAPIView, UserDetailAPIView

app_name = 'accounts'

urlpatterns = [
    path('', UserListAPIView.as_view(), name='user_list'),
    path('register/', UserCreateAPIView.as_view(), name='user_register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('<int:pk>/', UserDetailAPIView.as_view(), name='user_detail'),
]
