from rest_framework import generics
from .models import Songs
from .serializers import SongsSerializer
from .helpers.decorators import validate_request_data

from rest_framework.response import Response
from rest_framework.views import status

# Create your views here.

class ListCreateSongsView(generics.ListAPIView):
    """
    Provides a GET and POST method handler.
    """
    queryset = Songs.objects.all()
    serializer_class = SongsSerializer

    @validate_request_data
    def post(self, request, *args, **kwargs):
        song = Songs.objects.create(
            title = request.data["title"],
            artist = request.data["artist"],
            album = request.data["album"]
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
    queryset = Songs.objects.all()
    serializer_class = SongsSerializer

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