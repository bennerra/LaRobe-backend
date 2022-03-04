from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, NOT
from rest_framework.response import Response

from auth_server.models import User
from auth_server.serializers import UserSerializer, ProfileSerializer


class RegistrationViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    PERMISSION_CLASSES = (
        AllowAny,
    )
    basename = "user"

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.kwargs.get("pk"):
            return User.objects.filter(id=self.kwargs.get("pk")).first()
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_queryset()
        if not instance:
            return Response(status=status.HTTP_404_NOT_FOUND, data="User does not exist")

        serializer = self.serializer_class(instance)
        return Response(serializer.data)