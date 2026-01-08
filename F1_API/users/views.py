from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializers import UserSerializer
from .models import User
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model


User = get_user_model()
#User SIGN-UP
class SignupView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)
    

#Login
class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        user = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=user, password=password)

        if not user:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
        token, created = Token.objects.get_or_create(user=user)
        serialzer = UserSerializer(instance=user)
        return Response({'token': token.key, 'user': serialzer.data})

class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
