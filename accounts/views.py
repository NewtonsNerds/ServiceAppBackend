from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework_jwt.views import JSONWebTokenAPIView

from .serializers import UserRegisterSerializer, \
    UserDetailSerializer, \
    CustomJSONWebTokenSerializer, \
    ResetPasswordSerializer

from .models import CustomUser
from .permissions import IsOwnerOrReadOnly


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
def reset_password(request):
    if request.method == 'PUT':
        data = request.data
        data['email'] = request.user.email
        serializer = ResetPasswordSerializer(request.user, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password successfully updated"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetJSONWebToken(JSONWebTokenAPIView):
    """
    API View that receives a POST with a user's username and password.

    Returns a JSON Web Token that can be used for authenticated requests.
    """
    serializer_class = CustomJSONWebTokenSerializer
