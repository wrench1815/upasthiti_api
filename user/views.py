import logging
import random
import string

from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from drf_spectacular.types import OpenApiTypes

from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter

from django_filters.rest_framework import DjangoFilterBackend

from .serializers import HODSerializer, PrincipalSerializer, UserSerializer, UserCreateSerializer, UserUpdateSerializer, UserPasswordSerializer
from .permissions import UserIsAdmin
from .filters import HODFilter

from api.paginator import StandardPagination

from college.models import CollegeModel

User = get_user_model()
logger = logging.getLogger(__name__)


@extend_schema_view(
    post=extend_schema(
        request=UserCreateSerializer,
        responses={
            #? 201
            status.HTTP_201_CREATED:
            OpenApiResponse(
                description='User Created Successfully',
                response=UserSerializer,
            ),
            #? 400
            status.HTTP_400_BAD_REQUEST:
            OpenApiResponse(
                description='Bad Request',
                response=OpenApiTypes.OBJECT,
            ),
        },
        description='Create a new user.'),
    get=extend_schema(
        request=UserSerializer,
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(
                description='Users List',
                response=UserSerializer,
            ),
            #? 400
            status.HTTP_400_BAD_REQUEST:
            OpenApiResponse(
                description='Bad Request',
                response=OpenApiTypes.OBJECT,
            ),
        },
        description='Returns list of all Users.'),
)
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
    pagination_class = StandardPagination
    filter_backends = [OrderingFilter]
    ordering_fields = 'date_added'
    ordering = '-date_added'

    #? Create a new User
    def post(self, request, *args, **kwargs):
        if 'password' not in request.data or not request.data['password']:
            #? Generate a random password
            pwd_1 = ''.join(
                random.choice(string.ascii_lowercase) for _ in range(3))
            pwd_2 = ''.join(
                random.choice(string.ascii_uppercase) for _ in range(3))
            pwd_3 = ''.join(random.choice(string.digits) for _ in range(3))
            pwd_4 = ''.join(random.choice('!@#$%^&*()') for _ in range(3))
            pwd = pwd_1 + pwd_2 + pwd_3 + pwd_4
            pwd = list(pwd)

            random.shuffle(pwd)
            pwd = ''.join(pwd)

            request.data['password'] = pwd
            request.data['confirm_password'] = pwd

        serializer = UserCreateSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = None
        college = None

        try:
            #? check if the college passed in case of teacher exist or not
            if serializer.validated_data['is_teacher']:
                try:
                    college = CollegeModel.objects.get(
                        id=serializer.validated_data['college'])
                except CollegeModel.DoesNotExist:
                    response = {
                        'college': 'The College does not exist, Try Again.'
                    }

                    logger.warning(response)

                    return Response(
                        response,
                        status=status.HTTP_404_NOT_FOUND,
                    )

            user = User.objects.create_user(
                profile_image=serializer.validated_data['profile_image'],
                profile_image_public_id=serializer.
                validated_data['profile_image_public_id'],
                first_name=serializer.validated_data['first_name'],
                last_name=serializer.validated_data['last_name'],
                email=serializer.validated_data['email'],
                mobile=serializer.validated_data['mobile'],
                district=serializer.validated_data['district'],
                address=serializer.validated_data['address'],
                gender=serializer.validated_data['gender'],
                password=serializer.validated_data['password'],
                is_admin=serializer.validated_data['is_admin'],
                is_principal=serializer.validated_data['is_principal'],
                is_hod=serializer.validated_data['is_hod'],
                is_teacher=serializer.validated_data['is_teacher'],
            )

            logger.info("User Saved Successfully")

            #? if user created is a teacher, then assign the College passed in request
            if user.is_teacher:
                user.college_teacher.add(college)  #? reverse relation

                logger.info("User(Teacher) assigned to the College")

            #? send email to user
            subject = 'Welcome to Upasthiti'
            message = f'Hello {user.first_name},\n\nWelcome to Upasthiti.\n\nYour login credentials are:\n\nEmail: {user.email}\nPassword: {request.data["password"]}\n\nRegards,\nUpasthiti'

            user.email_user(subject, message)

            #? if development environment, log password
            if settings.DEBUG:
                logger.info(
                    f'>>>>>>>>>>>>>>>>>>>>>>>>>>> password for user {request.data["email"]} is {request.data["password"]} <<<<<<<<<<<<<<<<<<<<<<<<<<<'
                )
                logger.info(message)

        except Exception as ex:
            logger.error(str(ex))

            return Response({'detail': str(ex)},
                            status=status.HTTP_400_BAD_REQUEST)

        response = UserSerializer(user)
        logger.info('User Created Successfully')

        #? return created user
        return Response(response.data, status=status.HTTP_201_CREATED)


