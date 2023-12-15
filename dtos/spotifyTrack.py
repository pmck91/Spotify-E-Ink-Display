from dataclasses import dataclass


@dataclass
class SpotifyTrack:
    """Holds spotify tack data"""
    track_id: str
    track: str
    artists: [str]
    image_url: str

    def __str__(self):
        return f"id: {self.track_id} | track: {self.track} | artist(s): {self.artists} | image url: {self.image_url}"

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.track_id == other.track_id
        else:
            return False
