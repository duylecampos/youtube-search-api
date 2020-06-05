import requests
import math
from typing import Iterator
from settings import YOUTUBE_API_KEY


class Youtube(object):
    MAX_ITEM_PER_PAGE = 50

    def _page_generator(self, max_results: int) -> Iterator[int]:
        total_pages = math.ceil(max_results / self.MAX_ITEM_PER_PAGE)

        for page_number in range(0, total_pages):
            is_last_page = (page_number + 1) == total_pages
            if is_last_page:
                yield abs(max_results - page_number * self.MAX_ITEM_PER_PAGE)
            else:
                yield self.MAX_ITEM_PER_PAGE

    def _fetch_youtube_data(
        self, term: str, max_results_in_page: int, page_token: str
    ) -> dict:
        response = requests.get(
            "https://www.googleapis.com/youtube/v3/search",
            params={
                "key": YOUTUBE_API_KEY,
                "part": "snippet",
                "q": term,
                "maxResults": max_results_in_page,
                "pageToken": page_token,
            },
        ).json()
        return response

    def search(self, term: str, max_results: int = 200) -> dict:
        movies = list()
        page_token = None
        for max_results_in_page in self._page_generator(max_results):
            response = self._fetch_youtube_data(term, max_results_in_page, page_token)
            page_token = response["nextPageToken"]
            movies = movies + response["items"]
        return movies
