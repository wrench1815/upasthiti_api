import logging

from drf_spectacular.utils import OpenApiResponse, extend_schema

from django.contrib.auth import get_user_model

from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .serializers import UserSerializer, UserCreateSerializer, UserUpdateSerializer, UserPasswordSerializer
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

    #? Create a new User
    @extend_schema(request=UserCreateSerializer,
                   responses=UserCreateSerializer)
    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

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


class UserRetrieveUpdateDestroyAPIView(generics.GenericAPIView):
    '''
        Allowed methods: GET, PATCH, DELETE

        GET: Return User of given Id
        PATCH: Update User of given Id with Validated data provided
        DELETE: Delete User of given Id

        Note: Updatation on User is done via Partial Update method

        args: pk
        
        Accessible by: Admin
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated & (UserIsAdmin)]
    lookup_field = 'pk'

    #? get single User
    @extend_schema(
        description=
        'Returns Single User registered on Application of given Id.\n\nargs: pk\n\nAccessible by: Admin',
        responses={
            #? 200
            status.HTTP_200_OK:
            UserSerializer,
            #? 404
            status.HTTP_404_NOT_FOUND:
            OpenApiResponse(description='Not found')
        })
    def get(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UserSerializer(user)
        return Response(serializer.data)

    #? Update User of given Id
    @extend_schema(
        request=UserUpdateSerializer,
        description=
        'Updates the User of given Id with the provided Data.\n\nargs: pk\n\nAccessible by: Admin',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(description='User Updated Successfully'),
            #? 404
            status.HTTP_404_NOT_FOUND:
            OpenApiResponse(description='Not found')
        })
    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UserUpdateSerializer(user,
                                          data=request.data,
                                          partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = {'detail': 'User Updated Successfully'}
        logger.info(response)

        return Response(response, status=status.HTTP_200_OK)

    #? Delete User of given Id
    @extend_schema(
        description=
        'Deletes the User of the given Id.\n\nargs: pk\n\nAccessible by: Admin',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(description='User Deleted Successfully'),
            #? 404
            status.HTTP_404_NOT_FOUND:
            OpenApiResponse(description='Not found')
        })
    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()

        response = {'detail': 'User Deleted Successfully'}
        logger.info(response)

        return Response(response, status=status.HTTP_200_OK)


class UserPasswordUpdateAPIView(generics.GenericAPIView):
    '''
        Updates the Password of User of given Id.

        Accessible by: Admin
    '''
    queryset = User.objects.all()
    serializer_class = UserPasswordSerializer
    permission_classes = [permissions.IsAuthenticated & (UserIsAdmin)]
    lookup_field = 'pk'

    @extend_schema(
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(description='User Password Updated Successfully'),

            #? 404
            status.HTTP_404_NOT_FOUND:
            OpenApiResponse(description='User not found'),

            #? 400
            status.HTTP_400_BAD_REQUEST:
            OpenApiResponse(
                description='Confirm Password does not match Password')
        },
        operation_id='user_password_update')
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(pk=serializer.validated_data['id'])

        if user is None:
            response = {'detail': 'User not found'}
            logger.error(response)

            return Response(response, status=status.HTTP_404_NOT_FOUND)

        user.set_password(serializer.validated_data['password'])
        user.save()

        response = {'detail': 'Password Updated Successfully'}
        logger.info(response)

        return Response(response, status=status.HTTP_200_OK)
