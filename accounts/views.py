from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework_jwt.views import JSONWebTokenAPIView

from .serializers import (UserRegisterSerializer,
                          UserDetailSerializer,
                          CustomJSONWebTokenSerializer,
                          UpdatePasswordSerializer,
                          ForgotPasswordRequestSerializer,
                          ForgotPasswordChangeSerializer,
                          UserLoginSerializer)


from .models import CustomUser

from django.conf.global_settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail
from django.template import loader
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import render
from django.http import HttpResponse


# Create your views here


@api_view(['POST'])
@permission_classes((AllowAny,))
def register(request):
    if request.method == 'POST':
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((AllowAny, ))
def login(request):
    if request.method == 'POST':
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def detail(request, pk):
    try:
        user = CustomUser.objects.get(pk=pk)
    except CustomUser.DoesNotExist:
        return Response({"message": "No user found"},
                        status=status.HTTP_404_NOT_FOUND, )

    if request.method == 'GET':
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)


@api_view(['PUT'])
@permission_classes((IsAuthenticated, ))
def update_password(request):
    if request.method == 'PUT':
        data = request.data
        data['email'] = request.user.email
        serializer = UpdatePasswordSerializer(request.user, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password successfully updated"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((AllowAny, ))
def forgot_password(request):
    if request.method == 'POST':
        serializer = ForgotPasswordRequestSerializer(data=request.data)
        if serializer.is_valid():
            user = CustomUser.objects.get(email=serializer.data['email'])

            c = {
                'email': user.email,
                'domain': request.META['HTTP_HOST'],
                'site_name': 'your site',
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': default_token_generator.make_token(user),
                'protocol': 'http',
            }

            email_template_name = 'accounts/forgot_password_email.html'
            email = loader.render_to_string(email_template_name, c)
            send_mail("RESET YOUR PASSWORD", email, DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
            return Response({"message": 'Email has been sent to your email address. '
                                        'Please check its inbox to continue resetting password.'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes((AllowAny, ))
def forgot_password_confirm(request, uidb64=None, token=None):
    try:
        # urlsafe_base64_decode() decodes to bytestring on Python 3
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        return Response({"error": "Error"})

    if request.method == 'GET':
        return render(request, 'accounts/forgot_password_confirm.html')

    elif request.method == 'POST':
        data = request.data
        data['email'] = user.email
        serializer = ForgotPasswordChangeSerializer(data=data)
        if serializer.is_valid():
            return HttpResponse("Changed password")
        return Response(serializer.errors)


class GetJSONWebToken(JSONWebTokenAPIView):
    """
    API View that receives a POST with a user's username and password.

    Returns a JSON Web Token that can be used for authenticated requests.
    """
    serializer_class = CustomJSONWebTokenSerializer
