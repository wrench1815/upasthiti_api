import logging

from drf_spectacular.utils import OpenApiResponse, extend_schema

from django.contrib.auth import get_user_model

from rest_framework import generics, permissions, status
from rest_framework.response import Response

from user.serializers import UserSerializer

User = get_user_model()
logger = logging.getLogger(__name__)


class AuthMeApiView(generics.GenericAPIView):
    '''
        Allowed methods: GET

        GET: Returns data of Currently Logged in User

        Accessible by: Any Authenticated User
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        responses={
            200:
            UserSerializer,
            401:
            OpenApiResponse(
                description='Authentication credentials were not provided.')
        },
        operation_id='user_me',
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)
