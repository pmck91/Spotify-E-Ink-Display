import spotipy
import configparser
from spotipy.oauth2 import SpotifyOAuth

from dtos.spotifyTrack import SpotifyTrack
from exceptions.spotifyException import NoSpotifySessionException, SpotifyException

config = configparser.ConfigParser()
config.read("config/config.ini")

cache_path = config.get("spotify", "cache_location", fallback="spotifyCache/.spotifyCache")


def __dict_to_spotify_track(api_response: dict):
    if api_response is None:
        raise NoSpotifySessionException("No Response returned from spotify")

    if "item" not in api_response:
        raise SpotifyException("No track info returned from spotify")
    else:
        item = api_response["item"]

        track_id = item["id"]
        track = item["name"]

        if "album" in item:
            artists = list(map(lambda artist: artist["name"], item["artists"]))
            image_url = item["album"]["images"][0]["url"]
        else:
            artists = [item["show"]["name"]]
            image_url = item["show"]["images"][0]["url"]

        return SpotifyTrack(track_id, track, artists, image_url)


def get_playback_info():
    scope = "user-read-currently-playing"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, open_browser=False, cache_path=cache_path))
    spotify_response = sp.currently_playing(additional_types="track,episode")
    return __dict_to_spotify_track(spotify_response)
