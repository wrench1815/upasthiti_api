import logging

from drf_spectacular.utils import OpenApiResponse, extend_schema

from rest_framework import generics, permissions, status
from rest_framework.response import Response

from . import serializers, models

from user.permissions import UserIsAdmin, UserIsHOD, UserIsTeacher

logger = logging.getLogger(__name__)


class StudentListCreateAPIView(generics.ListCreateAPIView):
    '''
        Allowed methods: GET, POST

        GET: Returns list of all Students
        POST: Creates a new Student object

        Accessible by: Admin, HOD, Teacher
    '''
    queryset = models.StudentModel.objects.all()
    serializer_class = serializers.StudentFullSerializer
    permission_classes = [
        permissions.IsAuthenticated & (UserIsAdmin | UserIsHOD | UserIsTeacher)
    ]

    #? create a new Student Object
    @extend_schema(
        request=serializers.StudentSerializer,
        responses={
            #? 201
            status.HTTP_201_CREATED:
            OpenApiResponse(description='Student Added Successfully'),
            #? 400
            status.HTTP_400_BAD_REQUEST:
            OpenApiResponse({})
        },
        description='Creates a new Student Object.')
    def post(self, request, *args, **kwargs):
        serializer = serializers.StudentSerializer(data=request.data,many=True)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()

        except Exception as ex:
            logger.error(str(ex))

            return Response({'detail': str(ex)},
                            status=status.HTTP_400_BAD_REQUEST)

        response = {'detail': 'Student Added Successfully'}
        logger.info(response)

        return Response(response, status=status.HTTP_201_CREATED)


class StudentRetrieveUpdateDestroyAPIView(generics.GenericAPIView):
    '''
        Allowed methods: GET, PATCH, DELETE

        GET: Return Student of given Id
        PATCH: Update Student of given Id with Validated data provided
        DELETE: Delete Student of given Id

        Note: Updatation on Student is done via Partial Update method

        args: pk
        
        Accessible by: Admin, HOD, Teacher
    '''
    queryset = models.StudentModel.objects.all()
    serializer_class = serializers.StudentSerializer
    permission_classes = [
        permissions.IsAuthenticated & (UserIsAdmin | UserIsHOD | UserIsTeacher)
    ]
    lookup_field = 'pk'

    #? get single Student
    @extend_schema(
        description=
        'Returns Single Student on Application of given Id.\n\nargs: pk\n\nAccessible by: Admin, Teacher',
        responses={
            #? 200
            status.HTTP_200_OK:
            serializers.StudentFullSerializer,
            #? 404
            status.HTTP_404_NOT_FOUND:
            OpenApiResponse(description='Not found')
        })
    def get(self, request, *args, **kwargs):
        student = self.get_object()
        serializer = serializers.StudentFullSerializer(student)
        return Response(serializer.data)

    #? Update Student of given Id
    @extend_schema(
        request=serializers.StudentSerializer,
        description=
        'Updates the Student of given Id with the provided Data.\n\nargs: pk\n\nAccessible by: Admin, Teacher',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(description='Student Updated Successfully'),
            #? 404
            status.HTTP_404_NOT_FOUND:
            OpenApiResponse(description='Not found')
        })
    def patch(self, request, *args, **kwargs):
        student = self.get_object()
        serializer = serializers.StudentSerializer(
            student,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = {'detail': 'Student Updated Sucecssfully'}
        logger.info(response)

        return Response(response, status=status.HTTP_200_OK)

    #? Delete Student of given Id
    @extend_schema(
        description=
        'Deletes the Student of the given Id.\n\nargs: pk\n\nAccessible by: Admin, Teacher',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(description='Student Deleted Successfully'),
            #? 404
            status.HTTP_404_NOT_FOUND:
            OpenApiResponse(description='Not found')
        })
    def delete(self, request, *args, **kwargs):
        student = self.get_object()
        student.delete()

        response = {'detail': 'Student Deleted Successfully'}
        logger.info(response)

        return Response(response, status=status.HTTP_200_OK)
