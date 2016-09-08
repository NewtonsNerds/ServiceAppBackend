from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework_jwt.views import JSONWebTokenAPIView

from .serializers import UserRegisterSerializer, UserDetailSerializer, CustomJSONWebTokenSerializer
from .models import CustomUser


# Create your views here


@api_view(['POST'])
def register(request):
    if request.method == 'GET':
        return Response()

    elif request.method == 'POST':
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def detail(request, pk):
    try:
        user = CustomUser.objects.get(pk=pk)
    except CustomUser.DoesNotExist:
        return Response({"message": "No user found"},
                        status=status.HTTP_404_NOT_FOUND, )

    if request.method == 'GET':
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)


class GetJSONWebToken(JSONWebTokenAPIView):
    """
    API View that receives a POST with a user's username and password.

    Returns a JSON Web Token that can be used for authenticated requests.
    """
    serializer_class = CustomJSONWebTokenSerializer
