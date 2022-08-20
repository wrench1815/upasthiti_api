import logging

from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from drf_spectacular.types import OpenApiTypes

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter, SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from . import serializers, models
from .filters import DepartmentTypeFilter

from user.permissions import UserIsAdmin, UserIsPrincipal, UserIsTeacher

from api.paginator import StandardPagination

logger = logging.getLogger(__name__)


@extend_schema_view(
    post=extend_schema(
        request=serializers.DepartmentSerializer,
        responses={
            #? 201
            status.HTTP_201_CREATED:
            OpenApiResponse(description='Department Added Successfully', ),
            #? 400
            status.HTTP_400_BAD_REQUEST:
            OpenApiResponse(
                description='Bad Request',
                response=OpenApiTypes.OBJECT,
            ),
        },
        description='Creates a new Department Object.'),
    get=extend_schema(
        request=serializers.DepartmentFullSerializer,
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(
                description='Department List',
                response=serializers.DepartmentFullSerializer,
            ),
            #? 400
            status.HTTP_400_BAD_REQUEST:
            OpenApiResponse(
                description='Bad Request',
                response=OpenApiTypes.OBJECT,
            ),
        },
        description='Returns list of all Department.'),
)
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
    pagination_class = StandardPagination
    filter_backends = [OrderingFilter, SearchFilter, DjangoFilterBackend]
    ordering_fields = ['created_on']
    ordering = '-created_on'
    search_fields = ['$name__department_name']  #? fuzzy search using regex
    filterset_fields = [
        'name',
        'college',
        'hod',
    ]

    #? Create a new department object
    def post(self, request, *args, **kwargs):
        dept = serializers.DepartmentSerializer(data=request.data)
        dept.is_valid(raise_exception=True)

        try:
            dept.save()
        except Exception as ex:
            logger.error(str(ex))
            return Response({'detail': str(ex)},
                            status=status.HTTP_400_BAD_REQUEST)

        response = {'detail': 'Department Added Successfully'}
        logger.info(response)

        return Response(response, status=status.HTTP_201_CREATED)


