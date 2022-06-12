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
