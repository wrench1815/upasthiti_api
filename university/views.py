import logging

from drf_spectacular.utils import OpenApiResponse, extend_schema_view, extend_schema
from drf_spectacular.types import OpenApiTypes

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter

from . import models, serializers

from user.permissions import UserIsAdmin

from api.paginator import StandardPagination

logger = logging.getLogger(__name__)


@extend_schema_view(
    post=extend_schema(
        request=serializers.UniversityCreateSerializer,
        responses={
            #? 201
            status.HTTP_201_CREATED:
            OpenApiResponse(description='University Created Successfully', ),
            #? 400
            status.HTTP_400_BAD_REQUEST:
            OpenApiResponse(
                description='Bad Request',
                response=OpenApiTypes.OBJECT,
            ),
        },
        description='Create a new University.'),
    get=extend_schema(
        request=serializers.UniversitySerializer,
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(
                description='University List',
                response=serializers.UniversitySerializer,
            ),
            #? 400
            status.HTTP_400_BAD_REQUEST:
            OpenApiResponse(
                description='Bad Request',
                response=OpenApiTypes.OBJECT,
            ),
        },
        description='Returns list of all University.'),
)
class UniversityListCreateAPIView(generics.ListCreateAPIView):
    '''
        Allowed methods: GET, POST

        GET: Returns list of all University
        POST: Creates a new University

        Accessible by: Admin
    '''
    queryset = models.UniversityModel.objects.all()
    serializer_class = serializers.UniversitySerializer
    permission_classes = [permissions.IsAuthenticated & (UserIsAdmin)]
    pagination_class = StandardPagination
    filter_backends = [OrderingFilter]
    ordering_fields = 'date_added'
    ordering = '-date_added'

    #? Create a new University
    def post(self, request, *args, **kwargs):
        serializer = serializers.UniversityCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()

        except Exception as ex:
            logger.error(str(ex))

            return Response({'detail': str(ex)},
                            status=status.HTTP_400_BAD_REQUEST)

        response = {'detail': 'University Created Successfully'}
        logger.info(response)

        return Response(response, status=status.HTTP_201_CREATED)
