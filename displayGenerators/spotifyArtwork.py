import logging

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from io import BytesIO
import requests

from dtos.spotifyTrack import SpotifyTrack


class SpotifyTrackImage:
    """Generates an image to display based on spotify data"""
    track_info: SpotifyTrack
    font: ImageFont
    image: Image
    logger = logging.getLogger()
    blur_factor = 7
    dim_factor = 0.5
    default_font_size = 30
    x_border = 50

    def __init__(self, track_info: SpotifyTrack):
        self.track_info = track_info
        self.font = ImageFont.truetype("./font/GothamMedium.ttf")

    def generate(self):
        self.__fetch_image_from_spotify()
        self.__blur_bg_and_overlay_thumbnail()
        self.__draw_track_and_artist_text()

        file_path = f"images/tracks/{self.track_info.track_id}.png"

        self.logger.info(file_path)

        # crop the image to fit the inky impression 5.7, change these values for other displays
        cropped_for_inky = self.image.crop((0, 76, 600, 524))
        cropped_for_inky.save(file_path)
        return cropped_for_inky

    def __draw_track_and_artist_text(self):
        artists = ', '.join(map(str, self.track_info.artists))
        track_font_size = self.__calculate_font_size(self.track_info.track, self.default_font_size)
        artists_font_size = self.__calculate_font_size(artists, track_font_size - 5)
        self.__draw_track(track_font_size)
        self.__draw_artists(artists, artists_font_size)

    def __draw_track(self, font_size: int):
        x = self.x_border
        y = 524 - 64 - font_size
        draw = ImageDraw.Draw(self.image)
        draw.text((x + 3, y + 3), self.track_info.track, font=self.font.font_variant(size=font_size),
                  fill=(28, 28, 28))
        draw.text((x, y), self.track_info.track, font=self.font.font_variant(size=font_size))

    def __draw_artists(self, artists: str, artists_font_size: int):
        draw = ImageDraw.Draw(self.image)
        x = self.x_border
        y = 524 - 60

        draw.text((x + 3, y + 3), artists, font=self.font.font_variant(size=artists_font_size),
                  fill=(28, 28, 28))
        draw.text((x, y), artists, font=self.font.font_variant(size=artists_font_size))

    def __blur_bg_and_overlay_thumbnail(self):
        thumbnail = self.image.resize(size=(300, 300), resample=Image.Resampling.LANCZOS)
        image = self.image.filter(ImageFilter.GaussianBlur(self.blur_factor))
        dimmer = ImageEnhance.Brightness(image)
        self.image = dimmer.enhance(self.dim_factor)
        self.image.paste(thumbnail, (150, 100), thumbnail)

    def __fetch_image_from_spotify(self):
        self.logger.info(f"Fetching artwork for track: '{self.track_info.track_id}'")
        try:
            # throw if we dont get the image
            response = requests.get(self.track_info.image_url)
            response.raise_for_status()

            self.image = Image.open(BytesIO(response.content)).convert("RGBA").resize((600, 600))
        except requests.exceptions.RequestException as ex:
            self.logger.warning(f"was unable to fetch an image for track: '{self.track_info.track_id}'. Displaying default artwork", ex)
            self.image = Image.open("../images/system/no_artwork.png").convert("RGBA")
        self.draw = ImageDraw.Draw(self.image)

    def __calculate_font_size(self, string: str, starting_font_size: int):
        image_width_minus_borders = 500
        track = string
        font_size = starting_font_size
        draw = ImageDraw.Draw(self.image)

        while True:
            font = self.font.font_variant(size=font_size)
            text_width = draw.textlength(track, font)
            if text_width < image_width_minus_borders:
                return font_size

            font_size -= 1
