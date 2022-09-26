import logging

from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from drf_spectacular.types import OpenApiTypes

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter

from django_filters.rest_framework import DjangoFilterBackend

from django.conf import settings

from . import serializers, models

from user.permissions import UserIsAdmin, UserIsHOD, UserIsTeacher

from api.paginator import StandardPagination

logger = logging.getLogger(__name__)


@extend_schema_view(
    post=extend_schema(
        request=serializers.StudentCreateUpdateSerializerFull,
        responses={
            #? 201
            status.HTTP_201_CREATED:
            OpenApiResponse(
                description='Student Added Successfully',
                response=serializers.StudentCreateUpdateSerializerFull,
            ),
            #? 400
            status.HTTP_400_BAD_REQUEST:
            OpenApiResponse(
                description='Bad Request',
                response=OpenApiTypes.OBJECT,
            )
        },
        description=
        'Allowed methods: GET, POST \n\nPOST: Creates a new Student object\n\nAccessible by: Admin, HOD, Teacher',
    ),
    get=extend_schema(
        request=serializers.StudentFullSerializer,
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(
                description='Student List',
                response=serializers.StudentFullSerializer,
            ),
            #? 400
            status.HTTP_400_BAD_REQUEST:
            OpenApiResponse(
                description='Bad Request',
                response=OpenApiTypes.OBJECT,
            ),
        },
        description=
        'Returns list of all Students.\n\nOrdering:\n\n- default: -created_on\n\n- allowed: created_on, -created_on'
    ),
)
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
    pagination_class = StandardPagination
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_on']
    ordering = '-created_on'

    #? create a new Student Object
    def post(self, request, *args, **kwargs):
        serializer = serializers.StudentCreateUpdateSerializerFull(
            data=request.data)
        serializer.is_valid(raise_exception=True)

        #? collect list of all Colleges and Universities passed
        college_roll_list = serializer.validated_data['college']
        uni_roll_list = serializer.validated_data['university']

        #? change the serializer and re-validate
        #? reason: to easen the burden of having to remove uneeded fields
        serializer = serializers.StudentCreateUpdateSerializer(
            data=request.data)
        serializer.is_valid(raise_exception=True)

        student = None
        college_set = True
        university_set = True

        try:
            #? Create the Student as per updated Serializer
            student = serializer.save()

            #? Assign college roll no and college if exist or create if needed
            if len(college_roll_list) != 0:
                for item in college_roll_list:
                    col_roll, _ = models.CollegeRollNo.objects.get_or_create(
                        class_roll_no=item['class_roll_no'],
                        college=item['college'],
                    )
                    if col_roll.student:
                        college_set = False

                    col_roll.student = student
                    col_roll.save()

            #? Assign University roll no and University if exist or create if needed
            if len(uni_roll_list) != 0:
                for item in uni_roll_list:
                    uni_roll, _ = models.UniversityRollNo.objects.get_or_create(
                        university_roll_no=item['university_roll_no'],
                        university=item['university'],
                    )
                    if uni_roll.student:
                        university_set = False

                    uni_roll.student = student
                    uni_roll.save()

        except Exception as ex:
            logger.error(str(ex))

            return Response(
                {'detail': str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        response = serializers.StudentFullSerializer(student).data
        #! Runs only if DEBUG = True
        if settings.DEBUG:
            logger.info(response)
        logger.info('Student Added Successfully')

        #? check if any error occured and add their message to the response
        errors = {}
        if not college_set:
            errors['college'] = [
                'Student with the College Roll no already Exist.'
            ]
        if not university_set:
            errors['unoversity'] = [
                'Student with the Univerity Roll no already Exist.'
            ]
        if not college_set or not university_set:
            response['error'] = errors

        return Response(response, status=status.HTTP_201_CREATED)


@extend_schema_view(
    get=extend_schema(
        description=
        'Returns Single Student on Application of given Id.\n\nargs: pk\n\nAccessible by: Admin, Teacher',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(
                description='Student Details',
                response=serializers.StudentFullSerializer,
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
        request=serializers.StudentCreateUpdateSerializerFull,
        description=
        'Updates the Student of given Id with the provided Data.\n\nargs: pk\n\nAccessible by: Admin, Teacher',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(
                description='Student Updated Successfully',
                response=OpenApiTypes.OBJECT,
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
    delete=extend_schema(
        description=
        'Deletes the Student of the given Id.\n\nargs: pk\n\nAccessible by: Admin, Teacher',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(description='Student Deleted Successfully', ),
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
    serializer_class = serializers.StudentFullSerializer
    permission_classes = [
        permissions.IsAuthenticated & (UserIsAdmin | UserIsHOD | UserIsTeacher)
    ]
    lookup_field = 'pk'

    #? get single Student
    def get(self, request, *args, **kwargs):
        student = self.get_object()
        serializer = serializers.StudentFullSerializer(student)
        return Response(serializer.data)

    #? Update Student of given Id
    def patch(self, request, *args, **kwargs):
        student = self.get_object()
        college_set = True
        university_set = True

        serializer = serializers.StudentCreateUpdateSerializerFull(
            student,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        #? collect list of all Colleges and Universities passed
        college_roll_list = serializer.validated_data['college']
        uni_roll_list = serializer.validated_data['university']

        #? change the serializer and re-validate
        #? reason: to easen the burden of having to remove uneeded fields
        serializer = serializers.StudentCreateUpdateSerializer(
            student,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        try:
            #? Create the Student as per updated Serializer
            student = serializer.save()

            #? Assign college roll no and college if exist or create if needed
            if len(college_roll_list) != 0:
                for item in college_roll_list:
                    col_roll, _ = models.CollegeRollNo.objects.get_or_create(
                        class_roll_no=item['class_roll_no'],
                        college=item['college'],
                    )
                    if col_roll.student and col_roll.student.id != student.id:
                        college_set = False

                    col_roll.student = student
                    col_roll.save()
            elif len(college_roll_list) == 0:
                student.student_college_roll.clear()

            #? Assign University roll no and University if exist or create if needed
            if len(uni_roll_list) != 0:
                for item in uni_roll_list:
                    uni_roll, _ = models.UniversityRollNo.objects.get_or_create(
                        university_roll_no=item['university_roll_no'],
                        university=item['university'],
                    )
                    if uni_roll.student and uni_roll.student.id != student.id:
                        university_set = False

                    uni_roll.student = student
                    uni_roll.save()
            elif len(uni_roll_list) == 0:
                student.student_university_roll.clear()

        except Exception as ex:
            logger.error(str(ex))

            return Response(
                {'detail': str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        response = {'detail': ['Student Updated Successfully']}

        #! Runs only if DEBUG = True
        if settings.DEBUG:
            logger.info(serializers.StudentFullSerializer(student).data)

        logger.info('Student Updated Successfully')

        #? check if any error occured and add their message to the response
        errors = {}
        if not college_set:
            errors['college'] = [
                'Student with the College Roll no already Exist.'
            ]
        if not university_set:
            errors['unoversity'] = [
                'Student with the Univerity Roll no already Exist.'
            ]
        if not college_set or not university_set:
            response['error'] = errors

        return Response(response, status=status.HTTP_200_OK)

    #? Delete Student of given Id
    def delete(self, request, *args, **kwargs):
        student = self.get_object()

        #! Unlink all related values
        student.student_college_roll.clear()
        student.student_university_roll.clear()

        #! Delete the Student
        student.delete()

        response = {'detail': ['Student Deleted Successfully']}
        logger.info(response)

        return Response(response, status=status.HTTP_200_OK)


class StudentBulkCreateAPIView(generics.CreateAPIView):
    '''
        Allowed methods: Bulk Post

        
        POST: Bulk Creates Student objects

        Accessible by: Admin, HOD, Teacher
    '''
    queryset = models.StudentModel.objects.all()
    serializer_class = serializers.StudentFullSerializer
    permission_classes = [
        permissions.IsAuthenticated & (UserIsAdmin | UserIsHOD | UserIsTeacher)
    ]

    #? Bulk Create Student Objects
    @extend_schema(
        request=serializers.StudentSerializer,
        responses={
            #? 201
            status.HTTP_201_CREATED:
            OpenApiResponse(description='Students Added Successfully'),
            #? 400
            status.HTTP_400_BAD_REQUEST:
            OpenApiResponse({})
        },
        description=
        'Bulk Post Students \n\nPOST: Bulk Creates Student objects \n\nAccessible by: Admin, HOD, Teacher',
    )
    def post(self, request, *args, **kwargs):
        serializer = serializers.StudentSerializer(
            data=request.data,
            many=True,
        )
        serializer.is_valid(raise_exception=True)

        try:

            serializer.save()

        except Exception as ex:
            logger.error(str(ex))

            return Response({'detail': str(ex)},
                            status=status.HTTP_400_BAD_REQUEST)

        response = {'detail': ['Students Added Successfully']}
        logger.info(response)

        return Response(response, status=status.HTTP_201_CREATED)
