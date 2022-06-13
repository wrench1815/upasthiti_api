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


class ClassesRetrieveUpdateDestroyAPIView(generics.GenericAPIView):
    '''
        Allowed methods: GET, PATCH, DELETE

        GET: Return Classes of given Id
        PATCH: Update Classes of given Id with Validated data provided
        DELETE: Delete Classes of given Id

        Note: Updatation on Classes is done via Partial Update method

        args: pk
        
        Accessible by: Admin, HOD, Teacher
    '''
    queryset = models.ClassesModel.objects.all()
    serializer_class = serializers.ClassesSerializer
    permission_classes = [
        permissions.IsAuthenticated & (UserIsAdmin | UserIsHOD | UserIsTeacher)
    ]
    lookup_field = 'pk'

    #? get single Class(s)
    @extend_schema(
        description=
        'Returns Single Classes on Application of given Id.\n\nargs: pk\n\nAccessible by: Admin, HOD, Teacher',
        responses={
            #? 200
            status.HTTP_200_OK:
            serializers.ClassesFullSerializer,
            #? 404
            status.HTTP_404_NOT_FOUND:
            OpenApiResponse(description='Not found')
        })
    def get(self, request, *args, **kwargs):
        classes = self.get_object()
        serializer = serializers.ClassesFullSerializer(classes)
        return Response(serializer.data)

    #? Update Classes of given Id
    @extend_schema(
        request=serializers.ClassesSerializer,
        description=
        'Updates the Classes of given Id with the provided Data.\n\nargs: pk\n\nAccessible by: Admin, HOD, Teacher',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(description='Classes Updated Successfully'),
            #? 404
            status.HTTP_404_NOT_FOUND:
            OpenApiResponse(description='Not found')
        })
    def patch(self, request, *args, **kwargs):
        classes = self.get_object()
        serializer = serializers.ClassesSerializer(
            classes,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = {'detail': 'Classes Updated Sucecssfully'}
        logger.info(response)

        return Response(response, status=status.HTTP_200_OK)

    #? Delete Classes of given Id
    @extend_schema(
        description=
        'Deletes the Classes of the given Id.\n\nargs: pk\n\nAccessible by: Admin, HOD, Teacher',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(description='Classes Deleted Successfully'),
            #? 404
            status.HTTP_404_NOT_FOUND:
            OpenApiResponse(description='Not found')
        })
    def delete(self, request, *args, **kwargs):
        classes = self.get_object()
        classes.delete()

        response = {'detail': 'Classes Deleted Successfully'}
        logger.info(response)

        return Response(response, status=status.HTTP_200_OK)
