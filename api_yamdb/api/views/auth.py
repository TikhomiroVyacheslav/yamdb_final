from api.serializers.auth import UserSignUpSerializer, UserTokenSerializer
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


class SignUpViewSet(CreateAPIView):
    serializer_class = UserSignUpSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = UserSignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.send_mail_with_confirmation_code()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class TokenViewSet(CreateAPIView):
    serializer_class = UserTokenSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = UserTokenSerializer(data=request.data)
        if serializer.is_valid():
            data = {'token': serializer.user.get_token()}
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
