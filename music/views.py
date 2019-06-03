from rest_framework import generics
from .helpers.uploader import uploader
from .helpers.permissions import IsOwnerOrReadOnly
from .models import Songs
from .serializers import (SongsSerializer, TABLE)
from .helpers.decorators import validate_request_data

from rest_framework.response import Response
from rest_framework.views import status


LOOKUP_FIELD = 'title'


def get_song(title):
    """
    Get a song from the provided title.
    """
    try: 
        song = TABLE.objects.get(title=title)
        return song
    except TABLE.DoesNotExist:
        return Response(
            data={
                "message": "Song with title: {} does not exist"
            },
            status=status.HTTP_404_NOT_FOUND
        )
# Create your views here.

class ListCreateSongsView(generics.ListAPIView):
    """
    Provides a GET and POST method handler.
    """
    queryset = Songs.objects.all()
    serializer_class = SongsSerializer

    @validate_request_data
    def post(self, request, *args, **kwargs):
        image = None
        if request.data.get('image_file'):
            image = uploader(request.data.get('image_file'))
            image = image.get('secure_url')
            del request.data['image_file']

        else:
            song = Songs.objects.create(
                title = request.data["title"],
                artist = request.data["artist"],
                album = request.data["album"],
                image = request.data["image"]
            )

        return Response(
            data=SongsSerializer(song).data,
            status=status.HTTP_201_CREATED
        )

class SongsDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Provides:
        GET songs/:id/
        PUT songs/:id/
        DELETE songs/:id/
    """
    permission_classes = [IsOwnerOrReadOnly,]
    queryset = Songs.objects.all()
    serializer_class = SongsSerializer
    lookup_field = LOOKUP_FIELD

    def get(self, request, *args, **kwargs):
        try:
            song = self.queryset.get(pk=kwargs["pk"])
            return Response(SongsSerializer(song).data)
        except Songs.DoesNotExist:
            return Response(
                data={
                    "message": "Song with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    @validate_request_data
    def put(self, request, *args, **kwargs):
        try:
            song = self.queryset.get(pk=kwargs["pk"])
            serializer = SongsSerializer()
            update_song = serializer.update(song, request.data)
            return Response(SongsSerializer(update_song).data)
        except Songs.DoesNotExist:
            return Response(
                data={
                    "message": "Song with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            song = self.queryset.get(pk=kwargs["pk"])
            song.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Songs.DoesNotExist:
            return Response(
                data={
                    "message": "Song with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )