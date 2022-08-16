import logging

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse
from drf_spectacular.types import OpenApiTypes

from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter

from django_filters.rest_framework import DjangoFilterBackend

from .serializers import ContactSerializer, ContactCreateEditSerializer
from .models import ContactModel

from user.permissions import UserIsAdmin
from api.paginator import StandardPagination

logger = logging.getLogger(__name__)


@extend_schema_view(
    get=extend_schema(
        request=ContactSerializer,
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(
                description='Contact List',
                response=ContactSerializer,
            ),
            #? 400
            status.HTTP_400_BAD_REQUEST:
            OpenApiResponse(
                description='Bad Request',
                response=OpenApiTypes.OBJECT,
            ),
        },
        description=
        'Returns list of all Contacts.\n\nFilters:\n\n- contact_district\n\nOrdering:\n\n- default: -date_added\n\n- allowed: date_added, -date_added'
    ), )
class ContactListAPIView(generics.ListAPIView):
    queryset = ContactModel.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated & (UserIsAdmin)]
    pagination_class = StandardPagination
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['date_added']
    ordering = '-date_added'
    filterset_fields = ['contact_district']


@extend_schema_view(
    post=extend_schema(
        request=ContactCreateEditSerializer,
        responses={
            #? 201
            status.HTTP_201_CREATED:
            OpenApiResponse(description='Contact Created Successfully', ),
            #? 400
            status.HTTP_400_BAD_REQUEST:
            OpenApiResponse(
                description='Bad Request',
                response=OpenApiTypes.OBJECT,
            ),
        },
        description='Create a new Contact.',
        operation_id='contact_create',
        auth=False,
    ), )
class ContactCreateAPIView(generics.CreateAPIView):
    serializer_class = ContactCreateEditSerializer

    def post(self, request, *args, **kwargs):
        contact = ContactCreateEditSerializer(data=request.data)
        contact.is_valid(raise_exception=True)

        try:
            contact.save()

        except Exception as ex:
            logger.error(str(ex))

            return Response(
                {'detail': str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        response = {'detail': 'Contact Created Successfully'}
        logger.info(response)

        return Response(response, status=status.HTTP_201_CREATED)


@extend_schema_view(
    get=extend_schema(
        description='Returns Single Contact of given Id.\n\nargs: pk',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(
                description='Contact Detail',
                response=ContactSerializer,
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
        request=ContactCreateEditSerializer,
        description=
        'Updates the Contact of given Id with the provided Data.\n\nargs: pk',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(description='Contact Updated Successfully', ),
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
        description='Deletes the Contact of the given Id.\n\nargs: pk',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(description='Contact Deleted Successfully', ),
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
class ContactRetrieveUpdateDestroyAPIView(generics.GenericAPIView):
    '''
        Allowed methods: GET, PATCH, DELETE

        GET: Return Contact of given Id
        PATCH: Update Contact of given Id with Validated data provided
        DELETE: Delete Contaact of given Id

        Note: Updatation on Contact is done via Partial Update method

        args: pk
        
        Accessible by: Admin
    '''
    queryset = ContactModel.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated & (UserIsAdmin)]
    lookup_field = 'pk'

    #? get single Contact
    def get(self, request, *args, **kwargs):
        contact = self.get_object()
        serializer = ContactSerializer(contact)
        return Response(serializer.data)

    #? Update Contact of given Id
    def patch(self, request, *args, **kwargs):
        contact = self.get_object()
        try:
            serializer = ContactCreateEditSerializer(
                contact,
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

        response = {'detail': 'Contact Updated Sucecssfully'}
        logger.info(response)

        return Response(response, status=status.HTTP_200_OK)

    #? Delete Contact of given Id
    def delete(self, request, *args, **kwargs):
        contact = self.get_object()

        try:
            contact.delete()
        except Exception as ex:
            logger.error(str(ex))

            return Response(
                {'detail': str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        response = {'detail': 'Contact Deleted Successfully'}
        logger.info(response)

        return Response(response, status=status.HTTP_200_OK)
