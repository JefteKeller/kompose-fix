from django.test import TestCase
from rest_framework.test import APIClient


class TestSongView(TestCase):
    SONGS_URL = '/api/songs/'
    SONGS_URL_ID_1 = '/api/songs/1/'
    SONGS_URL_ID_2 = '/api/songs/2/'

    @classmethod
    def setUpTestData(cls):

        cls.artist_data = {'name': 'John Doe'}
        cls.artist_data_2 = {'name': 'Marie Jane'}
        cls.invalid_artist_data = {'login': 'majae'}

        cls.song_data = {'title': 'Sunshine'}
        cls.song_data_2 = {'title': 'One'}

        cls.invalid_song_data = {'track': 'You and I'}

        cls.valid_song_data = {**cls.song_data, 'artist': {**cls.artist_data}}
        cls.valid_song_data_2 = {**cls.song_data_2, 'artist': {**cls.artist_data_2}}

        cls.expected_song_data = {
            'id': 1,
            **cls.song_data,
            'artist': {'id': 1, **cls.artist_data},
            'votes': 1,
        }
        cls.expected_song_data_2 = {
            'id': 2,
            **cls.song_data_2,
            'artist': {'id': 2, **cls.artist_data_2},
            'votes': 1,
        }

    def setUp(self) -> None:
        self.client = APIClient()

    def test_should_not_create_song_with_invalid_data(self):

        invalid_data = {**self.invalid_artist_data, **self.invalid_song_data}
        incomplete_data = {**self.song_data}

        response_invalid_data = self.client.post(
            self.SONGS_URL, invalid_data, format='json'
        )
        self.assertEqual(response_invalid_data.status_code, 400)

        response_incomplete_data = self.client.post(
            self.SONGS_URL, incomplete_data, format='json'
        )
        self.assertEqual(response_incomplete_data.status_code, 400)

    def test_should_create_song_with_valid_data(self):

        response_valid_song_data = self.client.post(
            self.SONGS_URL, self.valid_song_data, format='json'
        )
        response_valid_song_data_2 = self.client.post(
            self.SONGS_URL, self.valid_song_data_2, format='json'
        )

        self.assertEqual(response_valid_song_data.status_code, 201)
        self.assertEqual(response_valid_song_data.json(), self.expected_song_data)

        self.assertEqual(response_valid_song_data_2.status_code, 201)
        self.assertEqual(response_valid_song_data_2.json(), self.expected_song_data_2)

    def test_should_list_songs(self):
        expected_song_list = []
        expected_song_list_2 = [self.expected_song_data, self.expected_song_data_2]

        response_list_songs = self.client.get(self.SONGS_URL)

        self.assertEqual(response_list_songs.status_code, 200)
        self.assertEqual(response_list_songs.json(), expected_song_list)

        self.client.post(self.SONGS_URL, self.valid_song_data, format='json')
        self.client.post(self.SONGS_URL, self.valid_song_data_2, format='json')

        response_list_songs_2 = self.client.get(self.SONGS_URL)

        self.assertEqual(response_list_songs_2.status_code, 200)
        self.assertEqual(response_list_songs_2.json(), expected_song_list_2)

    def test_list_song_by_id_should_return_404_with_invalid_id(self):
        response = self.client.get(self.SONGS_URL_ID_2)

        self.assertEqual(response.status_code, 404)

    def test_should_list_song_by_id(self):

        self.client.post(self.SONGS_URL, self.valid_song_data, format='json')
        self.client.post(self.SONGS_URL, self.valid_song_data_2, format='json')

        response_song_id_1 = self.client.get(self.SONGS_URL_ID_1)
        response_song_id_2 = self.client.get(self.SONGS_URL_ID_2)

        self.assertEqual(response_song_id_1.status_code, 200)
        self.assertEqual(response_song_id_1.json(), self.expected_song_data)

        self.assertEqual(response_song_id_2.status_code, 200)
        self.assertEqual(response_song_id_2.json(), self.expected_song_data_2)

    def test_should_not_update_song_with_invalid_data(self):

        invalid_data = {**self.invalid_artist_data, **self.invalid_song_data}
        incomplete_data = {**self.song_data}

        response_invalid_data = self.client.put(
            self.SONGS_URL_ID_1, invalid_data, format='json'
        )
        self.assertEqual(response_invalid_data.status_code, 400)

        response_incomplete_data = self.client.put(
            self.SONGS_URL_ID_1, incomplete_data, format='json'
        )
        self.assertEqual(response_incomplete_data.status_code, 400)

    def test_update_song_should_return_404_with_invalid_id(self):

        response = self.client.put(
            self.SONGS_URL_ID_1, self.valid_song_data, format='json'
        )
        self.assertEqual(response.status_code, 404)

    def test_should_update_song_title(self):
        updated_song = {**self.valid_song_data, 'title': 'New Title'}
        expected_song_data = {**self.expected_song_data, 'title': 'New Title'}

        self.client.post(self.SONGS_URL, self.valid_song_data, format='json')

        response_updated_data = self.client.put(
            self.SONGS_URL_ID_1, updated_song, format='json'
        )

        self.assertEqual(response_updated_data.status_code, 200)
        self.assertEqual(response_updated_data.json(), expected_song_data)

    def test_update_song_vote_count_should_return_404_with_invalid_id(self):

        response = self.client.patch(self.SONGS_URL_ID_1)
        self.assertEqual(response.status_code, 404)

    def test_should_update_song_vote_count(self):
        expected_song_data = {**self.expected_song_data, 'votes': 2}

        self.client.post(self.SONGS_URL, self.valid_song_data, format='json')

        response_updated_data = self.client.patch(self.SONGS_URL_ID_1)

        self.assertEqual(response_updated_data.status_code, 200)
        self.assertEqual(response_updated_data.json(), expected_song_data)

    def test_delete_song_should_return_404_with_invalid_id(self):

        response = self.client.delete(self.SONGS_URL_ID_1)
        self.assertEqual(response.status_code, 404)

    def test_should_delete_song(self):
        self.client.post(self.SONGS_URL, self.valid_song_data, format='json')

        response_delete_data = self.client.delete(self.SONGS_URL_ID_1)
        self.assertEqual(response_delete_data.status_code, 204)

        response_list_songs = self.client.get(self.SONGS_URL)
        self.assertEqual(response_list_songs.json(), [])
