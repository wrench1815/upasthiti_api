import logging

from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from drf_spectacular.types import OpenApiTypes

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter

from django.conf import settings

from . import serializers, models

from user.permissions import UserIsAdmin, UserIsTeacher

from api.paginator import StandardPagination

logger = logging.getLogger(__name__)


@extend_schema_view(
    post=extend_schema(
        request=serializers.AttendanceSerializer,
        responses={
            #? 201
            status.HTTP_201_CREATED:
            OpenApiResponse(
                description='Attendance Added Successfully',
                response=serializers.AttendanceSerializer,
            ),
            #? 400
            status.HTTP_400_BAD_REQUEST:
            OpenApiResponse(
                description='Bad Request',
                response=OpenApiTypes.OBJECT,
            ),
        },
        description='Creates a new Attendance Object.'),
    get=extend_schema(
        request=serializers.AttendanceFullSerializer,
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(
                description='Attendance List',
                response=serializers.AttendanceFullSerializer,
            ),
            #? 400
            status.HTTP_400_BAD_REQUEST:
            OpenApiResponse(
                description='Bad Request',
                response=OpenApiTypes.OBJECT,
            ),
        },
        description=
        'Returns list of all Attendances.\n\nOrdering:\n\n- default: -created_on\n\n- allowed: created_on, -created_on'
    ),
)
class AttendanceListCreateAPIView(generics.ListCreateAPIView):
    '''
        Allowed methods: GET, POST

        GET: Returns list of all Attendances
        POST: Creates a new Attendance object

        Accessible by: Admin, Teacher
    '''
    queryset = models.AttendanceModel.objects.all()
    serializer_class = serializers.AttendanceFullSerializer
    permission_classes = [
        permissions.IsAuthenticated & (UserIsAdmin | UserIsTeacher)
    ]
    pagination_class = StandardPagination
    filter_backends = [
        OrderingFilter,
    ]
    ordering_fields = ['created_on']
    ordering = '-created_on'

    #? create a new Attendance Object
    def post(self, request, *args, **kwargs):
        serializer = serializers.AttendanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()

            if settings.DEBUG:
                logger.info(serializer.data)

        except Exception as ex:
            logger.error(str(ex))

            return Response({'detail': str(ex)},
                            status=status.HTTP_400_BAD_REQUEST)

        response = serializer.data
        logger.info('Attendance Added Successfully')

        return Response(response, status=status.HTTP_201_CREATED)


@extend_schema_view(
    get=extend_schema(
        description=
        'Returns Single Attendance on Application of given Id.\n\nargs: pk\n\nAccessible by: Admin, Teacher',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(
                description='Attendance Details',
                response=serializers.AttendanceFullSerializer,
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
        request=serializers.AttendanceFullSerializer,
        description=
        'Updates an Attendance of given Id with the provided Data.\n\nargs: pk',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(description='Attendance Updated Successfully', ),
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
        description='Deletes the Attendance of the given Id.\n\nargs: pk',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(description='Attendance Deleted Successfully', ),
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
class AttendanceRetrieveUpdateDestroyAPIView(generics.GenericAPIView):
    '''
        Allowed methods: GET, PATCH, DELETE

        GET: Return Attendance of given Id
        PATCH: Update Attendance of given Id with Validated data provided
        DELETE: Delete Attendance of given Id

        Note: Updatation on Attendance is done via Partial Update method

        args: pk
        
        Accessible by: Admin, Teacher
    '''
    queryset = models.AttendanceModel.objects.all()
    serializer_class = serializers.AttendanceSerializer
    permission_classes = [
        permissions.IsAuthenticated & (UserIsAdmin | UserIsTeacher)
    ]
    lookup_field = 'pk'

    #? get single Attendance
    def get(self, request, *args, **kwargs):
        attendance = self.get_object()
        serializer = serializers.AttendanceFullSerializer(attendance)
        return Response(serializer.data)

    #? Update Attendance of given Id
    def patch(self, request, *args, **kwargs):
        attendance = self.get_object()
        serializer = serializers.AttendanceSerializer(
            attendance,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = {'detail': ['Attendance Updated Sucecssfully']}
        logger.info(response)

        return Response(response, status=status.HTTP_200_OK)

    #? Delete Attendance of given Id
    def delete(self, request, *args, **kwargs):
        attendance = self.get_object()

        #? unlink class from attendance
        if attendance.for_class:
            attendance.for_class.attendance_class.remove(attendance)

        #? unlink student from attendance
        if attendance.student:
            attendance.student.attendance_student.remove(attendance)

        attendance.delete()

        response = {'detail': ['Attendance Deleted Successfully']}
        logger.info(response)

        return Response(response, status=status.HTTP_200_OK)
