from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from home.api.v1.serializers import (
    SignupSerializer,
    UserSerializer, NormalSignupSerializer, UserProfileSerializer,
)
from modules.django_two_factor_authentication.two_factor_authentication.models import TwoFactorAuth
from users.models import UserProfile


class SignupViewSet(ModelViewSet):
    serializer_class = SignupSerializer
    http_method_names = ["post"]
    permission_classes = [AllowAny]


class NormalSignupViewSet(ModelViewSet):
    serializer_class = NormalSignupSerializer
    http_method_names = ["post"]
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        TwoFactorAuth.objects.get_or_create(email=validated_data.get('email'))
        return Response("Email Registered Successfully")


class LoginViewSet(ViewSet):
    """Based on rest_framework.authtoken.views.ObtainAuthToken"""

    serializer_class = AuthTokenSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = UserSerializer(user)
        return Response({"token": token.key, "user": user_serializer.data})


class UserProfileViewSet(ModelViewSet):
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=["post"], detail=False, url_path="accept-mission-statement", permission_classes=[IsAuthenticated])
    def accept_mission_statement(self, request, pk=None):
        self.request.user.is_mission_statement_accepted = True
        self.request.user.save()
        return Response("Accepted")

    @action(methods=["post"], detail=False, url_path="accept-payment-terms", permission_classes=[IsAuthenticated])
    def accept_payment_terms(self, request, pk=None):
        self.request.user.is_payment_terms_accepted = True
        self.request.user.save()
        return Response("Accepted")
