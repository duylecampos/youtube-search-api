import math
import requests
import aiohttp
import asyncio
from typing import Iterator

from .collections import YoutubeCollection
from .models import factory
from .utils import YoutubeUnavailable

from settings import YOUTUBE_API_KEY


class Youtube:
    MAX_ITEM_PER_PAGE = 50

    def _page_generator(self, max_results: int) -> Iterator[int]:
        total_pages = math.ceil(max_results / self.MAX_ITEM_PER_PAGE)

        for page_number in range(0, total_pages):
            is_last_page = (page_number + 1) == total_pages
            if is_last_page:
                yield abs(max_results - page_number * self.MAX_ITEM_PER_PAGE)
            else:
                yield self.MAX_ITEM_PER_PAGE

    async def _async_fetch(self, session, url: str, params: dict) -> dict:
        async with session.get(url, params=params,) as response:
            data = await response.json()
            if response.status != 200:
                raise YoutubeUnavailable(data)
            return data

    async def _fetch_videos_list(
        self, session, term: str, max_results_in_page: int, page_token: str
    ) -> dict:
        params = {
            "key": YOUTUBE_API_KEY,
            "part": "snippet",
            "q": term,
            "maxResults": max_results_in_page,
            "type": "video",
            "pageToken": page_token if page_token else "",
        }
        return await self._async_fetch(
            session, "https://www.googleapis.com/youtube/v3/search", params
        )

    async def _fetch_video_details(self, session, item: dict) -> dict:
        id = item["id"]["videoId"]
        params = {"key": YOUTUBE_API_KEY, "part": "contentDetails", "id": id}
        details = await self._async_fetch(
            session, "https://www.googleapis.com/youtube/v3/videos", params
        )
        return {"snippet": item, "details": details}

    async def _fetch_all(self, term: str, max_results: int):
        videos = list()
        async with aiohttp.ClientSession() as session:
            page_token = None
            for max_results_in_page in self._page_generator(max_results):
                video_list = await self._fetch_videos_list(
                    session, term, max_results_in_page, page_token
                )
                videos += await asyncio.gather(
                    *[
                        self._fetch_video_details(session, video)
                        for video in video_list["items"]
                    ]
                )
            return videos

    def search(self, term: str, max_results: int = 200) -> dict:
        videos = asyncio.run(self._fetch_all(term, max_results))

        return YoutubeCollection(
            [factory(video["snippet"], video["details"]) for video in videos]
        )
