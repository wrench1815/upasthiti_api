import logging

from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from drf_spectacular.types import OpenApiTypes

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter

from django_filters.rest_framework import DjangoFilterBackend

from django.conf import settings

from . import serializers, models

from user.permissions import UserIsAdmin, UserIsHOD, UserIsTeacher

from api.paginator import StandardPagination

logger = logging.getLogger(__name__)


@extend_schema_view(
    post=extend_schema(
        request=serializers.StudentCreateUpdateSerializerFull,
        responses={
            #? 201
            status.HTTP_201_CREATED:
            OpenApiResponse(
                description='Student Added Successfully',
                response=serializers.StudentCreateUpdateSerializerFull,
            ),
            #? 400
            status.HTTP_400_BAD_REQUEST:
            OpenApiResponse(
                description='Bad Request',
                response=OpenApiTypes.OBJECT,
            )
        },
        description=
        'Allowed methods: GET, POST \n\nPOST: Creates a new Student object\n\nAccessible by: Admin, HOD, Teacher',
    ),
    get=extend_schema(
        request=serializers.StudentFullSerializer,
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(
                description='Student List',
                response=serializers.StudentFullSerializer,
            ),
            #? 400
            status.HTTP_400_BAD_REQUEST:
            OpenApiResponse(
                description='Bad Request',
                response=OpenApiTypes.OBJECT,
            ),
        },
        description=
        'Returns list of all Students.\n\nOrdering:\n\n- default: -created_on\n\n- allowed: created_on, -created_on'
    ),
)
class StudentListCreateAPIView(generics.ListCreateAPIView):
    '''
        Allowed methods: GET, POST

        GET: Returns list of all Students
        POST: Creates a new Student object

        Accessible by: Admin, HOD, Teacher
    '''
    queryset = models.StudentModel.objects.all()
    serializer_class = serializers.StudentFullSerializer
    permission_classes = [
        permissions.IsAuthenticated & (UserIsAdmin | UserIsHOD | UserIsTeacher)
    ]
    pagination_class = StandardPagination
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_on']
    ordering = '-created_on'

    #? create a new Student Object
    def post(self, request, *args, **kwargs):
        serializer = serializers.StudentCreateUpdateSerializerFull(
            data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            #? Create the Student as per updated Serializer
            serializer.save()

            if settings.DEBUG:
                logger.info(serializer.data)

        except Exception as ex:
            logger.error(str(ex))

            return Response(
                {'detail': str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        response = serializer.data
        logger.info('Student Added Successfully')

        return Response(response, status=status.HTTP_201_CREATED)


@extend_schema_view(
    get=extend_schema(
        description=
        'Returns Single Student on Application of given Id.\n\nargs: pk\n\nAccessible by: Admin, Teacher',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(
                description='Student Details',
                response=serializers.StudentFullSerializer,
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
        request=serializers.StudentCreateUpdateSerializerFull,
        description=
        'Updates the Student of given Id with the provided Data.\n\nargs: pk\n\nAccessible by: Admin, Teacher',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(
                description='Student Updated Successfully',
                response=OpenApiTypes.OBJECT,
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
    delete=extend_schema(
        description=
        'Deletes the Student of the given Id.\n\nargs: pk\n\nAccessible by: Admin, Teacher',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(description='Student Deleted Successfully', ),
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
class StudentRetrieveUpdateDestroyAPIView(generics.GenericAPIView):
    '''
        Allowed methods: GET, PATCH, DELETE

        GET: Return Student of given Id
        PATCH: Update Student of given Id with Validated data provided
        DELETE: Delete Student of given Id

        Note: Updatation on Student is done via Partial Update method

        args: pk
        
        Accessible by: Admin, HOD, Teacher
    '''
    queryset = models.StudentModel.objects.all()
    serializer_class = serializers.StudentFullSerializer
    permission_classes = [
        permissions.IsAuthenticated & (UserIsAdmin | UserIsHOD | UserIsTeacher)
    ]
    lookup_field = 'pk'

    #? get single Student
    def get(self, request, *args, **kwargs):
        student = self.get_object()
        serializer = serializers.StudentFullSerializer(student)
        return Response(serializer.data)

    #? Update Student of given Id
    def patch(self, request, *args, **kwargs):
        student = self.get_object()
        serializer = serializers.StudentCreateUpdateSerializerFull(
            student,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()

        except Exception as ex:
            logger.error(str(ex))

            return Response(
                {'detail': str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        response = {'detail': ['Student Updated Successfully']}
        logger.info(response)

        return Response(response, status=status.HTTP_200_OK)

    #? Delete Student of given Id
    def delete(self, request, *args, **kwargs):
        student = self.get_object()

        #? unlink college from Student
        if student.college:
            student.college.student.remove(student)

        #? Delete the Student
        student.delete()

        response = {'detail': ['Student Deleted Successfully']}
        logger.info(response)

        return Response(response, status=status.HTTP_200_OK)


class StudentBulkCreateAPIView(generics.CreateAPIView):
    '''
        Allowed methods: Bulk Post

        
        POST: Bulk Creates Student objects

        Accessible by: Admin, HOD, Teacher
    '''
    queryset = models.StudentModel.objects.all()
    serializer_class = serializers.StudentFullSerializer
    permission_classes = [
        permissions.IsAuthenticated & (UserIsAdmin | UserIsHOD | UserIsTeacher)
    ]

    #? Bulk Create Student Objects
    @extend_schema(
        request=serializers.StudentSerializer,
        responses={
            #? 201
            status.HTTP_201_CREATED:
            OpenApiResponse(description='Students Added Successfully'),
            #? 400
            status.HTTP_400_BAD_REQUEST:
            OpenApiResponse({})
        },
        description=
        'Bulk Post Students \n\nPOST: Bulk Creates Student objects \n\nAccessible by: Admin, HOD, Teacher',
    )
    def post(self, request, *args, **kwargs):
        serializer = serializers.StudentSerializer(
            data=request.data,
            many=True,
        )
        serializer.is_valid(raise_exception=True)

        try:

            serializer.save()

        except Exception as ex:
            logger.error(str(ex))

            return Response({'detail': str(ex)},
                            status=status.HTTP_400_BAD_REQUEST)

        response = {'detail': ['Students Added Successfully']}
        logger.info(response)

        return Response(response, status=status.HTTP_201_CREATED)
