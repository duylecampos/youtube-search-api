from . import respositories


class Youtube:

    _movies = None

    def __init__(self, term: str):
        repo = respositories.Youtube()
        self._movies = repo.search(term, 200)

    def get_all(self):
        return self._movies.all()

    def common_words(self):
        return self._movies.common_words()

    def days_to_watch_all(self, availability: int):
        return self._movies.days_to_watch_all(availability)
