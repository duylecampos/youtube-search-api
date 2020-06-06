from dataclasses import dataclass
from metomi.isodatetime.parsers import DurationParser

@dataclass
class YoutubeMovie:
    id: str
    title: str
    description: str
    duration: str

    def duration_in_seconds(self):
        parsed = DurationParser().parse(self.duration)
        return parsed.get_seconds()


def factory(snippet: str, details: str) -> YoutubeMovie:
    detail_movie = next(filter(lambda item: item['id'] == snippet['id'], details['items']))
    return YoutubeMovie(
        snippet['id'],
        snippet['snippet']['title'],
        snippet['snippet']['description'],
        detail_movie['contentDetails']['duration']
    )
