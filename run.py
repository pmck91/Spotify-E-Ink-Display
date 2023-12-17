#!/usr/bin/env python3

import logging.config
import os
import sys
import time
import configparser
from enum import Enum
from datetime import datetime, timedelta
from PIL import Image

from dtos.spotifyTrack import SpotifyTrack
from exceptions.spotifyException import SpotifyException, NoSpotifySessionException
from apiConsumers.spotifyApi import get_playback_info
from displayGenerators.spotifyArtwork import SpotifyTrackImage
from displayGenerators.SlideArtwork import SlideHandler
from display import Display


class CurrentDisplay(Enum):
    SPOTIFY = 1
    SLIDE = 2
    NONE = 3


# Set up logging and config reader
logging.config.fileConfig('config/logging.ini')
logger = logging.getLogger()
config = configparser.ConfigParser()
config.read("config/config.ini")

# Get config data
SLIDES_DISPLAY_REFRESH = int(config.get("display", "slides_interval", fallback=20))
DISPLAY_SLIDES = int(config.get("display", "display_slides", fallback=0))
SPOTIFY_POLLING_INTERVAL = int(config.get("spotify", "polling_interval_seconds", fallback=20))

slide_handler = SlideHandler(datetime.now())
previous_playback_item = SpotifyTrack("", "", [""], "")
currently_displayed = CurrentDisplay.NONE
inky = Display()

while True:
    current_time = datetime.now()

    try:
        try:
            playback_item = get_playback_info()
            currently_displayed = CurrentDisplay.SPOTIFY
            if previous_playback_item != playback_item:
                file_path = f"images/tracks/{playback_item.track_id}.png"

                if os.path.isfile(file_path):
                    logger.info(f"Artwork for track {playback_item.track_id} already cached")
                    artwork = Image.open(file_path).convert("RGBA")
                else:
                    artwork = SpotifyTrackImage(playback_item).generate()

                previous_playback_item = playback_item

                # send artwork to display
                inky.display(artwork)

        except NoSpotifySessionException as ex:
            if DISPLAY_SLIDES == 1:
                if currently_displayed != CurrentDisplay.SLIDE:
                    logger.info("No Spotify Session, displaying slides")
                    currently_displayed = CurrentDisplay.SLIDE
                    inky.display(slide_handler.get_slide())

        except SpotifyException as ex:
            logger.warning(ex.message)

        if CurrentDisplay == CurrentDisplay.SLIDE:
            if current_time - slide_handler.slide_last_update >= timedelta(minutes=SLIDES_DISPLAY_REFRESH):
                inky.display(slide_handler.get_slide())

        time.sleep(SPOTIFY_POLLING_INTERVAL)
    except KeyboardInterrupt:
        logger.info("See ya later!")
        sys.exit(0)
