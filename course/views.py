import logging

from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from drf_spectacular.types import OpenApiTypes

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter

from django_filters.rest_framework import DjangoFilterBackend

from . import serializers, models

from user.permissions import UserIsAdmin, UserIsPrincipal, UserIsHOD, UserIsTeacher

from api.paginator import StandardPagination

logger = logging.getLogger(__name__)


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
    # filterset_fields = ['university', 'district']

    #? create a new Course Object
    @extend_schema(
        request=serializers.CourseSerializer,
        responses={
            #? 201
            status.HTTP_201_CREATED:
            OpenApiResponse(description='Course Added Successfully'),
            #? 400
            status.HTTP_400_BAD_REQUEST:
            OpenApiResponse({})
        },
        description='Creates a new Course Object.')
    def post(self, request, *args, **kwargs):
        serializer = serializers.CourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()

        except Exception as ex:
            logger.error(str(ex))

            return Response({'detail': str(ex)},
                            status=status.HTTP_400_BAD_REQUEST)

        response = {'detail': 'Course Added Successfully'}
        logger.info(response)

        return Response(response, status=status.HTTP_201_CREATED)


class CourseRetrieveUpdateDestroyAPIView(generics.GenericAPIView):
    '''
        Allowed methods: GET, PATCH, DELETE

        GET: Return Course of given Id
        PATCH: Update Course of given Id with Validated data provided
        DELETE: Delete Course of given Id

        Note: Updatation on Course is done via Partial Update method

        args: pk
        
        Accessible by: Admin,Principal, HOD
    '''
    queryset = models.CourseModel.objects.all()
    serializer_class = serializers.CourseSerializer
    permission_classes = [
        permissions.IsAuthenticated &
        (UserIsAdmin | UserIsHOD | UserIsPrincipal)
    ]
    lookup_field = 'pk'

    #? get single Course
    @extend_schema(
        description=
        'Returns Single Course on Application of given Id.\n\nargs: pk\n\nAccessible by: Admin',
        responses={
            #? 200
            status.HTTP_200_OK:
            serializers.CourseFullSerializer,
            #? 404
            status.HTTP_404_NOT_FOUND:
            OpenApiResponse(description='Not found')
        })
    def get(self, request, *args, **kwargs):
        course = self.get_object()
        serializer = serializers.CourseFullSerializer(course)
        return Response(serializer.data)

    #? Update Course of given Id
    @extend_schema(
        request=serializers.CourseSerializer,
        description=
        'Updates the Course of given Id with the provided Data.\n\nargs: pk\n\nAccessible by: Admin',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(description='Course Updated Successfully'),
            #? 404
            status.HTTP_404_NOT_FOUND:
            OpenApiResponse(description='Not found')
        })
    def patch(self, request, *args, **kwargs):
        course = self.get_object()
        serializer = serializers.CourseSerializer(
            course,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = {'detail': 'Course Updated Sucecssfully'}
        logger.info(response)

        return Response(response, status=status.HTTP_200_OK)

    #? Delete Course of given Id
    @extend_schema(
        description=
        'Deletes the Course of the given Id.\n\nargs: pk\n\nAccessible by: Admin',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(description='Course Deleted Successfully'),
            #? 404
            status.HTTP_404_NOT_FOUND:
            OpenApiResponse(description='Not found')
        })
    def delete(self, request, *args, **kwargs):
        course = self.get_object()
        course.delete()

        response = {'detail': 'Course Deleted Successfully'}
        logger.info(response)

        return Response(response, status=status.HTTP_200_OK)
