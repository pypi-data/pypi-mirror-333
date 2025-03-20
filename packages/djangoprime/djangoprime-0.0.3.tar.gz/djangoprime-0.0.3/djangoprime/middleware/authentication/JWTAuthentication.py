from typing import Optional, Tuple

from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication as SimpleJWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.utils import get_md5_hash_password

# Access the JWT_AUTH_MODEL from settings, or use None if not defined
JWT_AUTH_MODEL = getattr(settings, 'JWT_AUTH_MODEL', None)


class JWTAuthentication(SimpleJWTAuthentication):
    """
    Custom JWT Authentication class that allows the use of a custom user model for authentication.

    This class checks if a custom model is specified in settings.py (`JWT_AUTH_MODEL`) and uses it for authentication.
    If no custom model is specified, it defaults to using the standard Django User model.

    Attributes:
        user_model: The user model to use for authentication.
                    It is either the custom model specified in `JWT_AUTH_MODEL` or the default Django `User` model.
    """

    def __init__(self, *args, **kwargs) -> None:
        """
        Initializes the custom JWT Authentication class by selecting the user model based on settings.

        - If `JWT_AUTH_MODEL` is defined in settings.py, the custom model is used.
        - If `JWT_AUTH_MODEL` is not defined, it defaults to Django's `get_user_model()`.

        Args:
            *args: Variable length argument list.
            **kwargs: Keyword arguments for the parent class.
        """
        super().__init__(*args, **kwargs)
        # Dynamically select the user model to use for authentication
        self.user_model = get_user_model() if not JWT_AUTH_MODEL else apps.get_model(JWT_AUTH_MODEL)

    def authenticate(self, request: Request) -> Optional[Tuple]:
        """
        Override the default authentication method to authenticate using either a custom user model
        or the default Django user model.

        Args:
            request (Request): The incoming HTTP request containing the JWT token.

        Returns:
            Optional[Tuple]: A tuple of (user, validated_token) if authentication succeeds,
                              or None if the token is invalid or missing.
        """
        # Extract token from the request header
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        # Validate the token
        try:
            validated_token = self.get_validated_token(raw_token)
        except InvalidToken:
            raise AuthenticationFailed(_("Invalid token."), code="invalid_token")

        # Get the user associated with the validated token
        return self.get_user(validated_token), validated_token

    def get_user(self, validated_token: Token):
        """
        Retrieves and validates the user associated with the given validated token.

        Args:
            validated_token (Token): The validated JWT token.

        Returns:
            user (User): The user object retrieved from the database.

        Raises:
            AuthenticationFailed: If the user is not found or fails validation.
        """
        try:
            # Extract user ID from token
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            raise InvalidToken(_("Token contains no recognizable user identification"))

        try:
            # Get the user from the database using the user ID claim
            user = self.user_model.objects.get(**{api_settings.USER_ID_FIELD: user_id})
        except self.user_model.DoesNotExist:
            raise AuthenticationFailed(_("User not found"), code="user__not__found")

        # Check if the user is active
        if not user.is_active:
            raise AuthenticationFailed(_("User is inactive"), code="user__inactive")

        # Check if the token has been revoked (if token revocation is enabled)
        if api_settings.CHECK_REVOKE_TOKEN:
            if validated_token.get(api_settings.REVOKE_TOKEN_CLAIM) != get_md5_hash_password(user.password):
                raise AuthenticationFailed(
                    _("The user's password has been changed."), code="password__changed"
                )

        return user
