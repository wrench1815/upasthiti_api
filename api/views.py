from collections import OrderedDict
import logging

import cloudinary.uploader

from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from drf_spectacular.types import OpenApiTypes

from rest_framework import generics, permissions, status
from rest_framework.response import Response

from . import serializers, response_serializers

#? set logger
logger = logging.getLogger(__name__)


@extend_schema_view(
    post=extend_schema(
        request=serializers.ImageUploadSerializer,
        responses={
            #? 201
            status.HTTP_201_CREATED:
            OpenApiResponse(
                description='Image Uploaded Successfully',
                response=response_serializers.ImageUploadResposeSerializer),
            #? 400
            status.HTTP_400_BAD_REQUEST:
            OpenApiResponse(response=OpenApiTypes.OBJECT)
        },
        description=
        'Uploads an image to cloudinary and returns the url.\n\noptional: Deletes an image if public_id is passed\n\nAccessible by: Authenticated',
    ), )
class ImageUploadAPIView(generics.CreateAPIView):
    '''
        Allowed methods: POST

        Uploads an image to cloudinary and returns the url.

        optional: Deletes an image if public_id is passed.
            
        Accessible by: Authenticated
    '''

    serializer_class = serializers.ImageUploadSerializer
    permission_classes = [permissions.IsAuthenticated]

    #? upload Image to Cloudinary and return its url
    def post(self, request, *args, **kwargs):
        request_data = OrderedDict()
        request_data.update(request.data)

        # if public_id does not exist in request set public_id to ''
        if 'public_id' not in request_data:
            request_data['public_id'] = ''

        instance = self.get_serializer(data=request_data)
        instance.is_valid(raise_exception=True)

        try:
            #? upload image to cloudinary
            uploaded_image = cloudinary.uploader.upload(
                instance.validated_data['image'],
                folder=instance.validated_data['folder'],
            )

            #? remove api_key
            uploaded_image.pop('api_key')
            logger.info(uploaded_image)

            #? if public_id is provided delete the image from cloudinary
            if instance.validated_data['public_id']:
                delete_image = cloudinary.uploader.destroy(
                    public_id=instance.validated_data['public_id'], )

                logger.info(delete_image)

        except Exception as ex:
            logger.error(str(ex))

            return Response({'detail': str(ex)},
                            status=status.HTTP_400_BAD_REQUEST)

        response = {
            'image_url': uploaded_image['secure_url'],
            'public_id': uploaded_image['public_id'],
        }
        logger.info(response)

        return Response(response, status=status.HTTP_201_CREATED)
