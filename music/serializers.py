from rest_framework import serializers
from django.apps import apps
from .helpers.uploader import uploader
from django.contrib.auth.models import AnonymousUser
from .models import Songs

TABLE = apps.get_model('music', 'Songs')

NAMESPACE = 'music_api'
fields = ('id', 'image', 'title', 'artist', 'album')


class SongsSerializer(serializers.ModelSerializer):
    """
    Song Serializer.
    """
    image_file = serializers.ImageField(required=False)
    update_url = serializers.HyperlinkedIdentityField(
        view_name=NAMESPACE + ':update', lookup_field='title'
    )
    delete_url = serializers.HyperlinkedIdentityField(
        view_name=NAMESPACE + ':delete', lookup_field='title'
    )

    class Meta:
        """
        Metadata description.
        """
        model = TABLE
        fields = fields

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.artist = validated_data.get("artist", instance.artist)
        instance.album = validated_data.get("album", instance.album)

        if validated_data.get("image_file"):
            image = uploader(validated_data.get("image_file"))
            instance.image = image.get("secure_url", instance.image)

        instance.save()

        return instance
