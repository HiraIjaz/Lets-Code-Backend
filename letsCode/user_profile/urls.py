from django.urls import path
from .views import *

urlpatterns = [
    path('register/', UserRegisterAPIView.as_view(), name='register'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('update/', UserUpdateAPIView.as_view(), name='update'),
    path('logout/', UserLogoutAPIView.as_view(), name='logout')
]
