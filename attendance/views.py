import logging

from drf_spectacular.utils import OpenApiResponse, extend_schema

from rest_framework import generics, permissions, status
from rest_framework.response import Response

from . import serializers, models

from user.permissions import UserIsAdmin, UserIsTeacher

logger = logging.getLogger(__name__)


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

    #? create a new Attendance Object
    @extend_schema(
        request=serializers.AttendanceSerializer,
        responses={
            #? 201
            status.HTTP_201_CREATED:
            OpenApiResponse(description='Attendance Added Successfully'),
            #? 400
            status.HTTP_400_BAD_REQUEST:
            OpenApiResponse({})
        },
        description='Creates a new Attendance Object.')
    def post(self, request, *args, **kwargs):
        serializer = serializers.AttendanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()

        except Exception as ex:
            logger.error(str(ex))

            return Response({'detail': str(ex)},
                            status=status.HTTP_400_BAD_REQUEST)

        response = {'detail': 'Attendance Added Successfully'}
        logger.info(response)

        return Response(response, status=status.HTTP_201_CREATED)


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
    @extend_schema(
        description=
        'Returns Single Attendance on Application of given Id.\n\nargs: pk\n\nAccessible by: Admin, Teacher',
        responses={
            #? 200
            status.HTTP_200_OK:
            serializers.AttendanceFullSerializer,
            #? 404
            status.HTTP_404_NOT_FOUND:
            OpenApiResponse(description='Not found')
        })
    def get(self, request, *args, **kwargs):
        attendance = self.get_object()
        serializer = serializers.AttendanceFullSerializer(attendance)
        return Response(serializer.data)

    #? Update Attendance of given Id
    @extend_schema(
        request=serializers.AttendanceSerializer,
        description=
        'Updates the Attendance of given Id with the provided Data.\n\nargs: pk\n\nAccessible by: Admin, Teacher',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(description='Attendance Updated Successfully'),
            #? 404
            status.HTTP_404_NOT_FOUND:
            OpenApiResponse(description='Not found')
        })
    def patch(self, request, *args, **kwargs):
        attendance = self.get_object()
        serializer = serializers.AttendanceSerializer(
            attendance,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = {'detail': 'Attendance Updated Sucecssfully'}
        logger.info(response)

        return Response(response, status=status.HTTP_200_OK)

    #? Delete Attendance of given Id
    @extend_schema(
        description=
        'Deletes the Attendance of the given Id.\n\nargs: pk\n\nAccessible by: Admin, Teacher',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(description='Attdendance Deleted Successfully'),
            #? 404
            status.HTTP_404_NOT_FOUND:
            OpenApiResponse(description='Not found')
        })
    def delete(self, request, *args, **kwargs):
        attendance = self.get_object()
        attendance.delete()

        response = {'detail': 'Attendance Deleted Successfully'}
        logger.info(response)

        return Response(response, status=status.HTTP_200_OK)