@extend_schema_view(
    get=extend_schema(
        description=
        'Returns Single Department registered on Application of given Id.\n\nargs: pk',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(
                description='Department Details',
                response=serializers.DepartmentFullSerializer,
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
        request=serializers.DepartmentSerializer,
        description=
        'Updates the Department of given Id with the provided Data.\n\nargs: pk',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(description='Department Updated Successfully', ),
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
        description='Deletes the Department of the given Id.\n\nargs: pk',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(description='Department Deleted Successfully', ),
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
class DepartmentRetrieveUpdateDestroyAPIView(generics.GenericAPIView):
    '''
        Allowed methods: GET, PATCH, DELETE

        GET: Return Department of given Id
        PATCH: Update Department of given Id with Validated data provided
        DELETE: Delete Department of given Id

        Note: Updatation on Department is done via Partial Update method

        args: pk
        
        Accessible by: Admin, Principal
    '''
    queryset = models.DepartmentModel.objects.all()
    serializer_class = serializers.DepartmentSerializer
    permission_classes = [
        permissions.IsAuthenticated & (UserIsAdmin | UserIsPrincipal)
    ]
    lookup_field = 'pk'

    #? get single Department
    def get(self, request, *args, **kwargs):
        department = self.get_object()
        serializer = serializers.DepartmentFullSerializer(department)
        return Response(serializer.data)

    #? Update Department of given Id
    def patch(self, request, *args, **kwargs):
        department = self.get_object()
        serializer = serializers.DepartmentSerializer(
            department,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = {'detail': 'Department Updated Sucecssfully'}
        logger.info(response)

        return Response(response, status=status.HTTP_200_OK)

    #? Delete Department of given Id
    def delete(self, request, *args, **kwargs):
        department = self.get_object()
        department.delete()

        response = {'detail': 'Department Deleted Successfully'}
        logger.info(response)

        return Response(response, status=status.HTTP_200_OK)


@extend_schema_view(
    get=extend_schema(
        description=
        'Returns list of all Department Types.\n\nFilters:\n\n- unassigned\n\n- exclude_college\n\nAccessible by: Admin, Teacher',
        responses={
            #? 200
            status.HTTP_200_OK:
            serializers.DepartmentTypeFullSerializer,
            #? 404
            status.HTTP_404_NOT_FOUND:
            OpenApiResponse(description='Not found')
        }),
    post=extend_schema(
        request=serializers.DepartmentTypeSerializer,
        responses={
            #? 201
            status.HTTP_201_CREATED:
            OpenApiResponse(description='Department Type Added Successfully'),
            #?400
            status.HTTP_400_BAD_REQUEST:
            OpenApiResponse({})
        },
        description=
        'Creates a new Department Type Object.\n\nAccessible by: Admin, Teacher'
    ),
)
class DepartmentTypeListCreateAPIView(generics.ListCreateAPIView):
    '''
        Allowed methods: GET, POST

        GET: Returns list of all Department Types
        POST: Creates a new Department Type object

        Accessible by: Admin, Principal
    '''
    queryset = models.DepartmentTypeModel.objects.all()
    serializer_class = serializers.DepartmentTypeFullSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = DepartmentTypeFilter

    #? Create a new department object
    def post(self, request, *args, **kwargs):
        serializer = serializers.DepartmentTypeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()
        except Exception as ex:
            logger.error(str(ex))
            return Response({'detail': str(ex)},
                            status=status.HTTP_400_BAD_REQUEST)

        response = {'detail': 'Department Type Added Successfully'}
        logger.info(response)

        return Response(response, status=status.HTTP_201_CREATED)


@extend_schema_view(
    get=extend_schema(
        description=
        'Returns Single Department Type of given Id.\n\nargs: pk\n\nAccessible by: Admin, Teacher',
        responses={
            #? 200
            status.HTTP_200_OK:
            serializers.DepartmentTypeSerializer,
            #? 404
            status.HTTP_404_NOT_FOUND:
            OpenApiResponse(description='Not found')
        }),
    patch=extend_schema(
        request=serializers.DepartmentTypeSerializer,
        description=
        'Updates the Department Type of given Id with the provided Data.\n\nargs: pk\n\nAccessible by: Admin, Teacher',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(
                description='Department Type Updated Successfully'),
            #? 404
            status.HTTP_404_NOT_FOUND:
            OpenApiResponse(description='Not found')
        }),
    delete=extend_schema(
        description=
        'Deletes the Department Type of the given Id.\n\nargs: pk\n\nAccessible by: Admin, Teacher',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(
                description='Department Type Deleted Successfully'),
            #? 404
            status.HTTP_404_NOT_FOUND:
            OpenApiResponse(description='Not found')
        }),
)
class DepartmentTypeRetrieveUpdateDestroyAPIView(generics.GenericAPIView):
    '''
        Allowed methods: GET, PATCH, DELETE

        GET: Return Department Type of given Id
        PATCH: Update Department Type of given Id with Validated data provided
        DELETE: Delete Department Type of given Id

        Note: Updatation on Department Type is done via Partial Update method

        args: pk
        
        Accessible by: Admin, Principal
    '''
    queryset = models.DepartmentTypeModel.objects.all()
    serializer_class = serializers.DepartmentTypeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'pk'

    #? get single Department Type
    def get(self, request, *args, **kwargs):
        department_type = self.get_object()
        serializer = serializers.DepartmentTypeFullSerializer(department_type)

        return Response(serializer.data)

    #? Update Department Type of given Id
    def patch(self, request, *args, **kwargs):
        department_type = self.get_object()
        serializer = serializers.DepartmentTypeSerializer(
            department_type,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = {'detail': 'Department Type Updated Sucecssfully'}
        logger.info(response)

        return Response(response, status=status.HTTP_200_OK)

    #? Delete Department Type of given Id
    def delete(self, request, *args, **kwargs):
        department_type = self.get_object()
        department_type.delete()

        response = {'detail': 'Department Type Deleted Successfully'}
        logger.info(response)

        return Response(response, status=status.HTTP_200_OK)
