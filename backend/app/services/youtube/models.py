from dataclasses import dataclass
from metomi.isodatetime.parsers import DurationParser


@dataclass
class YoutubeMovie:
    id: str
    title: str
    description: str
    duration: str

    _duration_in_seconds = None

    @property
    def duration_in_seconds(self) -> int:
        """
        Convert ISO8601 duration from youtube to seconds
        """

        parsed = DurationParser().parse(self.duration)
        if self._duration_in_seconds is None:
            self._duration_in_seconds = parsed.get_seconds()
        return self._duration_in_seconds


def factory(snippet: str, details: str) -> YoutubeMovie:
    detail_movie = next(
        filter(lambda item: item["id"] == snippet["id"], details["items"])
    )
    return YoutubeMovie(
        snippet["id"],
        snippet["snippet"]["title"],
        snippet["snippet"]["description"],
        detail_movie["contentDetails"]["duration"],
    )
