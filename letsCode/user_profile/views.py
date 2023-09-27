from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import (
    UserCreationSerializer,
    UserLoginSerializer,
    UserUpdateSerializer,
)


class UserRegisterAPIView(CreateAPIView):
    """
    API view for user registration.
    Allows creating a new user using the UserCreationSerializer.

    Attributes:
       serializer_class (class): The serializer class for user creation.
       queryset (QuerySet): Queryset containing all User objects.
    """

    serializer_class = UserCreationSerializer
    queryset = User.objects.all()


class UserLoginAPIView(APIView):
    """
    API view for user login.
    Allows users to log in using the UserLoginSerializer.

    Attributes:
        permission_classes (list): List of permission classes, allowing any user.
        serializer_class (class): The serializer class for user login.
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        """
        Handle user login request.

        Args:
            request (Request): The HTTP request object.
            *args: Variable-length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: Response object with user data if login is successful,
                      or error response with HTTP_400_BAD_REQUEST status.
        """
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            current_user = User.objects.get(username=serializer.data["username"])
            login(request, current_user)
            print(request.user)
            return Response(new_data, status=HTTP_200_OK)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserUpdateAPIView(RetrieveUpdateAPIView):
    """
    API view for updating user information.
    Allows authenticated users to retrieve and update their own user data.

    Attributes:
        permission_classes (list): List of permission classes, requiring authentication.
        queryset (QuerySet): Queryset containing all User objects.
        serializer_class (class): The serializer class for user updates.
    """

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer

    def get_object(self):
        """
        Get the user object associated with the current request.

        Returns:
            User: The user object.
        """
        return self.request.user

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=HTTP_400_BAD_REQUEST)


class UserLogoutAPIView(APIView):
    """
    API view for user logout.
    Allows authenticated users to log out.

    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Handle user logout request.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: Response object with HTTP_200_OK status indicating successful logout.
        """
        logout(request)
        return Response("user logged out", status=HTTP_200_OK)
