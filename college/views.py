import logging

from drf_spectacular.utils import OpenApiResponse, extend_schema

from rest_framework import generics, permissions, status
from rest_framework.response import Response

from . import serializers, models

from user.permissions import UserIsAdmin

logger = logging.getLogger(__name__)


class CollegeListCreateAPIView(generics.ListCreateAPIView):
    '''
        Allowed methods: GET, POST

        GET: Returns list of all Colleges
        POST: Creates a new College object

        Accessible by: Admin
    '''
    queryset = models.CollegeModel.objects.all()
    serializer_class = serializers.CollegeFullSerializer
    permission_classes = [permissions.IsAuthenticated & (UserIsAdmin)]

    #? create a new College Object
    @extend_schema(
        request=serializers.CollegeSerializer,
        responses={
            #? 201
            status.HTTP_201_CREATED:
            OpenApiResponse(description='College Added Successfully'),
            #? 400
            status.HTTP_400_BAD_REQUEST:
            OpenApiResponse({})
        },
        description='Creates a new College Object.')
    def post(self, request, *args, **kwargs):
        serializer = serializers.CollegeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()

        except Exception as ex:
            logger.error(str(ex))

            return Response({'detail': str(ex)},
                            status=status.HTTP_400_BAD_REQUEST)

        response = {'detail': 'College Added Successfully'}
        logger.info(response)

        return Response(response, status=status.HTTP_201_CREATED)
