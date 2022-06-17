import logging

from drf_spectacular.utils import OpenApiResponse, extend_schema

from rest_framework import generics, permissions, status
from rest_framework.response import Response

from . import serializers, models

from user.permissions import UserIsAdmin, UserIsPrincipal, UserIsTeacher

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
    @extend_schema(
        description=
        'Returns Single Department on Application of given Id.\n\nargs: pk\n\nAccessible by: Admin, Teacher',
        responses={
            #? 200
            status.HTTP_200_OK:
            serializers.DepartmentFullSerializer,
            #? 404
            status.HTTP_404_NOT_FOUND:
            OpenApiResponse(description='Not found')
        })
    def get(self, request, *args, **kwargs):
        department = self.get_object()
        serializer = serializers.DepartmentFullSerializer(department)
        return Response(serializer.data)

    #? Update Department of given Id
    @extend_schema(
        request=serializers.DepartmentSerializer,
        description=
        'Updates the Department of given Id with the provided Data.\n\nargs: pk\n\nAccessible by: Admin, Teacher',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(description='Department Updated Successfully'),
            #? 404
            status.HTTP_404_NOT_FOUND:
            OpenApiResponse(description='Not found')
        })
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
    @extend_schema(
        description=
        'Deletes the Department of the given Id.\n\nargs: pk\n\nAccessible by: Admin, Teacher',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(description='Department Deleted Successfully'),
            #? 404
            status.HTTP_404_NOT_FOUND:
            OpenApiResponse(description='Not found')
        })
    def delete(self, request, *args, **kwargs):
        department = self.get_object()
        department.delete()

        response = {'detail': 'Department Deleted Successfully'}
        logger.info(response)

        return Response(response, status=status.HTTP_200_OK)


class DepartmentTypeListCreateAPIView(generics.ListCreateAPIView):
    '''
        Allowed methods: GET, POST

        GET: Returns list of all Department Types
        POST: Creates a new Department Type object

        Accessible by: Admin, Principal
    '''
    queryset = models.DepartmentTypeModel.objects.all()
    serializer_class = serializers.DepartmentTypeSerializer
    permission_classes = [
        permissions.IsAuthenticated & (UserIsAdmin | UserIsPrincipal)
    ]

    #? list all department types
    @extend_schema(
        description=
        'Returns list of all Department Types.\n\nAccessible by: Admin, Teacher',
        responses={
            #? 200
            status.HTTP_200_OK:
            serializers.DepartmentTypeSerializer,
            #? 404
            status.HTTP_404_NOT_FOUND:
            OpenApiResponse(description='Not found')
        })
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    #? Create a new department object
    @extend_schema(
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
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


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
    permission_classes = [
        permissions.IsAuthenticated & (UserIsAdmin | UserIsPrincipal)
    ]
    lookup_field = 'pk'

    #? get single Department Type
    @extend_schema(
        description=
        'Returns Single Department Type of given Id.\n\nargs: pk\n\nAccessible by: Admin, Teacher',
        responses={
            #? 200
            status.HTTP_200_OK:
            serializers.DepartmentTypeSerializer,
            #? 404
            status.HTTP_404_NOT_FOUND:
            OpenApiResponse(description='Not found')
        })
    def get(self, request, *args, **kwargs):
        department_type = self.get_object()
        serializer = serializers.DepartmentTypeSerializer(department_type)

        return Response(serializer.data)

    #? Update Department Type of given Id
    @extend_schema(
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
        })
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
    @extend_schema(
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
        })
    def delete(self, request, *args, **kwargs):
        department_type = self.get_object()
        department_type.delete()

        response = {'detail': 'Department Type Deleted Successfully'}
        logger.info(response)

        return Response(response, status=status.HTTP_200_OK)
