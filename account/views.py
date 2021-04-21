from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegistrationSerializer, CustomLoginSerializer, CreateNewPasswordSerializer
from rest_framework import status
from rest_framework.generics import get_object_or_404
from .models import MyUser
from .utils import send_activation_email

class RegistrationView(APIView):
    def post(self, request):
        data = request.data
        serializer = RegistrationSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Successfully registered', status = status.HTTP_200_OK)
        return Response('Not valid info', status=status.HTTP_400_BAD_REQUEST)


class ActivationView(APIView):
    def get(self, request, activation_code):
        user = get_object_or_404(MyUser, activation_code=activation_code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response('Successfully activated')


class LoginView(ObtainAuthToken):
    serializer_class = CustomLoginSerializer


#api/v1/account/forgot_password/
class ForgotPassword(APIView):
    def get(self, request):
        email = request.query_params.get('email')
        print(email)
        user = get_object_or_404(MyUser, email=email)
        user.is_active = False
        user.create_activation_code()
        user.save()
        send_activation_email(email=email, activation_code=user.activation_code, is_password=True)
        return Response('Activation code has been sent to your email', status=status.HTTP_200_OK)


class ForgotPasswordComplete(APIView):
    def post(self, request):
        data = request.data
        serializer = CreateNewPasswordSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('You have successfully reset your password', status=status.HTTP_200_OK)

