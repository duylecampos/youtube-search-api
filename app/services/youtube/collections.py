from itertools import cycle
from collections.abc import Collection
from collections import Counter
from typing import List, Dict, Iterator

from .models import YoutubeMovie
from .utils import string_sanitize


class YoutubeCollection(Collection):

    SECONDS_IN_MINUTE = 60

    _movies = list()

    def __init__(self, movies: List[YoutubeMovie]):
        self._movies = movies

    def all(self) -> List[dict]:
        return self._movies

    def common_words(self, quantity: int = 5) -> Dict[str, int]:
        words = []
        for movie in self._movies:
            words += string_sanitize(movie.title).split()
            words += string_sanitize(movie.description).split()

        most_common_words = Counter(words).most_common(quantity)
        return {c[0]: c[1] for c in most_common_words}

    def days_to_watch_all(self, availability: List[int]) -> int:
        max_available_time = max(availability) * self.SECONDS_IN_MINUTE
        compatible_movies = filter(
            lambda movie: movie.duration_in_seconds <= max_available_time, self._movies
        )
        availability = cycle([day * self.SECONDS_IN_MINUTE for day in availability])

        spent_days = 0
        available_time = 0
        for movie in compatible_movies:
            while movie.duration_in_seconds > available_time:
                available_time = next(availability)
                spent_days += 1
            available_time -= movie.duration_in_seconds

        return spent_days

    def __contains__(self, movie: dict) -> bool:
        return movie in self._movies

    def __iter__(self) -> Iterator[YoutubeMovie]:
        for movie in self._movies:
            yield movie

    def __len__(self) -> int:
        return len(self._movies)
