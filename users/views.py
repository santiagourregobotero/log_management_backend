from rest_framework import generics, pagination
from django.db import transaction
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.permissions import IsAuthenticated
from common.authentication import BearerTokenAuthentication
from .serializers import UserSerializer
from .validation_serializers import LoginValidationSerializer, TokenValidationSerializer
from .models import User
from rest_framework import status
from common.utils import format_serializer_errors
from django.db.models import Q
import jwt
import datetime

class RegisterAPIView(APIView):
    parser_classes = [JSONParser]
    authentication_classes = []
    permission_classes = []

    @transaction.atomic
    def post(self, request):
        print(request)
        user_serializer = UserSerializer(data=request.data)
  
        try:
            if user_serializer.is_valid(raise_exception=True):
                user_serializer.save()
                return Response({'msg' : 'Registered successfully.'})
        except ValidationError as ve:
            return Response(format_serializer_errors(ve.detail), status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    parser_classes = [JSONParser]
    authentication_classes = []
    permission_classes = []
    
    def post(self, request):
        ser_post_data = LoginValidationSerializer(data=request.data)
        if not ser_post_data.is_valid():
            return Response(
                format_serializer_errors(ser_post_data.errors), 
                status=status.HTTP_400_BAD_REQUEST
            )

        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()
        if user is None:
            return Response({"msg": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
        if not user.check_password(password):
            return Response({"msg": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
        
        payload = {
            "id": user.id,
            "email": user.email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=60),
            "iat": datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        user_serializer = UserSerializer(user)
        return Response({"msg" : "Login successfully", 'data' : {'access_token' : token, 'user' : user_serializer.data}})


class LoginWithTokenAPIView(APIView):
    authentication_classes = []
    permission_classes = []
    
    def post(self, request):
        ser_post_data = TokenValidationSerializer(data=request.data)
        if not ser_post_data.is_valid():
            return Response(
                format_serializer_errors(ser_post_data.errors), 
                status=status.HTTP_400_BAD_REQUEST
            )

        access_token = request.data['access_token']
        payload = jwt.decode(jwt=access_token, key='secret', algorithms=['HS256'])
        user = User.objects.filter(id=payload['id']).first()
        user_serializer = UserSerializer(user)
        return Response({"msg" : "Login successfully", 'data' : {'access_token' : access_token, 'user' : user_serializer.data}})


class BasicSizePagination(pagination.PageNumberPagination):
    page_size_query_param  = 'size'


class UserListView(generics.ListAPIView):
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    pagination_class = BasicSizePagination
    serializer_class = UserSerializer
    
    def get_queryset(self):
        search = self.request.query_params.get('search')
        if search == None:
            return User.objects.all()
        
        return User.objects.filter(Q(email__contains = search))


class UserCreateView(generics.CreateAPIView):
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRUDView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileView(generics.RetrieveUpdateAPIView):
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user
