#!/usr/bin/env python3

import logging.config
import os
import sys
import time
import configparser
import random
from enum import Enum
from inky.auto import auto as auto_display
from datetime import datetime, timedelta
from PIL import Image

from dtos.spotifyTrack import SpotifyTrack
from exceptions.spotifyException import SpotifyException, NoSpotifySessionException
from apiConsumers.spotifyApi import get_playback_info
from displayGenerators.spotifyArtwork import SpotifyTrackImage


class CurrentDisplay(Enum):
    SPOTIFY = 1
    SLIDE = 2
    NONE = 3


logging.config.fileConfig('config/logging.ini')
logger = logging.getLogger()
config = configparser.ConfigParser()
config.read("config/config.ini")


def _choose_slide():
    slide_files = list(filter(lambda pth: os.path.isfile(f"./images/slides/{pth}"), os.listdir("./images/slides")))
    if previous_slide_file in slide_files: slide_files.remove(previous_slide_file)

    if not slide_files:
        logger.info("no images in slides, displaying elk logo")
        return "default/logo.jpg"
    return random.choice(slide_files)


SLIDES_DISPLAY_REFRESH = int(config.get("display", "slides_interval", fallback=20))
DISPLAY_SLIDES = int(config.get("display", "display_slides", fallback=0))
SPOTIFY_POLLING_INTERVAL = int(config.get("spotify", "polling_interval_seconds", fallback=20))

slide_last_update = datetime.now()

previous_playback_item = SpotifyTrack("", "", [""], "")
previous_slide_file = "default/logo.jpg"
currently_displayed = CurrentDisplay.NONE
display = auto_display(verbose=True)

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
                display.set_image(artwork)
                display.show()

        except NoSpotifySessionException as ex:
            if DISPLAY_SLIDES == 1:
                if currently_displayed != CurrentDisplay.SLIDE:
                    logger.info("No Spotify Session, displaying slides")
                    currently_displayed = CurrentDisplay.SLIDE
                    slide = _choose_slide()
                    slide_image = Image.open(f"./images/slides/{slide}")
                    previous_slide_file = slide
                    slide_last_update = datetime.now()
                    logger.info(f"Changing the slide to: {slide}")
                    # send it to the display
                    display.set_image(slide_image)
                    display.show()

        except SpotifyException as ex:
            logger.warning(ex.message)

        if CurrentDisplay == CurrentDisplay.SLIDE:
            if current_time - slide_last_update >= timedelta(minutes=SLIDES_DISPLAY_REFRESH):
                slide = _choose_slide()
                slide_image = Image.open(f"./images/slides/{slide}")
                previous_slide_file = slide
                slide_last_update = datetime.now()
                logger.info(f"Changing the slide to: {slide}")
                # send it to the display
                display.set_image(slide_image)
                display.show()

        time.sleep(SPOTIFY_POLLING_INTERVAL)
    except KeyboardInterrupt:
        logger.info("See ya later!")
        sys.exit(0)
