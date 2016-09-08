from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, CustomJSONWebTokenSerializer
from rest_framework import status
from rest_framework_jwt.views import JSONWebTokenAPIView


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


class GetJSONWebToken(JSONWebTokenAPIView):
    """
    API View that receives a POST with a user's username and password.

    Returns a JSON Web Token that can be used for authenticated requests.
    """
    serializer_class = CustomJSONWebTokenSerializer
