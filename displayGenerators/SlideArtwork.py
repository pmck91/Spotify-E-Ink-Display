import os
import logging.config
import random
from datetime import datetime
from PIL import Image


class SlideHandler:
    previous_slide_file = "default/logo.jpg"
    slide_last_update: datetime
    logger = logging.getLogger()

    def __init__(self, start_time: datetime):
        self.slide_last_update = start_time

    def get_slide(self):
        slide = self.__choose_slide()
        slide_image = Image.open(f"./images/slides/{slide}")
        self.previous_slide_file = slide
        self.slide_last_update = datetime.now()
        self.logger.info(f"Changing the slide to: {slide}")
        return slide_image

    def __choose_slide(self):
        slide_files = list(filter(lambda pth: os.path.isfile(f"./images/slides/{pth}"), os.listdir("./images/slides")))
        if self.previous_slide_file in slide_files:
            slide_files.remove(self.previous_slide_file)

        if not slide_files:
            self.logger.info("no images in slides, displaying elk logo")
            return "default/logo.jpg"
        return random.choice(slide_files)