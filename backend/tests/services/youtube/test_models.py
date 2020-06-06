import pytest
from dataclasses import asdict
from app.services.youtube.models import YoutubeMovie, factory


@pytest.mark.parametrize(
    "input",
    [
        {
            "id": "TJVbhpN7l_4",
            "title": "Lorem ipsum dolor sit amet",
            "description": "Mauris lobortis accumsan est, et lacinia velit feugiat ultrices. Mauris et urna non felis aliquet consectetur. ",
            "duration": "PT6M39S",
        }
    ],
)
def test_constructor(input):
    movie = YoutubeMovie(**input)
    assert asdict(movie) == input


@pytest.mark.parametrize(
    "input,expected",
    [("PT6M39S", 399), ("PT39S", 39), ("P1DT5M49S", 86749), ("PT99S", 99)],
)
def test_duration_in_seconds(input, expected):
    movie = YoutubeMovie(None, None, None, input)
    duration = movie.duration_in_seconds
    assert duration == expected


@pytest.mark.parametrize(
    "snippet,details,expected",
    [
        (
            {
                "id": "TJVbhpN7l_4",
                "snippet": {
                    "title": "Lorem ipsum dolor sit amet",
                    "description": "Mauris lobortis accumsan est, et lacinia velit feugiat ultrices. Mauris et urna non felis aliquet consectetur. ",
                },
            },
            {
                "items": [
                    {"id": "TJVbhpN7l_4", "contentDetails": {"duration": "PT6M39S"}}
                ]
            },
            YoutubeMovie(
                "TJVbhpN7l_4",
                "Lorem ipsum dolor sit amet",
                "Mauris lobortis accumsan est, et lacinia velit feugiat ultrices. Mauris et urna non felis aliquet consectetur. ",
                "PT6M39S",
            ),
        )
    ],
)
def test_factory(snippet, details, expected):
    movie = factory(snippet, details)
    assert movie == expected
