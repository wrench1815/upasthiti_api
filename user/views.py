from django.contrib.auth import get_user_model

from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .serializers import UserSerializer, UserCreateSerializer
from .permissions import UserIsAdmin

User = get_user_model()


class UserListAPIView(generics.ListAPIView):
    '''
        Returns list of all Users registered on Application

        Accessible by: Admin
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated & (UserIsAdmin)]


class UserDetailAPIView(generics.RetrieveAPIView):
    '''
        Returns Single User registered on Application

        args: pk
        
        Accessible by: Admin
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated & (UserIsAdmin)]
    lookup_field = 'pk'


class UserCreateAPIView(generics.GenericAPIView):
    '''
        Creates a New User
        
        Accessible by: Admin
    '''
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.IsAuthenticated & (UserIsAdmin)]

    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data['password'] != serializer.validated_data[
                'confirm_password']:
            return Response(
                {'detail': 'Confirm Password does not match Password'},
                status=status.HTTP_400_BAD_REQUEST)
        try:
            User.objects.get_or_create(
                first_name=serializer.validated_data['first_name'],
                last_name=serializer.validated_data['last_name'],
                email=serializer.validated_data['email'],
                gender=serializer.validated_data['gender'],
                password=serializer.validated_data['password'])

        except Exception as ex:
            return Response({'detail': str(ex)},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': 'User Created Successfully'},
                        status=status.HTTP_201_CREATED)
