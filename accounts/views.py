from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import User

# Create your views here.


@api_view(['POST'])
def register(request):
    pass