import logging

from drf_spectacular.utils import OpenApiResponse, extend_schema

from rest_framework import generics, permissions, status
from rest_framework.response import Response

from . import serializers, models

from user.permissions import UserIsAdmin, UserIsPrincipal

logger = logging.getLogger(__name__)



class DepartmentListCreateAPIView(generics.ListCreateAPIView):
    '''
        Allowed methods: GET, POST

        GET: Returns list of all Departments
        POST: Creates a new Department object

        Accessible by: Admin, Principal
    '''
    queryset = models.DepartmentModel.objects.all()
    serializer_class = serializers.DepartmentFullSerializer
    permission_classes = [
        permissions.IsAuthenticated & (UserIsAdmin | UserIsPrincipal)
    ]

    #? Create a new department object
    @extend_schema(
        request=serializers.DepartmentSerializer,
        responses={
            #? 201
            status.HTTP_201_CREATED:
            OpenApiResponse(description='Department Added Successfully'),
            #?400
            status.HTTP_400_BAD_REQUEST:
            OpenApiResponse({})
        },
        description='Creates a new Department Object.')
    def post(self, request, *args, **kwargs):
        serializer = serializers.DepartmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()
        except Exception as ex:
            logger.error(str(ex))
            return Response({'detail': str(ex)},
                            status=status.HTTP_400_BAD_REQUEST)

        response = {'detail': 'Department Added Successfully'}
        logger.info(response)

        return Response(response, status=status.HTTP_201_CREATED)
