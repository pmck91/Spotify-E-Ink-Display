import logging.config
from PIL import Image
from inky.auto import auto as auto_display


class Display:
    """Manages the Inky Display"""
    logger = logging.getLogger()

    def __init__(self):
        self.inky = auto_display(verbose=True)

    def display(self, image: Image, saturation: float = 0.5):
        try:
            display_image = image
            if (display_image.width != 600) and (display_image.height != 448):
                self.logger.warning(f"Image {display_image} is not 600*448px, cannot display without cropping")
                display_image = image.resize(size=(600, 448), resample=Image.Resampling.LANCZOS)

            self.inky.set_image(display_image, saturation=saturation)
            self.inky.show()
        except ValueError as ex:
            self.logger.error("Failed to display image", ex)
