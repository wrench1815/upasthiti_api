from rest_framework import serializers


class ImageUploadResposeSerializer(serializers.Serializer):
    image_url = serializers.URLField()
    public_id = serializers.CharField()
