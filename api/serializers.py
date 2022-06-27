from rest_framework import serializers

#? max size 3 mb
MAX_UPLOAD_SIZE = 3145728


class ImageUploadSerializer(serializers.Serializer):
    '''
        Serializer to Upload Images and delete when needed
    '''
    image = serializers.ImageField(required=True)
    folder = serializers.CharField(required=True)
    public_id = serializers.CharField(required=False)

    def validate_image(self, value):
        '''
            Validations for image

            Validates if its Empty
            Validates if its a valid image
            Validates if its of a valid size
        '''
        if not value:
            raise serializers.ValidationError('No image provided.')

        #? check image format
        if value.content_type not in [
                'image/jpeg',
                'image/png',
                'image/x-icon',
        ]:
            raise serializers.ValidationError(
                'Image must be a JPEG or PNG or ICO.')

        #? check image size
        if value.size > MAX_UPLOAD_SIZE:
            raise serializers.ValidationError(
                'Image size must be less than 3 MB.')

        return value

    def validate_folder(self, value):
        '''
            Validations for folder
            
            Validates if folder is empty
        '''
        if not value:
            raise serializers.ValidationError('No folder provided.')

        return value
