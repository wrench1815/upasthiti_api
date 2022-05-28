import logging
from django.contrib.auth import get_user_model

from rest_framework import generics, permissions, status
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema

from .serializers import UserSerializer, UserCreateSerializer
from .permissions import UserIsAdmin

User = get_user_model()
logger = logging.getLogger(__name__)


class UserListCreateAPIView(generics.ListCreateAPIView):
    '''
        Allowed methods: GET, POST

        GET: Returns list of all Users
        POST: Creates a new User

        Accessible by: Admin
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated & (UserIsAdmin)]

    @extend_schema(request=UserCreateSerializer,
                   responses=UserCreateSerializer)
    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data['password'] != serializer.validated_data[
                'confirm_password']:
            response = {'detail': 'Confirm Password does not match Password'}
            logger.error(response)

            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        try:
            User.objects.get_or_create(
                first_name=serializer.validated_data['first_name'],
                last_name=serializer.validated_data['last_name'],
                email=serializer.validated_data['email'],
                gender=serializer.validated_data['gender'],
                password=serializer.validated_data['password'])

        except Exception as ex:
            logger.error(str(ex))

            return Response({'detail': str(ex)},
                            status=status.HTTP_400_BAD_REQUEST)

        response = {'detail': 'User Created Successfully'}
        logger.info(response)

        return Response(response, status=status.HTTP_201_CREATED)


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
