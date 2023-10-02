from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.serializers import (
    CharField,
    EmailField,
    ModelSerializer,
    ValidationError,
)
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]


class UserCreationSerializer(ModelSerializer):
    """
    Serializer for user registration.

    Fields:
    - username (str): The username for the new user.
    - first_name (str): The first name of the new user.
    - last_name (str): The last name of the new user.
    - email (str): The email address of the new user.
    - password (str): The password for the new user.

    Methods:
    - validate(data): Validates the serializer data, checking if the email is unique.
    - create(validated_data): Creates a new user object.

    """

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        """
        Validate the serializer data to ensure the email is unique.

        Args:
        - data (dict): The data to be validated.

        Returns:
        - dict: The validated data.

        Raises:
        - ValidationError: If the email is already registered.
        """
        email = data["email"]
        user_qs = User.objects.filter(email=email)
        if user_qs.exists():
            raise ValidationError("This user has already registered.")
        return data

    def create(self, validated_data):
        """
        Create a new user object.

        Args:
        - validated_data (dict): The validated data for user creation.

        Returns:
        - dict: The validated data.
        """
        username = validated_data["username"]
        first_name = validated_data["first_name"]
        last_name = validated_data["last_name"]
        email = validated_data["email"]
        password = validated_data["password"]
        user_obj = User(
            username=username, email=email, first_name=first_name, last_name=last_name
        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data


class UserLoginSerializer(ModelSerializer):
    """
    Serializer for user login.

    Fields:
    - username (str): The username of the user.
    - password (str): The password for authentication.
    - token (str): A token generated for the user's session.
    - first_name (str): The first name of the user.
    - last_name (str): The last name of the user.

    Methods:
    - validate(data): Validates the user's login data.

    """

    access_token = CharField(allow_blank=True, read_only=True)
    refresh_token = CharField(allow_blank=True, read_only=True)
    first_name = CharField(read_only=True)
    last_name = CharField(read_only=True)
    username = CharField(required=True)
    role = CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            "role",
            "access_token",
            "refresh_token",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        """
        Validate the user's login data.

        Args:
        - data (dict): The data to be validated.

        Returns:
        - dict: The validated data.

        Raises:
        - ValidationError: If the provided credentials are invalid.
        """
        username = data.get("username", None)
        password = data.get("password", None)
        if not username:
            raise ValidationError("User is required to login.")
        user = User.objects.filter(Q(username=username)).distinct()
        user_obj = user.first()
        if not user_obj or not user_obj.check_password(password):
            raise ValidationError("Invalid Credentials please try again.")

        refresh = RefreshToken.for_user(user_obj)

        data["access_token"] = str(refresh.access_token)
        data["refresh_token"] = str(refresh)
        data["first_name"] = user_obj.first_name
        data["id"] = user_obj.id
        data["last_name"] = user_obj.last_name
        data["email"] = user_obj.email
        data["role"] = "admin" if user_obj.is_superuser else "candidate"

        return data


class UserUpdateSerializer(ModelSerializer):
    """
    Serializer for updating user profile.

    Fields:
    - username (str): The updated username.
    - first_name (str): The updated first name.
    - last_name (str): The updated last name.
    - email (str): The updated email address.

    Methods:
    - validate_email(value): Validates the updated email address.
    - validate_username(value): Validates the updated username.
    - update(instance, validated_data): Updates the user profile.

    """

    email = EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]

    def validate_email(self, value):
        """
        Validate the updated email address.

        Args:
        - value (str): The updated email address.

        Returns:
        - str: The validated email address.

        Raises:
        - ValidationError: If the email is already in use.
        """
        user = self.context["request"].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise ValidationError("This email is already in use.")
        return value

    def validate_username(self, value):
        """
        Validate the updated username.

        Args:
        - value (str): The updated username.

        Returns:
        - str: The validated username.

        Raises:
        - ValidationError: If the username is already in use.
        """
        user = self.context["request"].user
        print(User.objects.exclude(pk=user.pk).filter(username=value))
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise ValidationError("This username is already in use.")
        return value

    def update(self, instance, validated_data):
        """
        Update the user profile.

        Args:
        - instance (User): The user object to be updated.
        - validated_data (dict): The validated data for updating the user profile.

        Returns:
        - User: The updated user object.
        """
        instance.first_name = validated_data["first_name"]
        instance.last_name = validated_data["last_name"]
        instance.email = validated_data["email"]
        instance.username = validated_data["username"]
        instance.save()
        return instance