@extend_schema_view(
    get=extend_schema(
        description=
        'Returns Single User registered on Application of given Id.\n\nargs: pk',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(
                description='User Details',
                response=UserSerializer,
            ),
            #? 404
            status.HTTP_404_NOT_FOUND:
            OpenApiResponse(
                description='Not found',
                response=OpenApiTypes.OBJECT,
            ),
            #? 400
            status.HTTP_400_BAD_REQUEST:
            OpenApiResponse(
                description='Bad Request',
                response=OpenApiTypes.OBJECT,
            ),
        }),
    patch=extend_schema(
        request=UserUpdateSerializer,
        description=
        'Updates the User of given Id with the provided Data.\n\nargs: pk',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(description='User Updated Successfully', ),
            #? 404
            status.HTTP_404_NOT_FOUND:
            OpenApiResponse(
                description='Not found',
                response=OpenApiTypes.OBJECT,
            ),
            #? 400
            status.HTTP_400_BAD_REQUEST:
            OpenApiResponse(
                description='Bad Request',
                response=OpenApiTypes.OBJECT,
            ),
        }),
    delete=extend_schema(
        description='Deletes the User of the given Id.\n\nargs: pk',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(description='User Deleted Successfully', ),
            #? 404
            status.HTTP_404_NOT_FOUND:
            OpenApiResponse(
                description='Not found',
                response=OpenApiTypes.OBJECT,
            ),
            #? 400
            status.HTTP_400_BAD_REQUEST:
            OpenApiResponse(
                description='Bad Request',
                response=OpenApiTypes.OBJECT,
            ),
        }),
)
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
    def get(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UserSerializer(user)
        return Response(serializer.data)

    #? Update User of given Id
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
    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()

        response = {'detail': 'User Deleted Successfully'}
        logger.info(response)

        return Response(response, status=status.HTTP_200_OK)


@extend_schema_view(
    post=extend_schema(
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(
                description='User Password Updated Successfully', ),

            #? 404
            status.HTTP_404_NOT_FOUND:
            OpenApiResponse(
                description='User not found',
                response=OpenApiTypes.OBJECT,
            ),

            #? 400
            status.HTTP_400_BAD_REQUEST:
            OpenApiResponse(
                description='Bad Request',
                response=OpenApiTypes.OBJECT,
            ),
        },
        operation_id='user_password_update'), )
class UserPasswordUpdateAPIView(generics.GenericAPIView):
    '''
        Updates the Password of User of given Id.

        Accessible by: Admin
    '''
    queryset = User.objects.all()
    serializer_class = UserPasswordSerializer
    permission_classes = [permissions.IsAuthenticated & (UserIsAdmin)]
    lookup_field = 'pk'

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        #? find user by id and return 404 if not found
        user = self.get_object()

        user.set_password(serializer.validated_data['password'])
        user.save()

        response = {'detail': 'Password Updated Successfully'}
        logger.info(response)

        return Response(response, status=status.HTTP_200_OK)


@extend_schema_view(
    get=extend_schema(
        description='Returns list of all Admin Users.',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(
                description='Admin List',
                response=UserSerializer,
            ),
            #? 400
            status.HTTP_400_BAD_REQUEST:
            OpenApiResponse(
                description='Bad Request',
                response=OpenApiTypes.OBJECT,
            ),
        }), )
class UsersAdminListAPIView(generics.ListAPIView):
    '''
        returns all Admin Users

        Accessible by: Admin
    '''
    queryset = User.objects.filter(is_admin=True)
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated & (UserIsAdmin)]
    lookup_field = 'pk'
    pagination_class = StandardPagination
    filter_backends = [OrderingFilter]
    ordering_fields = 'date_added'
    ordering = '-date_added'


@extend_schema_view(
    get=extend_schema(
        description='Returns list of all Principal Users.',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(
                description='Admin List',
                response=PrincipalSerializer,
            ),
            #? 400
            status.HTTP_400_BAD_REQUEST:
            OpenApiResponse(
                description='Bad Request',
                response=OpenApiTypes.OBJECT,
            ),
        }), )
class UsersPrincipalListAPIView(generics.ListAPIView):
    '''
        returns all Principal Users

        Accessible by: Admin
    '''
    queryset = User.objects.filter(is_principal=True)
    serializer_class = PrincipalSerializer
    permission_classes = [permissions.IsAuthenticated & (UserIsAdmin)]
    lookup_field = 'pk'
    pagination_class = StandardPagination
    filter_backends = [OrderingFilter]
    ordering_fields = 'date_added'
    ordering = '-date_added'


@extend_schema_view(
    get=extend_schema(
        description='Returns list of all Teacher Users.',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(
                description='Admin List',
                response=UserSerializer,
            ),
            #? 400
            status.HTTP_400_BAD_REQUEST:
            OpenApiResponse(
                description='Bad Request',
                response=OpenApiTypes.OBJECT,
            ),
        }), )
class UsersTeacherListAPIView(generics.ListAPIView):
    '''
        returns all Teacher Users

        Accessible by: Admin
    '''
    queryset = User.objects.filter(is_teacher=True)
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated & (UserIsAdmin)]
    lookup_field = 'pk'
    pagination_class = StandardPagination
    filter_backends = [OrderingFilter]
    ordering_fields = 'date_added'
    ordering = '-date_added'


@extend_schema_view(
    get=extend_schema(
        description=
        'Returns list of HoD Users.\n\nFilters:\n\n- unassigned\n\n- exclude_college',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(
                description='HOD List',
                response=HODSerializer,
            ),
            #? 400
            status.HTTP_400_BAD_REQUEST:
            OpenApiResponse(
                description='Bad Request',
                response=OpenApiTypes.OBJECT,
            ),
        }), )
class UsersHodListAPIView(generics.ListAPIView):
    '''
        returns all HOD Users

        Accessible by: Admin
    '''
    queryset = User.objects.filter(is_hod=True)
    serializer_class = HODSerializer
    permission_classes = [permissions.IsAuthenticated & (UserIsAdmin)]
    lookup_field = 'pk'
    pagination_class = StandardPagination
    filter_backends = [
        OrderingFilter,
        DjangoFilterBackend,
    ]
    ordering_fields = 'date_added'
    ordering = '-date_added'
    filterset_class = HODFilter
