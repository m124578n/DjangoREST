from rest_framework import viewsets
from .models import ToDoList
from django.contrib.auth.models import User
from rest_framework.response import Response
from .serializers import ToDoListSerializer, UserSerializer, UserRegisterSerializer, UserLoginSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import IsOwner
from drf_spectacular.utils import extend_schema
from rest_framework.generics import GenericAPIView


class HelloView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="hello",
        request=None,
        responses={200: None},
    )
    def get(self, request):
        return Response({'message':'success'})

class RegisterView(APIView):
    @extend_schema(
        summary="register",
        request=UserRegisterSerializer,
        responses={201: UserRegisterSerializer},
    )
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user_serializer = UserRegisterSerializer(user)
            return Response(
                {
                    'message':'register success',
                    'user':user_serializer.data,    
                },
                status=status.HTTP_201_CREATED,
                )
        else:
            errors = serializer.errors
            return Response(
                {
                    'message':'Bad request',
                    'errors':errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
                )

class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]

            user = authenticate(request, username=username, password=password)

            if user:
                refresh = RefreshToken.for_user(user)
                payload = {"user_id": user.id, "username": user.username}
                access_token = refresh.access_token
                access_token["payload"] = payload

                return Response(
                    {
                        "message": "User logged in successfully.",
                        "access_token": str(access_token),
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"message": "Invalid credentials."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        else:
            errors = serializer.errors
            return Response(
                {"message": "Bad Request.", "errors": errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

class ToDoListViewset(viewsets.ModelViewSet):
    permission_classes = [IsOwner]
    queryset = ToDoList.objects.all()
    serializer_class = ToDoListSerializer

class UserViewset(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
