import datetime
import logging
import string
from datetime import date, datetime

from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from drf_spectacular.types import OpenApiTypes

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter

from dateutil.relativedelta import relativedelta

from django.utils.crypto import get_random_string
from django.conf import settings

from . import serializers, models

from user.permissions import UserIsAdmin, UserIsHOD, UserIsTeacher
from api.paginator import StandardPagination

logger = logging.getLogger(__name__)


@extend_schema_view(
    post=extend_schema(
        request=serializers.ClassSerializer,
        responses={
            #? 201
            status.HTTP_201_CREATED:
            OpenApiResponse(
                description='Class Added Successfully',
                response=serializers.ClassSerializer,
            ),
            #? 400
            status.HTTP_400_BAD_REQUEST:
            OpenApiResponse(
                description='Bad Request',
                response=OpenApiTypes.OBJECT,
            ),
        },
        description='Creates a new Class.'),
    get=extend_schema(
        request=serializers.ClassFullSerializer,
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(
                description='Class List',
                response=serializers.ClassFullSerializer,
            ),
            #? 400
            status.HTTP_400_BAD_REQUEST:
            OpenApiResponse(
                description='Bad Request',
                response=OpenApiTypes.OBJECT,
            ),
        },
        description=
        'Returns list of all Classes.\n\nOrdering:\n\n- default: -created_on\n\n- allowed: created_on, -created_on'
    ),
)
class ClassListCreateAPIView(generics.ListCreateAPIView):
    '''
        Allowed methods: GET, POST

        GET: Returns list of all Classes
        POST: Creates a new Class

        Accessible by: Admin, HOD, Teacher
    '''
    queryset = models.ClassModel.objects.all()
    serializer_class = serializers.ClassFullSerializer
    permission_classes = [
        permissions.IsAuthenticated & (UserIsAdmin | UserIsHOD | UserIsTeacher)
    ]
    pagination_class = StandardPagination
    filter_backends = [
        OrderingFilter,
    ]
    ordering_fields = ['created_on']
    ordering = '-created_on'

    #? create a new Class
    def post(self, request, *args, **kwargs):
        serializer = None

        try:
            # generate a unique code for class
            allowed_code_chars = string.ascii_letters + string.digits + '-_+'
            code = None

            while True:
                code = get_random_string(14, allowed_code_chars)

                logger.info(code)

                if not models.ClassModel.objects.filter(code=code).exists():
                    break

            request.data['code'] = code

            #? calculate session end
            #! calculation is done in consideration that each semester is 6 months long
            #! this calculation is a rought estimate that the semester will end in 6 months
            #! during calculation, day, i.e 12 8 2022 the 12, is not considered and calculation is done considering the month only regardless of day
            session_end = datetime.strptime(
                request.data['session_start'],
                '%Y-%m-%d',
            ).date() + relativedelta(months=6)

            request.data['session_end'] = session_end.isoformat()

            serializer = serializers.ClassSerializer(data=request.data)

            serializer.is_valid(raise_exception=True)

            serializer.save()

            #? log created data if debug
            if settings.DEBUG:
                logger.info(serializer.data)

        except Exception as ex:
            logger.error(str(ex))

            return Response({'detail': str(ex)},
                            status=status.HTTP_400_BAD_REQUEST)

        response = serializer.data
        logger.info('Class Added Successfully')

        return Response(response, status=status.HTTP_201_CREATED)


@extend_schema_view(
    get=extend_schema(
        description='Returns Single Class of given Id.\n\nargs: pk',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(
                description='Class Details',
                response=serializers.ClassFullSerializer,
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
        request=serializers.ClassSerializer,
        description=
        'Updates the Class of given Id with the provided Data.\n\nargs: pk',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(description='Class Updated Successfully', ),
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
        description='Deletes the Class of the given Id.\n\nargs: pk',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(description='Class Deleted Successfully', ),
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
class ClassRetrieveUpdateDestroyAPIView(generics.GenericAPIView):
    '''
        Allowed methods: GET, PATCH, DELETE

        GET: Return Class of given Id
        PATCH: Update Class of given Id with Validated data provided
        DELETE: Delete Class of given Id

        Note: Updatation on Class is done via Partial Update method

        args: pk
        
        Accessible by: Admin, HOD, Teacher
    '''
    queryset = models.ClassModel.objects.all()
    serializer_class = serializers.ClassSerializer
    permission_classes = [
        permissions.IsAuthenticated & (UserIsAdmin | UserIsHOD | UserIsTeacher)
    ]
    lookup_field = 'pk'

    #? get single Class
    def get(self, request, *args, **kwargs):
        single_class = self.get_object()
        serializer = serializers.ClassFullSerializer(single_class)
        return Response(serializer.data)

    #? Update Class of given Id
    def patch(self, request, *args, **kwargs):
        try:
            single_class = self.get_object()

            #? calculate session end
            #! calculation is done in consideration that each semester is 6 months long
            #! this calculation is a rought estimate that the semester will end in 6 months
            #! during calculation, day, i.e 12 8 2022 the 12, is not considered and calculation is done considering the month only regardless of day
            session_end = datetime.strptime(
                request.data['session_start'],
                '%Y-%m-%d',
            ).date() + relativedelta(months=6)

            request.data['session_end'] = session_end.isoformat()

            serializer = serializers.ClassSerializer(
                single_class,
                data=request.data,
                partial=True,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            #? log updated data if debug
            if settings.DEBUG:
                logger.info(serializer.data)
        except Exception as ex:
            logger.error(str(ex))

            return Response({'detail': str(ex)},
                            status=status.HTTP_400_BAD_REQUEST)

        response = {'detail': ['Class Updated Sucecssfully']}
        logger.info(response)

        return Response(response, status=status.HTTP_200_OK)

    #? Delete Class of given Id
    def delete(self, request, *args, **kwargs):
        single_class = self.get_object()

        #? unlink student
        if single_class.college:
            single_class.college.classmodel_set.remove(single_class)

        #? unlink department
        if single_class.department:
            single_class.department.classmodel_set.remove(single_class)

        #? unlink course
        if single_class.course:
            single_class.course.classmodel_set.remove(single_class)

        #? unlink teacher
        if single_class.teacher:
            single_class.teacher.classmodel_set.remove(single_class)

        #? unlink student
        if single_class.student:
            single_class.student.classmodel_set.remove(single_class)

        #? delete class
        single_class.delete()

        response = {'detail': ['Class Deleted Successfully']}
        logger.info(response)

        return Response(response, status=status.HTTP_200_OK)
