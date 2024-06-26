import pytest

def test_is_playing_true(spotify_vision):
    assert spotify_vision.is_playing() == False

def test_artist_name(spotify_vision):
    assert spotify_vision.artist() == "string"

def test_song_name(spotify_vision):
    assert spotify_vision.song() == "string"

def test_pause(spotify_vision):
    assert spotify_vision.pause() == None

def test_resume(spotify_vision):
    assert spotify_vision.resume() != None

def test_next_song(spotify_vision):
    assert spotify_vision.next_song() == None

def test_print_playing(spotify_vision):
    assert spotify_vision.print_playing() == "Playing: string by string"

def test_print_paused(spotify_vision):
    assert spotify_vision.print_paused() == "Paused: string by string"

def test_like_song(spotify_vision):
    assert spotify_vision.print_liked() == "Liked: string by string"

def test_display_playlists(spotify_vision):
    assert isinstance(spotify_vision.display_playlists(), dict)





