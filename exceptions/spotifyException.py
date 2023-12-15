class SpotifyException(Exception):
    """Generic Exception for interacting with spotify"""
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class NoSpotifySessionException(Exception):
    """Raise when no track is playing"""
    def __init__(self, message):
        super().__init__(message)
        self.message = message
