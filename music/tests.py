import json
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Songs
from .serializers import SongsSerializer

# Create your tests here.
class SongsModelTest(APITestCase):
    def setUp(self):
        self.song = Songs.objects.create(
            title="Zaidi",
            artist="Jux",
            album="Zaidi"
        )

    def test_song(self):
        """
        This test ensures that the song created in the setup exists.
        """
        self.assertEqual(self.song.title, "Zaidi")
        self.assertEqual(self.song.artist, "Jux")
        self.assertEqual(self.song.album, "Zaidi")
        self.assertEqual(str(self.song), "Zaidi - Jux")


# tests for views

class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_song(title="", artist="", album=""):
        """
        Create a song in the db
        :param title:
        :param artist:
        :param album:
        :return:
        """
        if title != "" and artist != "" and album != "":
            Songs.objects.create(title=title, artist=artist, album=album)

    def make_a_request(self, kind="post", **kwargs):
        """
        Make a post request to create a song.
        :param kind: HTTP VERB
        :return:
        """
        if kind == "post":
            return self.client.post(
                reverse(
                    "songs-list-create",
                    kwargs={
                        "version": kwargs["version"]
                    }
                ),
                data=json.dumps(kwargs["data"]),
                content_type='application/json'
            )
        elif kind == "put":
            return self.client.put(
                reverse(
                    "songs-detail",
                    kwargs={
                        "version": kwargs["version"],
                        "pk": kwargs["id"]
                    }
                ),
                data=json.dumps(kwargs["data"]),
                content_type='application/json'
            )
        else:
            return None

    def fetch_song(self, pk=0):
        return self.client.get(
            reverse(
                "songs-detail",
                kwargs={
                    "version": "v1",
                    "pk": pk
                }
            )
        )

    def delete_song(self, pk=0):
        return self.client.delete(
            reverse(
                "songs-detail",
                kwargs={
                    "version": "v1",
                    "pk": pk
                }
            )
        )

    def setUp(self):
        # add test data
        self.create_song("Coolest kid in Africa", "Davido ft Nasty C", "African Boy")
        self.create_song("Simple song", "Konshens", "Koshens collection")
        self.create_song("Ipepete", "Masauti", "Cool Kid")
        self.create_song("God's plan", "Drake", "Mirage")
        self.valid_data ={
            "title": "test song",
            "artist": "test artist",
            "album": "test album"
        }
        self.invalid_data = {
            "title": "",
            "artist": "",
            "album": ""
        }
        self.valid_song_id = 1
        self.invalid_song_id = 100

class GetAllSongsTest(BaseViewTest):
    def test_get_all_songs(self):
        """
        This test ensures that all songs added in the setUp method
        exist when we make a GET request to the songs/ endpoint.
        """
        # hit the API endpoint
        response = self.client.get(
            reverse("songs-list-create", kwargs={"version": "v1"})
        )
        # fetch the data from db
        expected = Songs.objects.all()
        serialized = SongsSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetASingleSongTest(BaseViewTest):
    
    def test_get_single_song(self):
        """
        This test ensures that a single song of a given id is returned.
        """
        res = self.make_a_request(
            kind="post",
            version="v1",
            data=self.valid_data
        )
        response = self.fetch_song(self.valid_song_id)
        # fetch the data from db
        expected = Songs.objects.get(pk=self.valid_song_id)
        serialized = SongsSerializer(expected)

        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # test with a song that does not not exist
        response = self.fetch_song(self.invalid_song_id)
        self.assertEqual(
            response.data["message"],
            "Song with id: 100 does not exist"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class AddSongsTest(BaseViewTest):

    def test_create_song(self):
        """
        This test ensures that a songle song can be added.
        """
        response = self.make_a_request(
            kind="post",
            version="v1",
            data=self.valid_data
        )
        self.assertEqual(response.data, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # test with invalid data
        response = self.make_a_request(
            kind="post",
            version="v1",
            data=self.invalid_data
        )
        self.assertEqual(
            response.data["message"],
            'Both title, artist and album are required to add a song'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UpdateSongsTest(BaseViewTest):

    def test_update_song(self):
        """
        This test ensure that when a single song can be updated. In this
        test we can update the second song in the db with valid data and 
        the third song with invalid data and make assertions.
        """
        response = self.make_a_request(
            kind="put",
            version="v1",
            id=2,
            data=self.valid_data
        )
        import pdb;pdb.set_trace()
        self.assertEqual(response.data, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # test with invalid data
        response = self.make_a_request(
            kind="put",
            version="v1",
            id=3,
            data=self.invalid_data
        )
        self.assertEqual(
            response.data["message"],
            "Both title, artist and album are required to add a song"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class DeleteSongsTest(BaseViewTest):

    def test_delete_song(self):
        """
        This test ensures that when a song of given id can be deleted.
        """
        response = self.make_a_request(
            kind="post",
            version="v1",
            data=self.valid_data
        )
        self.assertEqual(response.data, self.valid_data)
        response = self.delete_song(1)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
