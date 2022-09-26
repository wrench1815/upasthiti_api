import logging

from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from drf_spectacular.types import OpenApiTypes

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter

from django_filters.rest_framework import DjangoFilterBackend

from django.conf import settings

from . import serializers, models

from user.permissions import UserIsAdmin, UserIsPrincipal, UserIsHOD, UserIsTeacher

from api.paginator import StandardPagination

logger = logging.getLogger(__name__)


@extend_schema_view(
    post=extend_schema(
        request=serializers.CourseSerializer,
        responses={
            #? 201
            status.HTTP_201_CREATED:
            OpenApiResponse(
                description='Course Added Successfully',
                response=serializers.CourseSerializer,
            ),
            #? 400
            status.HTTP_400_BAD_REQUEST:
            OpenApiResponse(
                description='Bad Request',
                response=OpenApiTypes.OBJECT,
            ),
        },
        description='Creates a new Course Object.'),
    get=extend_schema(
        request=serializers.CourseFullSerializer,
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(
                description='Course List',
                response=serializers.CourseFullSerializer,
            ),
            #? 400
            status.HTTP_400_BAD_REQUEST:
            OpenApiResponse(
                description='Bad Request',
                response=OpenApiTypes.OBJECT,
            ),
        },
        description=
        'Returns list of all Courses.\n\nFilters:\n\n- is_practical\n\n- university(id)\n\nOrdering:\n\n- default: -created_on\n\n- allowed: created_on, -created_on'
    ),
)
class CourseListCreateAPIView(generics.ListCreateAPIView):
    '''
        Allowed methods: GET, POST

        GET: Returns list of all Courses
        POST: Creates a new Course object

        Accessible by: Admin, Principal, HOD
    '''
    queryset = models.CourseModel.objects.all()
    serializer_class = serializers.CourseFullSerializer
    permission_classes = [
        permissions.IsAuthenticated &
        (UserIsAdmin | UserIsPrincipal | UserIsHOD | UserIsTeacher)
    ]
    pagination_class = StandardPagination
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['created_on']
    ordering = '-created_on'
    filterset_fields = ['university', 'is_practical']

    #? create a new Course Object
    def post(self, request, *args, **kwargs):
        serializer = serializers.CourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()

            # log created obect when debug
            if settings.DEBUG:
                logger.info(serializer.data)

        except Exception as ex:
            logger.error(str(ex))

            return Response({'detail': str(ex)},
                            status=status.HTTP_400_BAD_REQUEST)

        response = serializer.data
        logger.info('Course Added Successfully')

        return Response(response, status=status.HTTP_201_CREATED)


@extend_schema_view(
    get=extend_schema(
        description='Returns Single Course of given Id.\n\nargs: pk',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(
                description='Course Details',
                response=serializers.CourseFullSerializer,
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
        request=serializers.CourseSerializer,
        description=
        'Updates the Course of given Id with the provided Data.\n\nargs: pk',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(description='Course Updated Successfully', ),
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
        description='Deletes the Course of the given Id.\n\nargs: pk',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(description='Course Deleted Successfully', ),
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
class CourseRetrieveUpdateDestroyAPIView(generics.GenericAPIView):
    '''
        Allowed methods: GET, PATCH, DELETE

        GET: Return Course of given Id
        PATCH: Update Course of given Id with Validated data provided
        DELETE: Delete Course of given Id

        Note: Updatation on Course is done via Partial Update method

        args: pk
        
        Accessible by: Admin, Principal, HOD, Teacher
    '''
    queryset = models.CourseModel.objects.all()
    serializer_class = serializers.CourseSerializer
    permission_classes = [
        permissions.IsAuthenticated &
        (UserIsAdmin | UserIsHOD | UserIsPrincipal | UserIsTeacher)
    ]
    lookup_field = 'pk'

    #? get single Course
    def get(self, request, *args, **kwargs):
        course = self.get_object()
        serializer = serializers.CourseFullSerializer(course)
        return Response(serializer.data)

    #? Update Course of given Id
    def patch(self, request, *args, **kwargs):
        course = self.get_object()
        serializer = serializers.CourseSerializer(
            course,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = {'detail': ['Course Updated Sucecssfully']}
        logger.info(response)

        return Response(response, status=status.HTTP_200_OK)

    #? Delete Course of given Id
    def delete(self, request, *args, **kwargs):
        course = self.get_object()
        course.delete()

        response = {'detail': ['Course Deleted Successfully']}
        logger.info(response)

        return Response(response, status=status.HTTP_200_OK)
