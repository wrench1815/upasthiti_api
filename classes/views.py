import logging

from drf_spectacular.utils import OpenApiResponse, extend_schema

from rest_framework import generics, permissions, status
from rest_framework.response import Response

from . import serializers, models

from user.permissions import UserIsAdmin, UserIsHOD, UserIsTeacher

logger = logging.getLogger(__name__)


class ClassesListCreateAPIView(generics.ListCreateAPIView):
    '''
        Allowed methods: GET, POST

        GET: Returns list of all Classes
        POST: Creates a new Classes object

        Accessible by: Admin, HOD, Teacher
    '''
    queryset = models.ClassesModel.objects.all()
    serializer_class = serializers.ClassesFullSerializer
    permission_classes = [
        permissions.IsAuthenticated & (UserIsAdmin | UserIsHOD | UserIsTeacher)
    ]

    #? create a new Classes Object
    @extend_schema(
        request=serializers.ClassesSerializer,
        responses={
            #? 201
            status.HTTP_201_CREATED:
            OpenApiResponse(description='Classes Added Successfully'),
            #? 400
            status.HTTP_400_BAD_REQUEST:
            OpenApiResponse({})
        },
        description='Creates a new Classes Object.')
    def post(self, request, *args, **kwargs):
        serializer = serializers.ClassesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()

        except Exception as ex:
            logger.error(str(ex))

            return Response({'detail': str(ex)},
                            status=status.HTTP_400_BAD_REQUEST)

        response = {'detail': 'Classes Added Successfully'}
        logger.info(response)

        return Response(response, status=status.HTTP_201_CREATED)
