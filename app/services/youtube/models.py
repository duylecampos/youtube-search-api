from dataclasses import dataclass
from isodate import isoduration


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

        if self._duration_in_seconds is None:
            parsed = isoduration.parse_duration(self.duration)
            self._duration_in_seconds = parsed.total_seconds()
        return self._duration_in_seconds


def factory(snippet: str, details: str) -> YoutubeMovie:
    detail_movie = next(
        filter(lambda item: item["id"] == snippet["id"]["videoId"], details["items"])
    )
    return YoutubeMovie(
        snippet["id"]["videoId"],
        snippet["snippet"]["title"],
        snippet["snippet"]["description"],
        detail_movie["contentDetails"]["duration"],
    )
