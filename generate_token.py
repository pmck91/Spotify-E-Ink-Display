import os
import configparser
import logging.config
from spotipy.oauth2 import SpotifyOAuth

logging.config.fileConfig("config/logging.ini")
logger = logging.getLogger()
config = configparser.ConfigParser()
config.read("config/config.ini")

cache_path = config.get("spotify", "cache_location", fallback="spotifyCache/.spotifyCache")

logger.info(f"Generating Spotify Token, Please open the following link in a browser, and copy the url it forwards to")
scope = "user-read-currently-playing"

auth = SpotifyOAuth(scope=scope, open_browser=False, cache_path=cache_path)
auth.get_access_token(as_dict=False)

if os.path.isfile(cache_path):
    logger.info(f"Spotify Token Cache stored here: '{cache_path}'")
else:
    logger.error("Failed to generate Spotify Token")
