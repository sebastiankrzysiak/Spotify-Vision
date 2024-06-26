import pytest
import os
import json
from unittest import mock
from spotifyvision import SpotifyVision

with open('mock_spotify_data.json', 'r') as f:
    mock_current_playback_data = json.load(f)
with open('mock_spotify_playlist_data.json', 'r') as f:
    mock_current_playlist_data = json.load(f)

@pytest.fixture
def spotify_vision():
    with mock.patch.dict(os.environ, {
        'SPOTIPY_CLIENT_ID': 'mock_client_id',
        'SPOTIPY_CLIENT_SECRET': 'mock_client_secret'
    }):
        with mock.patch('spotipy.Spotify') as mock_spotify, \
             mock.patch('spotipy.oauth2.SpotifyOAuth') as mock_spotify_oauth:
            
            mock_spotify_oauth.return_value = mock.Mock()
            mock_spotify.return_value.devices.return_value = {"devices": [{"id": "device1", "name": "Device 1", "is_active": True}]}
            mock_spotify.return_value.current_user_playlists.return_value = mock_current_playlist_data
            mock_spotify.return_value.current_playback.return_value = mock_current_playback_data
            mock_spotify.return_value.pause_playback.return_value = None
            mock_spotify.return_value.resume_playback.return_value = None
            mock_spotify.return_value.next_track.return_value = None

            with mock.patch('builtins.input', return_value='1'):
                sv = SpotifyVision()

            yield sv
