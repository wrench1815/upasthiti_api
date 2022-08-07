import logging

from drf_spectacular.utils import OpenApiResponse, extend_schema_view, extend_schema
from drf_spectacular.types import OpenApiTypes

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter, SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

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

        Filters:
            district

        Ordering:
            default: -data_added
            allowed: date_added, -date_added

        Accessible by: Admin
    '''
    queryset = models.UniversityModel.objects.all()
    serializer_class = serializers.UniversitySerializer
    permission_classes = [permissions.IsAuthenticated & (UserIsAdmin)]
    pagination_class = StandardPagination
    filter_backends = [OrderingFilter, SearchFilter, DjangoFilterBackend]
    ordering_fields = ['date_added']
    ordering = '-date_added'
    search_fields = ['$name'] #? fuzzy search using regex
    filterset_fields = ['district']

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


@extend_schema_view(
    get=extend_schema(
        description=
        'Returns Single Ubiversity registered on Application of given Id.\n\nargs: pk',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(
                description='University Details',
                response=serializers.UniversitySerializer,
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
        request=serializers.UniversityCreateSerializer,
        description=
        'Updates the University of given Id with the provided Data.\n\nargs: pk',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(description='University Updated Successfully', ),
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
        description='Deletes the University of the given Id.\n\nargs: pk',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(description='University Deleted Successfully', ),
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
class UniversityRetrieveUpdateDestroyAPIView(generics.GenericAPIView):
    '''
        Allowed methods: GET, PATCH, DELETE

        GET: Return University of given Id
        PATCH: Update University of given Id with Validated data provided
        DELETE: Delete University of given Id

        Note: Updatation on University is done via Partial Update method

        args: pk
        
        Accessible by: Admin
    '''
    queryset = models.UniversityModel.objects.all()
    serializer_class = serializers.UniversitySerializer
    permission_classes = [permissions.IsAuthenticated & (UserIsAdmin)]
    lookup_field = 'pk'

    #? get single University
    def get(self, request, *args, **kwargs):
        university = self.get_object()
        serializer = serializers.UniversitySerializer(university)
        return Response(serializer.data)

    #? Update University of given Id
    def patch(self, request, *args, **kwargs):
        university = self.get_object()

        try:
            serializer = serializers.UniversityCreateSerializer(
                university,
                data=request.data,
                partial=True,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

        except Exception as ex:
            logger.error(str(ex))

            return Response({'detail': str(ex)},
                            status=status.HTTP_400_BAD_REQUEST)

        response = {'detail': 'University Updated Successfully'}
        logger.info(response)

        return Response(response, status=status.HTTP_200_OK)

    #? Delete University of given Id
    def delete(self, request, *args, **kwargs):
        university = self.get_object()

        try:

            university.delete()

        except Exception as ex:
            logger.error(str(ex))

            return Response({'detail': str(ex)},
                            status=status.HTTP_400_BAD_REQUEST)

        response = {'detail': 'University Deleted Successfully'}
        logger.info(response)

        return Response(response, status=status.HTTP_200_OK)
