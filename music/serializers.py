from rest_framework import serializers
from django.apps import apps
from .models import Songs

TABLE = apps.get_model('music', 'Songs')

NAMESPACE = 'music_api'
fields = ('id', 'title', 'artist', 'album')


class SongsSerializer(serializers.ModelSerializer):
    """
    Song Serializer.
    """
    class Meta:
        """
        Metadata description.
        """
        model = TABLE
        fields = fields

    def update(self, instance, validated_data):
        instance.title = validated_data("title", instance.title)
        instance.artist = validated_data("artist", instance.artist)
        instance.album = validated_data("album", instance.album)
        instance.save()

        return instance

    

