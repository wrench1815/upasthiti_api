import logging

from drf_spectacular.utils import OpenApiResponse, extend_schema

from rest_framework import generics, permissions, status
from rest_framework.response import Response

from . import serializers, models

from user.permissions import UserIsAdmin, UserIsPrincipal, UserIsHOD

logger = logging.getLogger(__name__)


class CourseListCreateAPIView(generics.ListCreateAPIView):
    '''
        Allowed methods: GET, POST

        GET: Returns list of all Courses
        POST: Creates a new Course object

        Accessible by: Admin, HOD, Teacher
    '''
    queryset = models.CourseModel.objects.all()
    serializer_class = serializers.CourseFullSerializer
    permission_classes = [
        permissions.IsAuthenticated &
        (UserIsAdmin | UserIsPrincipal | UserIsHOD)
    ]

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
