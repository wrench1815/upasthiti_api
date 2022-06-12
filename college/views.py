import logging

from drf_spectacular.utils import OpenApiResponse, extend_schema

from rest_framework import generics, permissions, status
from rest_framework.response import Response

from . import serializers, models

from user.permissions import UserIsAdmin

logger = logging.getLogger(__name__)


class CollegeListCreateAPIView(generics.ListCreateAPIView):
    '''
        Allowed methods: GET, POST

        GET: Returns list of all Colleges
        POST: Creates a new College object

        Accessible by: Admin
    '''
    queryset = models.CollegeModel.objects.all()
    serializer_class = serializers.CollegeFullSerializer
    permission_classes = [permissions.IsAuthenticated & (UserIsAdmin)]

    #? create a new College Object
    @extend_schema(
        request=serializers.CollegeSerializer,
        responses={
            #? 201
            status.HTTP_201_CREATED:
            OpenApiResponse(description='College Added Successfully'),
            #? 400
            status.HTTP_400_BAD_REQUEST:
            OpenApiResponse({})
        },
        description='Creates a new College Object.')
    def post(self, request, *args, **kwargs):
        serializer = serializers.CollegeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()

        except Exception as ex:
            logger.error(str(ex))

            return Response({'detail': str(ex)},
                            status=status.HTTP_400_BAD_REQUEST)

        response = {'detail': 'College Added Successfully'}
        logger.info(response)

        return Response(response, status=status.HTTP_201_CREATED)


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
    queryset = models.CollgeModel.objects.all()
    serializer_class = serializers.CollegeSerializer
    permission_classes = [permissions.IsAuthenticated & (UserIsAdmin)]
    lookup_field = 'pk'

    #? get single Collge
    @extend_schema(
        description=
        'Returns Single College on Application of given Id.\n\nargs: pk\n\nAccessible by: Admin',
        responses={
            #? 200
            status.HTTP_200_OK:
            serializers.CollegeFullSerializer,
            #? 404
            status.HTTP_404_NOT_FOUND:
            OpenApiResponse(description='Not found')
        })
    def get(self, request, *args, **kwargs):
        college = self.get_object()
        serializer = serializers.CollegeFullSerializer(college)
        return Response(serializer.data)

    #? Update College of given Id
    @extend_schema(
        request=serializers.CollegeSerializer,
        description=
        'Updates the College of given Id with the provided Data.\n\nargs: pk\n\nAccessible by: Admin',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(description='College Updated Successfully'),
            #? 404
            status.HTTP_404_NOT_FOUND:
            OpenApiResponse(description='Not found')
        })
    def patch(self, request, *args, **kwargs):
        college = self.get_object()
        serializer = serializers.CollegeSerializer(
            college,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = {'detail': 'College Updated Sucecssfully'}
        logger.info(response)

        return Response(response, status=status.HTTP_200_OK)

    #? Delete college of given Id
    @extend_schema(
        description=
        'Deletes the College of the given Id.\n\nargs: pk\n\nAccessible by: Admin',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(description='College Deleted Successfully'),
            #? 404
            status.HTTP_404_NOT_FOUND:
            OpenApiResponse(description='Not found')
        })
    def delete(self, request, *args, **kwargs):
        college = self.get_object()
        college.delete()

        response = {'detail': 'College Deleted Successfully'}
        logger.info(response)

        return Response(response, status=status.HTTP_200_OK)
