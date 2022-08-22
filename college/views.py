import logging

from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from drf_spectacular.types import OpenApiTypes

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter

from django_filters.rest_framework import DjangoFilterBackend

from . import serializers, models
from . import response_serializers as rs

from user.permissions import UserIsAdmin

from api.paginator import StandardPagination

logger = logging.getLogger(__name__)


@extend_schema_view(
    post=extend_schema(
        request=serializers.CollegeCreateUpdateSerializer,
        responses={
            #? 201
            status.HTTP_201_CREATED:
            OpenApiResponse(
                description='College Created Successfully',
                response=rs.ResponseCollegeCreateSerializer,
            ),
            #? 400
            status.HTTP_400_BAD_REQUEST:
            OpenApiResponse(
                description='Bad Request',
                response=OpenApiTypes.OBJECT,
            ),
        },
        description='Create a new College.'),
    get=extend_schema(
        request=serializers.CollegeSerializer,
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(
                description='College List',
                response=serializers.CollegeSerializer,
            ),
            #? 400
            status.HTTP_400_BAD_REQUEST:
            OpenApiResponse(
                description='Bad Request',
                response=OpenApiTypes.OBJECT,
            ),
        },
        description=
        'Returns list of all Colleges.\n\nFilters:\n\n- district\n\n- university(id)\n\nOrdering:\n\n- default: -created_on\n\n- allowed: created_on, -created_on'
    ),
)
class CollegeListCreateAPIView(generics.ListCreateAPIView):
    '''
        Allowed methods: GET, POST

        GET: Returns list of all Colleges
        POST: Creates a new College object

        Filters:
            district
            university(id)

        Ordering:
            default: -created_on
            allowed: created_on, -created_on

        Accessible by: Admin
    '''
    queryset = models.CollegeModel.objects.all()
    serializer_class = serializers.CollegeSerializer
    permission_classes = [permissions.IsAuthenticated & (UserIsAdmin)]
    pagination_class = StandardPagination
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['created_on']
    ordering = '-created_on'
    filterset_fields = ['university', 'district']

    #? create a new College
    def post(self, request, *args, **kwargs):
        serializer = serializers.CollegeCreateUpdateSerializer(
            data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()

        except Exception as ex:
            logger.error(str(ex))

            return Response({'detail': str(ex)},
                            status=status.HTTP_400_BAD_REQUEST)

        response = serializer.data
        logger.info('College Created Successfully')

        return Response(response, status=status.HTTP_201_CREATED)


@extend_schema_view(
    get=extend_schema(
        description='Returns Single College of given Id.\n\nargs: pk',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(
                description='College Details',
                response=serializers.CollegeSerializer,
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
        request=serializers.CollegeCreateUpdateSerializer,
        description=
        'Updates the College of given Id with the provided Data.\n\nargs: pk',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(description='College Updated Successfully', ),
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
        description='Deletes the College of the given Id.\n\nargs: pk',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(description='College Deleted Successfully', ),
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
class CollegeRetrieveUpdateDestroyAPIView(generics.GenericAPIView):
    '''
        Allowed methods: GET, PATCH, DELETE

        GET: Return College of given Id
        PATCH: Update College of given Id with Validated data provided
        DELETE: Delete College of given Id

        Note: Updatation on Collge is done via Partial Update method

        args: pk
        
        Accessible by: Admin
    '''
    queryset = models.CollegeModel.objects.all()
    serializer_class = serializers.CollegeCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated & (UserIsAdmin)]
    lookup_field = 'pk'

    #? get single College
    def get(self, request, *args, **kwargs):
        college = self.get_object()
        serializer = serializers.CollegeSerializer(college)
        return Response(serializer.data)

    #? Update College of given Id
    def patch(self, request, *args, **kwargs):
        college = self.get_object()
        try:
            serializer = serializers.CollegeCreateUpdateSerializer(
                college,
                data=request.data,
                partial=True,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

        except Exception as ex:
            logger.error(str(ex))

            return Response(
                {'detail': str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        response = {'detail': 'College Updated Sucecssfully'}
        logger.info(response)

        return Response(response, status=status.HTTP_200_OK)

    #? Delete college of given Id
    def delete(self, request, *args, **kwargs):
        college = self.get_object()

        try:
            college.delete()
        except Exception as ex:
            logger.error(str(ex))

            return Response(
                {'detail': str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        response = {'detail': 'College Deleted Successfully'}
        logger.info(response)

        return Response(response, status=status.HTTP_200_OK)
