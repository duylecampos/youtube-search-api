import pytest

from app.services.youtube.collections import YoutubeCollection
from app.services.youtube.models import YoutubeMovie


@pytest.mark.parametrize(
    "movies",
    [
        [
            YoutubeMovie(
                "TJVbhpN7l_4",
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus porta volutpat ante id tristique",
                "Suspendisse sed suscipit sapien. Mauris lobortis accumsan est, et lacinia velit feugiat ultrices. Mauris et urna non felis aliquet consectetur. Sed ullamcorper in est at feugiat. Aliquam erat volutpat. Aliquam aliquet laoreet volutpat. Nunc a sem interdum, sollicitudin elit et, gravida ex. Aliquam tincidunt lobortis libero, sit amet dictum velit placerat sit amet. Quisque semper nibh nisi, vel pharetra est porta imperdiet.",
                "PT6M39S",
                "https://i.ytimg.com/vi/WRKYfRPTcy0/mqdefault.jpg",
            )
        ]
    ],
)
def test_common_words(movies):
    c = YoutubeCollection(movies)
    common_words = c.common_words()
    assert common_words == {"amet": 3, "est": 3, "et": 3, "sit": 3, "volutpat": 3}


@pytest.mark.parametrize(
    "movies_time,availability,days_spent",
    [
        (["PT6M39S", "PT1M"], [15, 20, 45], 1),
        (
            [
                "PT20M",
                "PT30M",
                "PT60M",
                "PT90M",
                "PT200M",
                "PT30M",
                "PT40M",
                "PT20M",
                "PT60M",
                "PT15M",
            ],
            [15, 120, 30, 150, 20, 40, 90],
            8,
        ),
        (["PT6M39S", "PT1M"], [15, 20, 45, 30, 10, 5, 0], 1),
        (["PT6M39S", "PT1M"], [0, 0, 0, 0, 0, 5, 10], 7),
        (["PT6M39S", "PT1M"], [0, 0, 0, 0, 0, 5, 5], 6),
        (["PT200M", "PT250M", "PT2H40M", "PT3H"], [15, 120, 30, 150, 20, 40, 90], 0),
    ],
)
def test_days_to_watch_all(movies_time, availability, days_spent):
    movies = [
        YoutubeMovie(None, None, None, duration, None) for duration in movies_time
    ]
    c = YoutubeCollection(movies)
    days = c.days_to_watch_all(availability)
    assert days == days_spent
